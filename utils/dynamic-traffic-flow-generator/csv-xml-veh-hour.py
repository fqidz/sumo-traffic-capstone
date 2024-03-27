import csv
import os


class VehicleFlowConverter():
    def __init__(self, csv_files: list[str], vehicle_types: list[str], xml_file: str) -> None:
        self.csv_files = csv_files
        self.vehicle_types = vehicle_types
        self.xml_file = xml_file

    def convert_csv_to_xml(self):
        flow_data: dict[int, list] = {}
        count = 0
        for i, csv_file in enumerate(self.csv_files):
            vehicle_type = self.vehicle_types[i]
            with open(csv_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Get headers

                for j, row in enumerate(reader):
                    begin, end = int(row[0]), int(row[1])

                    # Generate unique flow id and route
                    # Skip first two columns
                    for i, flow_id in enumerate(headers[2:]):
                        route = flow_id
                        unique_id = f"{flow_id}{j}"

                        vehs_per_hour = row[i + 2]

                        # Write flow element
                        # xmlfile.write(f'    <flow id="{vehicle_type}{unique_id}" type="{vehicle_type}" begin="{begin}.00" route="{
                        #               route}" end="{end}.00" vehsPerHour="{vehs_per_hour}"/>\n')
                        flow_data[count] = [unique_id,
                                            vehicle_type,
                                            begin,
                                            route,
                                            end,
                                            vehs_per_hour
                                            ]
                        count += 1
        flow_data = {k: v for k, v in sorted(
            flow_data.items(), key=lambda x: x[1][2])}

        flow_data_list = list(flow_data.values())

        with open(self.xml_file, 'w') as xmlfile:
            for i in flow_data_list:
                xmlfile.write(f'    <flow id="{i[1]}{i[0]}" type="{i[1]}" begin="{i[2]}.00" route="{
                              i[3]}" end="{i[4]}.00" vehsPerHour="{i[5]}"/>\n')

        print(f'Wrote to {self.xml_file}')


gen = VehicleFlowConverter(
    ['passenger-density.csv', 'truck-density.csv'],
    ['PASSENGER', 'TRUCK'],
    'traffic_data.xml'
)

gen.convert_csv_to_xml()
