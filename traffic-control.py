# TODO: replace with activityGen.py
# TODO: prompt if user wants to rerun randomTrips.py command argument stuff
# TODO: also generate lane area detectors
# TODO: move the todo functionalities to separate scripts 
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

# junction 30896504
# east road 1: 281221761#1_0
# east road 2: 281221761#0_0
# north road 1: 480155244#5_0
# north road 2: 480155244#4_0
# west road 1: 480041825#9_0
# south road 1: 64661021#4_0
