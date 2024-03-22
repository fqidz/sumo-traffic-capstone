# TODO: use waiting time for reward
# TODO: check if cars are stuck in the junction
import traci
import random
import numpy as np
import time
import os


class TraciSim:
    def __init__(self, duration=1000) -> None:
        if os.name == 'nt':
            sumo_path = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo.exe"
            cfg_path = "../sumo-things/main.sumocfg"
        else:
            sumo_path = "/usr/share/sumo/bin/sumo-gui"
            cfg_path = "./sumo-things/main.sumocfg"

        self.sumo_cmd = [sumo_path, "-c", cfg_path]
        traci.start(self.sumo_cmd)

        self.traffic_id = "0"
        self.lanearea_ids = traci.lanearea.getIDList()
        self.duration = duration

        self.score = 0
        self.frame_iteration = 0
        self.reward = 0

        self.traffic_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.mean_speeds = np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.jam_length = np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    def reset(self):
        traci.close()
        traci.start(self.sumo_cmd)

        self.score = 0
        self.reward = 0
        self.frame_iteration = 0

        self.traffic_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.mean_speeds = np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.jam_length = np.array(
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    def getMeanSpeedInLanearea(self, lanearea_ids: tuple) -> None:
        """returns [eastLAD0, eastLAD1, northLAD0, ... , westLAD2]"""
        lanearea_mean_speed = {}
        for i in lanearea_ids:
            lanearea_mean_speed[i] = traci.lanearea.getLastStepMeanSpeed(
                i)

        # Split the keys by "_" and use the first part (direction) as the key in the summed_values dictionary
        mean_speed_sum = {}
        # count amount of lane segments to mean it later
        lane_segment_count = {}
        for key, value in lanearea_mean_speed.items():
            direction = key.split("_")[0]
            if direction not in mean_speed_sum:
                lane_segment_count[direction] = 0
                mean_speed_sum[direction] = 0
            else:
                lane_segment_count[direction] += 1
                mean_speed_sum[direction] += value

        # turn dict into list
        mean_speed_list = list(mean_speed_sum.values())
        dir_count_list = list(lane_segment_count.values())

        # get mean speed among the separated lanearea detectors, then normalize to max car speed
        mean_speeds = np.divide(mean_speed_list, dir_count_list)
        mean_speeds_normalized = np.round(
            np.divide(mean_speeds, 55.55), decimals=5)
        # make negative numbers round up to 0
        mean_speeds_normalized = mean_speeds_normalized.clip(min=0.0)

        self.mean_speeds = mean_speeds_normalized

    def getJamLengthInLanearea(self, lanearea_ids: tuple) -> None:
        """returns [eastLAD0, eastLAD1, northLAD0, ... , westLAD2]"""

        lanearea_jam = {}
        for i in lanearea_ids:
            lanearea_jam[i] = traci.lanearea.getLastIntervalMaxJamLengthInMeters(
                i)

        # Split the keys by "_" and use the first part (direction) as the key in the summed_values dictionary
        jam_count_sum = {}
        for key, value in lanearea_jam.items():
            direction = key.split("_")[0]
            if direction not in jam_count_sum:
                jam_count_sum[direction] = 0
            else:
                jam_count_sum[direction] += value

        max_jam_length = [230.56, 257.9656622406022, 306.3, 306.3, 306.3,
                          320.74, 348.64720360752835, 238.69, 230.32428296642462, 238.69]
        jam_length = list(jam_count_sum.values())

        # normalize jam length
        jam_length_normalized = np.round(
            np.divide(jam_length, max_jam_length), decimals=5)

        self.jam_length = jam_length_normalized

    def setState(self, traffic_id: str, state_input: list[float]) -> None:
        """converts list of floats to a string of state and sets the traffic state to that"""
        _state_output = []
        # states are grouped together, so that each state represent a phase that matches with the lane
        # so that eg. left turns and u-turns traffic light signals are grouped together
        for i, phase in enumerate(state_input):
            if (i % 2 == 0):
                if (phase == 0.0):
                    _state_output.append('rr')
                elif (phase == 0.5):
                    _state_output.append('yy')
                elif (phase == 1.0):
                    _state_output.append('GG')
                else:
                    raise Exception(
                        f'State should be 0.0, 0.5, or 1.0, not {phase}')
            else:
                if (phase == 0.0):
                    _state_output.append('rrrr')
                elif (phase == 0.5):
                    _state_output.append('yyyy')
                elif (phase == 1.0):
                    _state_output.append('GGGG')
                else:
                    raise Exception(
                        f'State should be 0.0, 0.5, or 1.0, not {phase}')

        _state_string = ''.join(_state_output)
        # set state
        traci.trafficlight.setRedYellowGreenState(traffic_id, _state_string)

    def play_step(self, traffic_state):
        # TODO: reward giving
        game_over = False
        self.reward = 0

        # game over if duration exceeds limit
        if self.frame_iteration >= self.duration:
            game_over = True
            return self.reward, game_over, self.score

        # give punishments if:
        # vehicles collide
        # vehicles emergency stop
        for i in range(traci.simulation.getCollidingVehiclesNumber()):
            self.reward -= 0.1

        for i in range(traci.simulation.getEmergencyStoppingVehiclesNumber()):
            self.reward -= 0.1

            self.reward += np.average(self.mean_speeds) * 0.5

        # TODO: make this score be something that we want to aim for, like queue length or waiting times
        self.score += traci.simulation.getArrivedNumber()

        self.getJamLengthInLanearea(self.lanearea_ids)
        self.getMeanSpeedInLanearea(self.lanearea_ids)

        # traffic state is the input
        self.traffic_state = traffic_state
        self.setState(self.traffic_id, self.traffic_state)

        traci.simulationStep()
        self.frame_iteration += 1

        return self.reward, game_over, self.score
