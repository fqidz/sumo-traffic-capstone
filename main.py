from sumo_rl import SumoEnvironment
from stable_baselines3.dqn.dqn import DQN
from pathlib import Path
import numpy as np
from gymnasium import spaces
from sumo_rl.environment.observations import ObservationFunction
from sumo_rl.environment.traffic_signal import TrafficSignal

Path("./output/traffic-stats/").mkdir(parents=True, exist_ok=True)
Path("./output/logs/").mkdir(parents=True, exist_ok=True)
Path("./output/models/").mkdir(parents=True, exist_ok=True)

num_seconds = 43500
delta_time = 10
# total seconds divided by delta time (time it takes for ai to take action)
agent_steps_per_episode = -(-num_seconds // delta_time)
episodes = 70


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
        # print(f'density: {density}')
        # print(f'queue: {queue}')
        # print(f'speed: {speed}')
        # print(f'observation: {observation}')
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


def ask_user(prompt: str) -> bool:
    repeat = True
    answer = False

    prompt_answer = input(prompt).lower()
    prompt_answer = "".join(prompt_answer.split())

    while repeat:
        if prompt_answer == "y":
            answer = True
            repeat = False
        elif prompt_answer == "n" or not prompt_answer:
            answer = False
            repeat = False
        else:
            repeat = True

    return answer


use_gui = ask_user("Use GUI? (y/N) ")

env = SumoEnvironment(net_file='./sumo-things/net.net.xml',
                      route_file='./sumo-things/main.rou.xml',
                      out_csv_name='./output/traffic-stats/traffic-sim-model4',
                      reward_fn=my_reward_fn,
                      delta_time=delta_time,
                      yellow_time=4,
                      min_green=10,
                      time_to_teleport=2000,
                      use_gui=use_gui,
                      single_agent=True,
                      num_seconds=num_seconds,
                      observation_class=MyObservationFunction
                      )


load_model = ask_user("Load model? (y/N) ")
if load_model:
    model = DQN.load('./output/models/model3.zip', print_system_info=True)
    model.set_env(env=env)
    model.learn(
        total_timesteps=agent_steps_per_episode * episodes, log_interval=1, callback=None, reset_num_timesteps=False)
else:
    model = DQN(
        env=env,
        policy="MlpPolicy",
        learning_rate=1e-3,
        learning_starts=0,
        buffer_size=50000,
        train_freq=1,
        target_update_interval=500,
        exploration_fraction=0.05,
        exploration_final_eps=0.01,
        verbose=1,
        tensorboard_log="./output/logs/"
    )
    model.learn(
        total_timesteps=agent_steps_per_episode * episodes, log_interval=1, callback=None)

model.save("./output/models/model3")
print("Model saved to ./output/")
