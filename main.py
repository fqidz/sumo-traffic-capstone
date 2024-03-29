from sumo_rl import SumoEnvironment
from stable_baselines3.dqn.dqn import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
from pathlib import Path
import numpy as np


# num_seconds = 43200
num_seconds = 43500
agent_steps = -(-num_seconds // 5)
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

Path("./output/dqn-stats/").mkdir(parents=True, exist_ok=True)

env = SumoEnvironment(net_file='./sumo-things/net.net.xml',
                      route_file='./sumo-things/main.rou.xml',
                      out_csv_name='./output/dqn-stats/traffic_sim_new_test',
                      reward_fn=my_reward_fn,
                      yellow_time=4,
                      time_to_teleport=2000,
                      use_gui=use_gui,
                      single_agent=True,
                      num_seconds=num_seconds,
                      )

Path("./output/logs/").mkdir(parents=True, exist_ok=True)
Path("./output/model_checkpoints/").mkdir(parents=True, exist_ok=True)


load_model = ask_user("Load model? (y/N) ")
if load_model:
    model = DQN.load('./output/model_saved.zip', print_system_info=True, env=env,
                     custom_objects={'lr_schedule': 0.0, 'exploration_schedule': 0.0})
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

    # if load_model:
    #     model.load('./output/model_checkpoints/traffic_sim_1957500_steps.zip', env=env)
    #     model.load_replay_buffer(
    #         './output/model_checkpoints/traffic_sim_replay_buffer_1957500_steps.pkl')
    #     print("checkpoint loaded")

checkpoint_callback = CheckpointCallback(
    save_freq=agent_steps * 5,
    save_path='./output/model_checkpoints/',
    name_prefix="traffic_sim",
    save_replay_buffer=True,
    save_vecnormalize=True,
    verbose=2,
)

model.learn(
    total_timesteps=agent_steps * episodes, log_interval=1, callback=checkpoint_callback)
model.save("./output/model_saved")
print("Model saved to ./output/")
