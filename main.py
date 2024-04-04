import os
from sumo_rl import SumoEnvironment
from stable_baselines3.dqn.dqn import DQN
from pathlib import Path
from utils.main_utils import MyObservationFunction, my_reward_fn, ask_user

model_name_path = input('Model Name: ')
model_name = model_name_path + '.zip'

output_path = './output/'
models_path = os.path.join(output_path, 'models/')
traffic_stats_path = os.path.join(
    output_path, 'traffic-stats/', model_name_path + '/')
logs_path = os.path.join(output_path, 'logs/', model_name_path + '/')

print(f'models path: {models_path}')
print(f'traffic stats path: {traffic_stats_path}')
print(f'logs path: {logs_path}')

Path(models_path).mkdir(parents=True, exist_ok=True)
Path(traffic_stats_path).mkdir(parents=True, exist_ok=True)
Path(logs_path).mkdir(parents=True, exist_ok=True)

num_seconds = 43500
delta_time = 10
# total seconds divided by delta time (time it takes for ai to take action)
agent_steps_per_episode = -(-num_seconds // delta_time)
episodes = 70


use_gui = ask_user("Use GUI? (y/N) ")
use_object_detection = ask_user("Object detection mode?")

if use_object_detection:
    route_file = './sumo-things/only_routes.rou.xml'
else:
    route_file = './sumo-things/main.rou.xml'

routes = [
    "e_to_e", "e_to_n",
    "e_to_s", "e_to_w",
    "n_to_e", "n_to_n",
    "n_to_s", "n_to_w",
    "s_to_e", "s_to_n",
    "s_to_s", "s_to_w",
    "w_to_e", "w_to_n",
    "w_to_s", "w_to_w",
]
vehicle_types = [
    "BUS",
    "TRUCK",
    "PASSENGER",
]

env = SumoEnvironment(net_file='./sumo-things/net.net.xml',
                      route_file=route_file,
                      routes=routes,
                      vehicle_types=vehicle_types,
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
    selected_model_path = os.path.join(models_path, model_name)
    print(f'Running model from: {selected_model_path}')

    model = DQN.load(selected_model_path, print_system_info=True)
    model.set_env(env=env)
    model.learn(
        total_timesteps=agent_steps_per_episode * episodes, callback=None, reset_num_timesteps=False)
else:
    save_model_name = input("Save model as: ")
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
        tensorboard_log=logs_path
    )
    model.learn(
        total_timesteps=agent_steps_per_episode * episodes, log_interval=1, callback=None)
    saved_model_path = os.path.join(models_path, save_model_name)
    model.save(saved_model_path)
    print(f"Model saved to {saved_model_path}")
