from aiAgent.trafficSim import TraciSim
import random

sim = TraciSim()

while True:
    rand_state = []
    for i in range(8):
        rand_state.append(random.choice([0.0, 0.5, 1.0]))

    sim.play_step(rand_state)
