import csv
import os


class VehicleFlowConverter():
    def __init__(self, csv_files: list[str], vehicle_types: list[str], xml_file: str) -> None:
        self.csv_files = csv_files
        self.vehicle_types = vehicle_types
        self.xml_file = xml_file

    def convert_csv_to_xml(self):
        for i, csv_file in enumerate(self.csv_files):
            vehicle_type = self.vehicle_types[i]
            with open(csv_file, 'r') as csvfile, open(self.xml_file, 'w') as xmlfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Get headers

                for j, row in enumerate(reader):
                    begin, end = row[0], row[1]

                    # Generate unique flow id and route
                    # Skip first two columns
                    for i, flow_id in enumerate(headers[2:]):
                        route = flow_id
                        unique_id = f"{flow_id}{j}"

                        vehs_per_hour = row[i + 2]

                        # Write flow element
                        xmlfile.write(f'<flow id="{unique_id}" type={vehicle_type} begin="{begin}.00" route="{
                                      route}" end="{end}.00" vehsPerHour="{vehs_per_hour}"/>\n')

                xmlfile.write('\n')
