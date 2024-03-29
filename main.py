from sumo_rl import SumoEnvironment
from stable_baselines3.dqn.dqn import DQN
from pathlib import Path
import numpy as np

Path("./output/dqn-stats/").mkdir(parents=True, exist_ok=True)
Path("./output/logs/").mkdir(parents=True, exist_ok=True)

num_seconds = 43500
# total seconds divided by 5 cause thats how long the ai takes to make a decision
agent_steps_per_episode = -(-num_seconds // 5)
episodes = 150


def my_reward_fn(traffic_signal):
    speed = traffic_signal.get_average_speed() * 2
    queue = -np.average(traffic_signal.get_total_queued()) * 0.75

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
                      out_csv_name='./output/dqn-stats/traffic-sim',
                      reward_fn=my_reward_fn,
                      yellow_time=5,
                      min_green=30,
                      time_to_teleport=2000,
                      use_gui=use_gui,
                      single_agent=True,
                      num_seconds=num_seconds,
                      )


load_model = ask_user("Load model? (y/N) ")
if load_model:
    model = DQN.load('./output/model_saved.zip', print_system_info=True)
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

model.save("./output/model_saved")
print("Model saved to ./output/")
