import traci
from aiAgent.trafficSim import TraciSim

SUMOGUI_PATH = "/usr/share/sumo/bin/sumo-gui"
SUMOCFG_PATH = "./sumo-things/main.sumocfg"

sumo_cmd = [SUMOGUI_PATH, "-c", SUMOCFG_PATH]

traci.start(sumo_cmd)
sim = TraciSim()

for i in range(5000):

    sim.step()

traci.close()
