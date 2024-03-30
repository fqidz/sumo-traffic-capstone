from os.path import isfile, join
import os
from pathlib import Path
from sys import prefix
from typing import Union
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import csv


class DataProcessing():
    def __init__(self, headers: list[str], input_path: str, output_path: str, output_file_names: list[str], trim_direction: list[str], trim: list[int], prefix: str = 'traffic-sim_conn0_ep') -> None:
        """
        Args:
            data (dict): the data
            trim (int): cut off point
            direction (str): 'up' or 'down'
        """
        if len(headers) != len(output_file_names):
            raise Exception("headers and output_file_names not same amount")
        self.headers = headers
        self.input_path = input_path
        self.output_path = output_path
        self.output_file_names = output_file_names
        self.trim = trim
        self.trim_direction = trim_direction
        self.data_dicts = []
        self.do_save = False
        self.prefix = prefix

    def extract_info(self) -> list[dict]:

        csv_files_path = [os.path.join(self.input_path, f) for f in os.listdir(
            self.input_path) if (isfile(join(self.input_path, f)) and f.endswith('.csv'))]

        _data_dicts = []
        for header in self.headers:
            data_dict = {}
            for file_path in csv_files_path:

                with open(file_path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)
                    file_name = os.path.split(file_path)[1]
                    # extract the number from the file
                    file_number = int(file_name.removeprefix(
                        self.prefix).removesuffix('.csv'))
                    # get the index of the header we're looking for
                    header_index = data[0].index(header)

                    if header == '0_queue_length':
                        data_value = self.get_queue_length_sum(
                            data, header_index)
                    elif header == 'system_mean_speed':
                        data_value = self.get_mean_speed(data, header_index)
                    else:
                        raise Exception("not implemented")

                    data_dict[file_number] = data_value

            # data_dict = self.trim_values(data_dict)
            _data_dicts.append(dict(sorted(data_dict.items())))

        return _data_dicts

    def get_queue_length_sum(self, data: list, header_index: int) -> float:
        queue_length = 0
        for row in data[1:]:
            queue_length += float(row[header_index])

        return queue_length

    def get_mean_speed(self, data: list, header_index: int) -> float:
        average_speeds = []
        for row in data[1:]:
            average_speeds.append(float(row[header_index]))

        total_average_speed = np.average(average_speeds)

        return float(total_average_speed)

    def trim_values(self, data: dict) -> dict:
        # trim outlier values
        for i, direction in enumerate(self.trim_direction):
            for key, value in data.items():
                if key > 30:
                    if self.trim_direction[i] == 'up':
                        if (value >= self.trim[i]):
                            neighbors_mean = (
                                data[key - 1] + data[key + 1]) / 2
                            data[key] = neighbors_mean
                            print(f"Episode {key} outlier (value of {value} >= {
                                  self.trim[i]}): Adjusted to mean of neighbors ({neighbors_mean})")
                    elif self.trim_direction[i] == 'down':
                        if (value <= self.trim[i]):
                            neighbors_mean = (
                                data[key - 1] + data[key + 1]) / 2
                            data[key] = neighbors_mean
                            print(f"Episode {key} outlier (value of {value} <= {
                                  self.trim[i]}): Adjusted to mean of neighbors ({neighbors_mean})")
                    else:
                        raise Exception(
                            "trim_direction can only be 'up' or 'down'")
        return data

    def save_to_csv(self) -> None:
        for i, data in enumerate(self.data_dicts):
            with open(os.path.join(self.output_path, self.output_file_names[i]), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(list(data.keys()))
                writer.writerow(list(data.values()))
            print(f"Saved {self.headers[i]} to {os.path.join(
                self.output_path, self.output_file_names[i])}")

    def load_csv(self) -> list[dict]:
        loaded_data = []
        for i, file_name in enumerate(self.output_file_names):
            _ = file_name
            file = os.path.join(self.output_path, self.output_file_names[i])
            if isfile(file):
                with open(file, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    data = list(reader)
                    data_dict = {}

                    for i, header in enumerate(data[0]):
                        data_dict[header] = float(data[1][i])

                    loaded_data.append(dict(data_dict))

        return loaded_data

    def prompt_save(self):
        repeat = True
        while repeat:
            save_prompt = input("Save data to csv? (y/N):").lower()
            save_prompt = "".join(save_prompt.split())

            if save_prompt == "y":
                self.do_save = True
                repeat = False
            elif save_prompt == "n" or not save_prompt:
                self.do_save = False
                repeat = False
            else:
                print("Wrong Input")
                print("")
                repeat = True

    def plot(self, dicts: list[dict]):
        data_list: list[list] = []
        for data in dicts:
            data_list.append(list(data.values()))

        fig, axs = plt.subplots(2)
        _ = fig
        axs[0].plot(data_list[0])
        axs[1].plot(data_list[1], color='r')
        axs[0].set_title('Queue Length (No. of Vehicles)')
        axs[1].set_title('Mean Speeds (m/s)')
        axs[0].set_yticks(np.arange(0, 900000, 50000))
        axs[1].set_yticks(np.arange(0.0, 9.0, 0.5))
        for ax in axs:
            ax.grid(visible=True)

        plt.show()

    def run(self):
        self.prompt_save()
        if self.do_save == True:
            self.data_dicts = self.extract_info()
            self.save_to_csv()
        else:
            self.data_dicts = self.load_csv()
        print(self.data_dicts)

        self.plot(self.data_dicts)


process = DataProcessing(
    ['0_queue_length', 'system_mean_speed'],
    '/home/faidz-arante/Documents/sumo-traffic-capstone/output/traffic-stats/',
    '/home/faidz-arante/Documents/sumo-traffic-capstone/output/processed_data/',
    ['queue_length.csv', 'mean_speeds.csv'],
    ['up', 'down'],
    [320000, 6]
)

# Path('/home/faidz-arante/Documents/sumo-traffic-capstone/output/actuated/processed_data/').mkdir(parents=True, exist_ok=True)
#
# process = DataProcessing(
#     ['0_queue_length', 'system_mean_speed'],
#     '/home/faidz-arante/Documents/sumo-traffic-capstone/output/actuated/traffic-stats/',
#     '/home/faidz-arante/Documents/sumo-traffic-capstone/output/actuated/processed_data/',
#     ['queue_length.csv', 'mean_speeds.csv'],
#     ['up', 'down'],
#     [320000, 6],
#     prefix='actuated_actuated'
# )

process.run()
