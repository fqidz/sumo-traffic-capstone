import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci

sumoBinary = "/usr/share/sumo/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "main.sumocfg"]

traci.start(sumoCmd)
for i in range(3000):
    traci.simulationStep()
    print(traci.vehicle.getIDCount())

traci.close()
