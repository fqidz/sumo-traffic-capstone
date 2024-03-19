# TODO: use queue length instead of count of cars
# TODO: use waiting time for reward
# TODO: check if cars are stuck in the junction
import traci
import traci.constants as tc


# [car count east, car count north, car count south, car count west
#  car avg speed east, car avg speed north, car avg speed south, car avg speed west
#
#  traffic light phase*]
#
# *format of: [rrGGyyrr] would be [0, 0, 1, 1, 0.5, 0.5, 0, 0]

SUMOGUI_PATH = "/usr/share/sumo/bin/sumo-gui"
SUMOCFG_PATH = "./sumo-things/main.sumocfg"

sumo_cmd = [SUMOGUI_PATH, "-c", SUMOCFG_PATH]


class TraciSim:
    def __init__(self) -> None:
        self.traffic_id = "0"
        self.traffic_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.lanearea_ids = traci.lanearea.getIDList()

    def countCarsInLanearea(self, lanearea_ids: tuple) -> dict:
        """returns the amount of cars in each lanearea detector"""
        # get the count of cars for each lane area detector
        lanearea_jam = {}
        for i in lanearea_ids:
            lanearea_jam[i] = traci.lanearea.getIntervalMaxJamLengthInMeters(i)

        # sum the lanearea detector car counts into each of the directions
        direction_values = {}
        for dir in ["eastLAD0", "northLAD0", "southLAD0", "westLAD0"]:
            direction_values = {key: value for key,
                                value in lanearea_jam.items() if key.startswith(dir)}
            direction_values[dir] = sum(direction_values.values())

        return direction_values

    def setState(self, traffic_id: str, state_input: list[float]) -> None:
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
                    raise Exception('State should be 0.0, 0.5, or 1.0')
            else:
                if (phase == 0.0):
                    _state_output.append('rrrr')
                elif (phase == 0.5):
                    _state_output.append('yyyy')
                elif (phase == 1.0):
                    _state_output.append('GGGG')
                else:
                    raise Exception('State should be 0.0, 0.5, or 1.0')

        _state_string = ''.join(_state_output)
        traci.trafficlight.setRedYellowGreenState(traffic_id, _state_string)

    def step(self):
        print(f'{self.countCarsInLanearea(self.lanearea_ids)}')
        self.setState(self.traffic_id, self.traffic_state)
        print(f'state: {traci.trafficlight.getRedYellowGreenState("0")}')
        print(self.lanearea_ids)
        traci.simulationStep()


traci.start(sumo_cmd)
sim = TraciSim()

for i in range(5000):

    sim.step()

traci.close()
