# import argparse
#
# parser = argparse.ArgumentParser(
#     prog='sumo-traffic-ai',
#     description='AI powered traffic light simulation\n for capstone'
# )
# # TODO: get models names as choices from ./models/
# parser.add_argument('-m', '--model', required=True,
#                     metavar='MODEL_NAME',
#                     help="Name of DQN model to be loaded/saved. Defaults to './models' directory")
#
# # TODO: allow to pass in paths
# action = parser.add_mutually_exclusive_group(required=True)
# action.add_argument('-l', '--load', action='store_true',
#                     help='Load model')
# action.add_argument('-s', '--save', action='store_true',
#                     help='Save model')
#
# parser.add_argument('-g', '--gui', required=False, action='store_true',
#                     help='Use sumo-gui instead of sumo')
# parser.add_argument('-c', '--object-dection', required=False, action='store_true',
#                     help='Use YOLO object detection and enable camera')
#
#
# args = parser.parse_args()
# print(args)
from pathlib import Path
output_path = Path('./output/')
models_path = output_path / 'models'
# TODO: put in new dir if dir exists

# get all model names from models_path
model_names = [file.stem for file in models_path.glob('**/*.zip')]

print(list(model_names))
