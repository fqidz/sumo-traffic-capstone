# TODO: replace with activityGen.py
# TODO: prompt if user wants to rerun randomTrips.py command argument stuff
# TODO: also generate lane area detectors
# TODO: move the todo functionalities to separate scripts 
import traci

NET_PATH = "./sumo-things/net.net.xml"
VEHICLE_CLASS_PATH = "./sumo-things/vehicleClass.add.xml"
# STAT_PATH = '"~/Documents/sumo-traffic-capstone/activity.stat.xml"'

# ask user to use activityGen or not
# generate_activity = input("Generate activity? (y/n)")
# if generate_activity.lower() == 'y':
#     subprocess.run(["python3", '"$SUMO_HOME/tools/activityGen.py"', "--net-file", NET_PATH, "--stat-file", STAT_PATH, "--output-file", '"./trips.rou.xml"', "--random"])


# ask user to use randomTrips or not

# start traci stuff
# SUMOGUI_PATH = "/usr/share/sumo/bin/sumo-gui"
SUMOGUI_PATH = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
SUMOCFG_PATH = "./sumo-things/main.sumocfg"
sumo_cmd = [SUMOGUI_PATH, "-c", SUMOCFG_PATH]


# class lanearea_count():
#     def __init__(self) -> None:
#         self.east = {}
#         self.east1 = []
#         self.east2 = []
#         self.east3 = []
#         self.north1 = []
#         self.north2 = []
#         self.north3 = []
#         self.west1 = []
#         self.west2 = []
#         self.west3 = []
#         self.south1 = []
#         self.south2 = []
#         self.south3 = []

def count_cars_in_lanearea(lanearea_ids: tuple) -> list:
    """returns the amount of cars in each lanearea detector\n
       format: [east1-3, north1-3, south1-3, west1-3]"""
    lanearea_count = []
    for i in lanearea_ids:
        lanearea_count.append(traci.lanearea.getLastStepVehicleNumber(i))


    return lanearea_count


traci.start(sumo_cmd)

for i in range(5000):
    lanearea_car_count = count_cars_in_lanearea(traci.lanearea.getIDList())
    print(traci.lanearea.getIDList())
    print(lanearea_car_count)

    traci.simulationStep()

traci.close()
