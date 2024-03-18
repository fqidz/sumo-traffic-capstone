# TODO: replace with activityGen.py TODO: prompt if user wants to rerun randomTrips.py command argument stuff
# TODO: also generate lane area detectors
# TODO: move the todo functionalities to separate scripts
import traci
import random

NET_PATH = "./sumo-things/net.net.xml"
VEHICLE_CLASS_PATH = "./sumo-things/vehicleClass.add.xml"
# STAT_PATH = '"~/Documents/sumo-traffic-capstone/activity.stat.xml"'

# ask user to use activityGen or not
# generate_activity = input("Generate activity? (y/n)")
# if generate_activity.lower() == 'y':
#     subprocess.run(["python3", '"$SUMO_HOME/tools/activityGen.py"', "--net-file", NET_PATH, "--stat-file", STAT_PATH, "--output-file", '"./trips.rou.xml"', "--random"])


# ask user to use randomTrips or not

# start traci stuff
SUMOGUI_PATH = "/usr/share/sumo/bin/sumo-gui"
SUMOCFG_PATH = "./sumo-things/main.sumocfg"
sumo_cmd = [SUMOGUI_PATH, "-c", SUMOCFG_PATH]


def count_cars_in_lanearea(lanearea_ids: tuple) -> dict:
    """returns the amount of cars in each lanearea detector"""
    # get the count of cars for each lane area detector
    lanearea_count = {}
    for i in lanearea_ids:
        lanearea_count[i] = traci.lanearea.getLastStepVehicleNumber(i)

    # sum the lanearea detector car counts into each of the directions
    lanearea_count_sum = {}
    for dir in ["east", "north", "south", "west"]:
        direction_values = {key: value for key,
                            value in lanearea_count.items() if key.startswith(dir)}
        lanearea_count_sum[dir] = sum(direction_values.values())

    return lanearea_count_sum


def switchPhase(traffic_id: str, phase: int):
    """switch traffic light phase"""
    traci.trafficlight.setPhase(traffic_id, phase)
    traci.trafficlight.setPhaseDuration(traffic_id, 999999)


traci.start(sumo_cmd)

time_since_last_phase = 0
traffic_phase_duration_green = 999999
traffic_phase_duration_yellow = 5
phase = 0

for i in range(5000):
    lanearea_id_list = traci.lanearea.getIDList()
    lanearea_car_count = count_cars_in_lanearea(lanearea_id_list)
    print(lanearea_car_count)

    if (time_since_last_phase == 0):
        traffic_phase_duration_green = random.randint(20, 100)

    print(f'traffic phase duration: {traffic_phase_duration_green}')
    print(f'time since last phase: {time_since_last_phase}')

    if (time_since_last_phase >= traffic_phase_duration_green):
        # reset time since last phase
        time_since_last_phase = 0
        # choose random phase and switch to it
        phase = random.choice([0, 2, 4, 6, 8, 10, 12, 14])
        switchPhase("30896504", phase)

    if (time_since_last_phase >= traffic_phase_duration_green - traffic_phase_duration_yellow):
        # if close to next phase, change it to yellow light
        switchPhase("30896504", phase + 1)

    print(f'current phase: {traci.trafficlight.getPhase("30896504")}')

    traci.simulationStep()
    time_since_last_phase += 1

traci.close()
