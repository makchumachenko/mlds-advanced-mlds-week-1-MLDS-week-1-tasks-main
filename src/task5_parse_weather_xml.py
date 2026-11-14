import xml.etree.ElementTree as ET
import csv
from typing import Any


def parse_weather_xml(xml_file: str) -> list[dict[str, Any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
    """

    def to_number(value: str) -> float | int | str:
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return value

    return [
        {child.tag: to_number(child.text) for child in element}
        for element in ET.parse(xml_file).findall("day")
    ]


def save_to_csv(data: list[dict[str, Any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ['Date', 'Temperature', 'Humidity', 'Precipitation']

    try:
        with open(filename, "w", newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=headers)
            writer.writeheader()
            for day in data:
                writer.writerow({header: day[header.lower()] for header in headers})
    except Exception:
        raise IOError


if __name__ == "__main__":
    try:
        # Parse the XML file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        # Save the parsed data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
