from typing import Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(day: dict[str, Any], temp_threshold: float = 30, 
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    analysis = {
        "is_hot_day": day['max_temperature'] > temp_threshold,
        "temperature_swing": day['max_temperature'] - day['min_temperature'],
        "is_windy_day": day['wind_speed'] > wind_threshold,
        "is_uncomfortable_day": day['humidity'] > humidity_threshold,
        "is_rainy_day": day['precipitation'] > 0
    }
    return day | analysis


def generate_daily_report(analysis: dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    return (f"Date: {analysis['date']}\n"
        + f"Weather: {analysis['weather_description']}\n"
        + f"Temperature: Max {analysis['max_temperature']}°C, Min {analysis['min_temperature']}°C (Swing: {analysis['temperature_swing']}°C)\n"
        + "It was a hot day.\n" * analysis['is_hot_day']
        + "It was a windy day.\n" * analysis['is_windy_day']
        + ("It was a rainy day." if analysis['is_rainy_day'] else "There was no precipitation."))


def summarize_weather_analysis(analyses: list[dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    report = [generate_daily_report(analysis) for analysis in analyses]
    metrics = ('max_temperature', 'wind_speed', 'humidity', 'precipitation')
    values = (
        value
        for metric in metrics
        for value in find_max_day(analyses, metric)
        )
    report.append(
        "Weather Summary:\n"
        "Hottest day: {} with a maximum temperature of {}°C\n"
        "Windiest day: {} with wind speeds of {} km/h\n"
        "Most humid day: {} with a humidity level of {}%\n"
        "Rainiest day: {} with {} mm of precipitation"
        .format(*values)
    )
    return "\n\n".join(report)


def find_max_day(analyses: list[dict[str, Any]], metric: str) -> tuple[str, int | float]:
    day = ""
    value = 0
    for analysis in analyses:
        if analysis[metric] > value:
            day = analysis['date']
            value = analysis[metric]
    return day, value


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")
