from typing import Any

import requests

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_weather_data() -> dict[str, Any]:
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
        KeyError: If the expected data is not in the API response.
    """
    url = ("https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
           "&daily=temperature_2m_max&timezone=Asia/Tokyo")
    json = requests.get(url).json()
    zipped = dict(zip(*json["daily"].values()))
    maximum = max(zipped.items(), key=lambda x: x[1])
    return dict(zip(['date', 'max_temperature'], maximum))


if __name__ == "__main__":
    try:
        # Fetch the weather data
        weather_data = fetch_weather_data()

        # Save the data to a JSON file
        save_to_json(weather_data, "tokyo_weather.json")

        print("Data successfully saved to tokyo_weather.json")
    except Exception as e:
        print(f"An error occurred: {e}")
