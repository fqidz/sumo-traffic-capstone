from pathlib import Path
from pathvalidate import sanitize_filepath
import argparse
import logging


def create_parser(args: list[str] = []):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('args_handler.py')

    # TODO: add subparsers for the scripts inside utils
    parser = argparse.ArgumentParser(
        prog='sumo-traffic-ai',
        description='AI powered traffic light signal control simulation for capstone'
    )
    subparsers = parser.add_subparsers()
    subparsers.required = True

    # Simulation subparser & params
    simulation_parser = subparsers.add_parser(
        'simulate', help='Start simulation')

    simulation_parser.add_argument('-m', '--model', required=True,
                                   metavar='MODEL_PATH', dest='model_path',
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
    if args:
        params = parser.parse_args(args)
    else:
        params = parser.parse_args()

    # TODO: make tests
    # TODO: add logging & research best practices for it
    # Handle file paths

    def check_model(path: Path, train: bool) -> Path:
        path = Path(path)

        if str(path) != sanitize_filepath(str(path)):
            raise AssertionError(
                f"'{str(path)}' is not a valid model name or path.")

        logger.info(f"Ok, '{str(path)}' == '{
                    sanitize_filepath(str(path))}'")

        file_suffix = path.suffix

        # if user specifies a suffix and its anything but '.zip', eg. test.py, foo.bar
        if file_suffix != '.zip' and file_suffix != '':
            raise AssertionError(
                f"'{file_suffix}' is not supported. Only zip files are supported")

        file_stem = path.stem
        zip_name = file_stem + '.zip'
        parent_path = Path(path).parent
        default_path = Path('./output/models/')

        # if no path & suffix is given, eg. model1, 1234, test1
        if str(parent_path) == '.' and not file_suffix:
            # Assume that user wants to point to the default path (./output/models/)
            # and not to a file with no suffix in the current directory.
            default_zip_path = Path(default_path / zip_name)
            # check if file exists
            if default_zip_path.is_file():
                return default_zip_path
            else:
                raise AssertionError(
                    f"'{zip_name}' does not exist in '{default_path}'.")
        else:
            # is a path to zip file, eg. ./foo/bar/balls.zip, test/1234/test.zip
            zip_path = Path(parent_path / zip_name)
            if train:
                # check if dir exists
                if parent_path.is_dir():
                    return zip_path
                else:
                    raise AssertionError(
                        f"'{parent_path}' directory does not exist.")
            else:
                # check if file exists
                if zip_path.is_file():
                    return zip_path
                else:
                    raise AssertionError(
                        f"'{zip_path}' does not exist.")

    params.model_path = check_model(params.model_path, params.train)

    return params


if __name__ == "__main__":
    print(create_parser())
