import csv
from typing import TextIO
from .task3_complex_weather_analysis import analyze_daily_weather
import pandas as pd

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: list[dict[str, any]]) -> dict[str, float]:
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    analyses = [analyze_daily_weather(day) for day in data]
    df = pd.DataFrame(analyses)
    return {
        "average_max_temp": df['max_temperature'].mean().item(),
        "average_min_temp": df['min_temperature'].mean().item(),
        "total_precipitation": df['precipitation'].sum().item(),
        "average_wind_speed": df['wind_speed'].mean().item(),
        "average_humidity": df['humidity'].mean().item(),
        "hot_days": df['is_hot_day'].sum().item(),
        "windy_days": df['is_windy_day'].sum().item(),
        "rainy_days": df['is_rainy_day'].sum().item()
    }


def export_to_csv(data: list[dict[str, any]], file: str | TextIO) -> None:
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed", "Humidity",
               "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day"]
    analyses = [analyze_daily_weather(day) for day in data]


    def write_data(writer: csv.DictWriter) -> None:
        """Helper function to write rows to the CSV.
        
        Args:
            writer (csv.DictWriter): The CSV writer object.
        """
        writer.writeheader()
        for analysis in analyses:
            writer.writerow({
                header: analysis[header.replace(' ', '_').lower()]
                for header in headers
                })

    if isinstance(file, str):
        with open(file, "w", newline="") as fp:
            write_data(csv.DictWriter(fp, fieldnames=headers))
    else:
        write_data(csv.DictWriter(file, fieldnames=headers))


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Summarize the weather data
        summary = summarize_weather_data(weather_data['daily'])

        # Print the summary for verification
        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Export the summarized data to a CSV file
        export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")
