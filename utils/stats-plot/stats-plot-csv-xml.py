from os.path import isfile, join
import os
import matplotlib.pyplot as plt
import csv


def extract_info(path_to_files: str, header_title: str, trim: int):

    csv_files_path = [os.path.join(path_to_files, f) for f in os.listdir(
        path_to_files) if isfile(join(path_to_files, f))]

    total_queue_length = {}
    for file_path in csv_files_path:

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            file_name = os.path.split(file_path)[1]
            # extract the number from the file
            file_number = int(file_name.removeprefix(
                'traffic_sim_conn0_ep').removesuffix('.csv'))
            # get the index of the header we're looking for
            header_index = data[0].index(header_title)

            queue_length = 0
            for row in data[1:]:
                queue_length += int(row[header_index])

            # trim big values
            if queue_length <= trim:
                total_queue_length[file_number] = queue_length

    return dict(sorted(total_queue_length.items()))


queue = extract_info(
    '/home/faidz-arante/Documents/sumo-traffic-capstone/output/dqn-stats/',
    '0_queue_length',
    320000,
)

queue_list = list(queue.values())

plt.plot(queue_list)
plt.ylabel('Total Queue Length')
plt.xlabel('Episode')
plt.show()
