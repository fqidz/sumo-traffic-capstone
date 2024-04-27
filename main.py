from sumo_rl import SumoEnvironment
from stable_baselines3.dqn.dqn import DQN
from pathlib import Path
from utils.main_utils import MyObservationFunction, my_reward_fn
import argparse


# TODO: put in new dir if dir exists
output_path = Path('./output/')
models_path = output_path / 'models'

# get all model names from models_path; without the .zip
model_names = [file.stem for file in models_path.glob('**/*.zip')]


# TODO: add subparsers for the scripts inside utils
parser = argparse.ArgumentParser(
    prog='sumo-traffic-ai',
    description='AI powered traffic light simulation\n for capstone'
)
parser.add_argument('-m', '--model', required=True,
                    metavar='MODEL_NAME', choices=model_names, dest='model_name',
                    help="Name of DQN model to be loaded/saved. Defaults to './models' directory")

# TODO: allow to pass in paths
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-l', '--load', action='store_true',
                    help='Load model')
action.add_argument('-s', '--save', action='store_true',
                    help='Save model')

parser.add_argument('-g', '--gui', required=False, action='store_true',
                    help='Use sumo-gui instead of sumo')
parser.add_argument('-c', '--object-detection', required=False, action='store_true',
                    help='Use YOLO object detection and enable camera')


# get args from parser
args = parser.parse_args()

traffic_stats_path = output_path / 'traffic-stats' / args.model_name
logs_path = output_path / 'logs' / args.model_name

print(f'models path: {models_path}')
print(f'traffic stats path: {traffic_stats_path}')
print(f'logs path: {logs_path}')

# make sure paths exist
Path(models_path).mkdir(parents=True, exist_ok=True)
Path(traffic_stats_path).mkdir(parents=True, exist_ok=True)
Path(logs_path).mkdir(parents=True, exist_ok=True)

num_seconds = 43500
delta_time = 10
# total seconds divided by delta time (time it takes for ai to take action)
agent_steps_per_episode = -(-num_seconds // delta_time)
episodes = 70


if args.object_detection:
    # use empty route file
    route_file = './sumo-things/only_routes.rou.xml'
    routes = [
        # to use for spawning cars for object detection
        "e_to_e", "e_to_n",
        "e_to_s", "e_to_w",
        "n_to_e", "n_to_n",
        "n_to_s", "n_to_w",
        "s_to_e", "s_to_n",
        "s_to_s", "s_to_w",
        "w_to_e", "w_to_n",
        "w_to_s", "w_to_w",
    ]
else:
    # use route file with trips
    route_file = './sumo-things/main.rou.xml'
    object_detection = False
    routes = []


env = SumoEnvironment(net_file='./sumo-things/net.net.xml',
                      route_file=route_file,
                      routes=routes,
                      out_csv_name='./output/traffic-stats/traffic-sim-model4',
                      reward_fn=my_reward_fn,
                      delta_time=delta_time,
                      yellow_time=4,
                      min_green=10,
                      time_to_teleport=2000,
                      use_gui=args.gui,
                      single_agent=True,
                      num_seconds=num_seconds,
                      observation_class=MyObservationFunction,
                      object_detection=args.object_detection,
                      use_cam=args.gui,
                      )


if args.load:
    # get path of selected model
    selected_model_path = list(models_path.glob(f'**/{args.model_name}.zip'))

    if len(selected_model_path) > 1:
        raise ValueError(
            f'Got more than 1 model: models({selected_model_path})')

    print(f'Running model from: {selected_model_path}')

    model = DQN.load(str(selected_model_path[0]), print_system_info=True)
    model.set_env(env=env)
    model.learn(
        total_timesteps=agent_steps_per_episode * episodes, callback=None, reset_num_timesteps=False)

elif args.save:
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
    saved_model_path = models_path / args.model_name
    model.save(saved_model_path)
    print(f"Model saved to {saved_model_path}")
