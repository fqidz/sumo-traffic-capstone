from traci import init
from sumo_rl import SumoEnvironment
from pathlib import Path
import numpy as np
import pandas as pd
import traci

Path("./output/actuated/traffic-stats/").mkdir(parents=True, exist_ok=True)
# Path("./output/actuated/logs/").mkdir(parents=True, exist_ok=True)
# Path("./output/actuated/models/").mkdir(parents=True, exist_ok=True)

num_seconds = 43500
delta_time = 10


# def _get_system_info(self):
#     vehicles = self.sumo.vehicle.getIDList()
#     speeds = [self.sumo.vehicle.getSpeed(vehicle) for vehicle in vehicles]
#     waiting_times = [self.sumo.vehicle.getWaitingTime(
#         vehicle) for vehicle in vehicles]
#     return {
#         # In SUMO, a vehicle is considered halting if its speed is below 0.1 m/s
#         "system_total_stopped": sum(int(speed < 0.1) for speed in speeds),
#         "system_total_waiting_time": sum(waiting_times),
#         "system_mean_waiting_time": 0.0 if len(vehicles) == 0 else np.mean(waiting_times),
#         "system_mean_speed": 0.0 if len(vehicles) == 0 else np.mean(speeds),
#     }
def save_csv(out_csv_name, metrics):
    """Save metrics of the simulation to a .csv file.

    Args:
        out_csv_name (str): Path to the output .csv file. E.g.: "results/my_results
        episode (int): Episode number to be appended to the output file name.
    """
    if out_csv_name is not None:
        df = pd.DataFrame(metrics)
        Path(Path(out_csv_name).parent).mkdir(parents=True, exist_ok=True)
        df.to_csv(out_csv_name +
                  f"actuated" + ".csv", index=False)


def _get_per_agent_info(veh_list, lane_list):
    speeds = [traci.vehicle.getSpeed(vehicle) for vehicle in veh_list]
    average_speed = get_average_speed(veh_list)
    total_queued = sum(traci.lane.getLastStepHaltingNumber(lane)
                       for lane in lane_list)
    info = {}
    info["system_mean_speed"] = 0.0 if len(veh_list) == 0 else np.mean(speeds),
    info[f"0_average_speed"] = average_speed
    info[f"0_queue_length"] = total_queued
    return info


def get_average_speed(veh_list) -> float:
    """Returns the average speed normalized by the maximum allowed speed of the vehicles in the intersection.

    Obs: If there are no vehicles in the intersection, it returns 1.0.
    """
    avg_speed = 0.0
    vehs = veh_list
    if len(vehs) == 0:
        return 1.0
    for v in vehs:
        avg_speed += traci.vehicle.getSpeed(
            v) / traci.vehicle.getAllowedSpeed(v)
    return avg_speed / len(vehs)


metrics = []

sumo_cmd = ['sumo-gui', '-c',
            './sumo-things/actuated/main.sumocfg', '--time-to-teleport', '2000']
traci.start(sumo_cmd)

lanes = list(
    dict.fromkeys(traci.trafficlight.getControlledLanes('0'))
)  # Remove duplicates and keep order

# added this:
extra_lanes = ['64661021#3_0', '64661021#3_1', '480041825#7_0', '480041825#7_1', '480041825#7_2',
               '480155244#4_0', '480155244#4_1', '480155244#4_2', '484449878#6_0', '484449878#6_1']
lanes.extend(extra_lanes)
lanes_dir: list[list[str]] = [
    ['281221761#1_0', '484449878#6_0', '281221761#1_1',
        '281221761#1_2', '484449878#6_1'],
    ['480155244#5_2', '480155244#4_2', '480155244#5_1',
        '480155244#4_1', '480155244#5_0', '480155244#4_0'],
    ['64661021#4_0', '64661021#3_0', '64661021#4_1',
        '64661021#3_1', '64661021#4_2'],
    ['480041825#9_2', '480041825#7_2', '480041825#9_1',
        '480041825#7_1', '480041825#9_0', '480041825#7_0'],
]


for _ in range(num_seconds):
    traci.simulationStep()
    # traci.trafficlight.setRedYellowGreenState('0', "rrrrrrrrrrrrrrrrrrrrrrrr")
    vehs = traci.vehicle.getIDList()
    info = {"step": traci.simulation.getTime()}
    all_info = _get_per_agent_info(vehs, lanes)
    info.update(all_info)
    if traci.simulation.getTime() % 10 == 0:
        metrics.append(info.copy())

    # veh_count_per_lane = []
    # for direction in lanes_dir:
    #     lane_dir_count = [
    #         traci.lane.getLastStepVehicleNumber(x) for x in direction]
    #     veh_count_per_lane.append(np.sum(lane_dir_count))
    # print(veh_count_per_lane)
    # veh_count_per_lane = np.divide(veh_count_per_lane, [60, 66, 42, 82])
    # print(veh_count_per_lane)

traci.close()

save_csv(out_csv_name='./output/actuated/traffic-stats/actuated3_', metrics=metrics)
