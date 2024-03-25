import csv


def convert_csv_to_xml(csv_file, xml_file):
    """
    Converts a CSV file to XML elements.

    Args:
      csv_file: Path to the CSV file.
      xml_file: Path to the output XML file.
    """
    with open(csv_file, 'r') as csvfile, open(xml_file, 'w') as xmlfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get headers

        # Write XML start tag
        xmlfile.write('<flows>\n')

        for j, row in enumerate(reader):
            begin, end = row[0], row[1]

            # Generate unique flow id and route
            for i, flow_id in enumerate(headers[2:]):  # Skip first two columns
                route = flow_id
                unique_id = f"{flow_id}{j}"

                vehs_per_hour = row[i + 2]

                # Write flow element
                xmlfile.write(f'  <flow id="{unique_id}" begin="{begin}.00" route="{
                              route}" end="{end}.00" vehsPerHour="{vehs_per_hour}"/>\n')

        # Write XML end tag
        xmlfile.write('</flows>')


# Example usage
csv_file = "traffic-veh-hour.csv"
xml_file = "traffic_data.xml"
convert_csv_to_xml(csv_file, xml_file)

print(f"Converted CSV file '{csv_file}' to XML file '{xml_file}'.")
