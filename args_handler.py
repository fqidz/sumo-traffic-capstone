from pathlib import Path
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('args_handler.py')


def create_parser():

    # TODO: add subparsers for the scripts inside utils
    parser = argparse.ArgumentParser(
        prog='sumo-traffic-ai',
        description='AI powered traffic light signal control simulation for capstone'
    )
    subparsers = parser.add_subparsers()

    # Simulation subparser & params
    simulation_parser = subparsers.add_parser(
        'simulate', help='Start simulation')

    simulation_parser.add_argument('-m', '--model', required=True,
                                   metavar='MODEL_PATH', dest='model_name',
                                   help="""Path to load/save model .zip file. Looks through
                                           './output/models/' if only model name is passed. 
                                           Loads model by default. Use '--train' to train/save 
                                           model to path instead""")
    simulation_parser.add_argument('-t', '--train', action='store_true',
                                   help='Option to train & save model')
    simulation_parser.add_argument('-g', '--gui', required=False, action='store_true',
                                   help='Option to use sumo-gui instead of sumo')
    simulation_parser.add_argument('-c', '--object-detection', required=False, action='store_true',
                                   help='Option to enable camera and YOLO object detection')

    # get args from parser
    params = parser.parse_args()

    # Handle errors
    model_path = Path(params.model_name)

    def check_model(path: Path, start: bool = True):

        logger.info(f"Checking if '{path}' is a .zip file")
        if path.suffix is '.zip':
            logger.info(f"Yes, '{path}' is a .zip file")
            logger.info(f"Checking if '{path}' exists")
            if path.is_file():
                logger.info(f"Yes, '{path}' exists")
                return
            elif not path.is_file() and start:
                logger.info(f"No, '{path}' doesn't exist")
                logger.info(f"Checking '{path}' in ./output/models/")
                check_model(path, False)
        elif path.suffix is not '.zip' and start:
            logger.info(f"No, '{path}' is not a zip file")
            # logger.info(f"Appending '.zip' to '{path}'")

            # default_path = Path(f'./output/models/{path}.zip')

            logger.info(f"Checking '{path}.zip' in ./output/models/")
            check_model(Path(f'{path}.zip'), False)
        else:
            raise FileNotFoundError()

    # def check_model(path: Path):
    #     logger.info(f"Checking if '{path}' is a file")

    #     if not path.is_file():
    #         logger.info(f"Checking if '{path}' is a .zip file")

    #         if not path.suffix == '.zip':
    #             logger.info(f"'{path}' is not a .zip file")
    #             new_path = Path(f'{path}.zip')
    #             check_model(new_path)
    #             raise AssertionError(f'{model_path.name} is not a file')

    #     logger.info(f"Ok, '{path}' is a file")

    # if model_path.is_file():
    #     if not model_path.suffix == '.zip':
    #         raise AssertionError(f'{model_path.name} is not a zip file')
    # else:
    #     # check if file is in ./output/models
    #     model_default_path = Path(f'./output/models/{params.model_name}.zip')
    #     if model_default_path.is_file():
    #         if not model_default_path.suffix == '.zip':
    #             raise FileNotFoundError(f'')
    #         return params, model_default_path
    #     raise FileNotFoundError(
    #         f"Model file '{model_path}' and '{model_default_path}' not found.\nUse '--train' if you want to train/save model.")
    check_model(model_path)

    return params


if __name__ == "__main__":
    print(create_parser())
    # # TODO: put in new dir if dir exists
    # output_path = Path('./output/')
    # models_path = output_path / 'models'
    # traffic_stats_path = output_path / 'traffic-stats' / params.model_name
    # logs_path = output_path / 'logs' / params.model_name

    # print(f'models path: {models_path}')
    # print(f'traffic stats path: {traffic_stats_path}')
    # print(f'logs path: {logs_path}')

    # # make sure paths exist
    # Path(models_path).mkdir(parents=True, exist_ok=True)
    # Path(traffic_stats_path).mkdir(parents=True, exist_ok=True)
    # Path(logs_path).mkdir(parents=True, exist_ok=True)
