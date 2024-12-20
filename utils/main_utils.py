import numpy as np
from gymnasium import spaces
from sumo_rl.environment.observations import ObservationFunction
from sumo_rl.environment.traffic_signal import TrafficSignal


class MyObservationFunction(ObservationFunction):

    def __init__(self, ts: TrafficSignal):
        super().__init__(ts)

    def __call__(self):
        phase_id = [1 if self.ts.green_phase == i else 0 for i in range(
            self.ts.num_green_phases)]  # one-hot encoding
        min_green = [0 if self.ts.time_since_last_phase_change <
                     self.ts.min_green + self.ts.yellow_time else 1]
        density = self.ts.get_lanes_density()
        queue = self.ts.get_lanes_queue()
        speed = self.ts.get_lanes_speed()
        observation = np.array(phase_id + min_green +
                               density + queue + speed, dtype=np.float32)
        print(f'lanes density: {np.array(density)}')
        print(f'queue length: {np.array(queue)}')
        print(f'vehicle speed: {np.array(speed)}')
        print('')
        return observation

    def observation_space(self):
        return spaces.Box(
            low=np.zeros(self.ts.num_green_phases + 1 + 3 *
                         len(self.ts.lanes), dtype=np.float32),
            high=np.ones(self.ts.num_green_phases + 1 + 3 *
                         len(self.ts.lanes), dtype=np.float32),
        )


def my_reward_fn(traffic_signal):
    speed = traffic_signal.get_average_speed() * 10
    queue = -np.average(traffic_signal.get_total_queued())

    # print(f'reward: {speed + queue}')

    return speed + queue
