from sumo_rl import SumoEnvironment
from stable_baselines3.dqn.dqn import DQN
import numpy as np

num_seconds = 43200
episodes = 100

# reward_fns = {
#     "diff-waiting-time": _diff_waiting_time_reward,
#     "average-speed": _average_speed_reward,
#     "queue": _queue_reward,
#     "pressure": _pressure_reward,
# }


def my_reward_fn(traffic_signal):
    speed = traffic_signal.get_average_speed() * 2
    queue = -np.average(traffic_signal.get_total_queued()) * 0.75

    return speed + queue


env = SumoEnvironment(net_file='./sumo-things/net.net.xml',
                      route_file='./sumo-things/main.rou.xml',
                      out_csv_name='./sumo-things/output/dqn',
                      reward_fn=my_reward_fn,
                      yellow_time=4,
                      use_gui=True,
                      single_agent=True,
                      num_seconds=num_seconds)

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
)


model.learn(total_timesteps=num_seconds * episodes, log_interval=1)
