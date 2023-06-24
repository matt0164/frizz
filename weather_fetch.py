# weather_fetch.py pulls in all of the weather data from an API and does the core logic
# processing, and passes the data to the other modules
import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
API_KEY = os.environ.get("API_KEY")
#print("API key: ", API_KEY) #prints API key if there are issues with it

# Base URL of the OpenWeatherMap API
BASE_URL = "https://api.openweathermap.org/data/3.0/"

def get_weather_by_coordinates_or_zip(data):

    if data.get('weather_option') == 'zip':
        return get_weather_by_zip(data.get('zip_code'), data.get('start_hour'), data.get('end_hour'))
    else:
        return get_weather_by_coordinates(data.get('lat'), data.get('lon'), data.get('start_hour'), data.get('end_hour'))

def get_weather_by_coordinates(lat, lon, start_hour=10, end_hour=15):

    if not isinstance(start_hour, int):  # Check if start_hour is not an integer
        start_hour = 0  # or some other default value

    if not isinstance(end_hour, int):  # Check if end_hour is not an integer
        end_hour = 24  # or some other default value

    # URL for the One Call API
    url = BASE_URL + "onecall?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + API_KEY + "&units=imperial"
    # Print the constructed URL (uncomment if troubleshooting API)
    #print("URL: ", url)

    # Send a GET request to the API
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the JSON data from the response
        weather_data = response.json()

        # Extract the hourly forecast data
        hourly_forecast = weather_data["hourly"]

        # Get the forecast for the core hours of the day (default 10AM - 3PM, but customizable)
        core_day_forecast = hourly_forecast[start_hour:end_hour+1]

        # Define thresholds for high and low humidity and dew point
        high_humidity = 60
        low_humidity = 40
        high_dew_point = 60
        low_dew_point = 40

        # Get the average humidity and dew point during core hours of the day
        avg_humidity = round(sum([forecast["humidity"] for forecast in core_day_forecast]) / len(core_day_forecast), 1)
        avg_dew_point = round(sum([forecast["dew_point"] for forecast in core_day_forecast]) / len(core_day_forecast),1)

        # Determine the forecast based on humidity and dew point
        if avg_humidity > high_humidity:
            if avg_dew_point > high_dew_point:
                photo = "https://images.pexels.com/photos/3768905/pexels-photo-3768905.jpeg"
                result = f"Forecast: High humidity and high dew point. \nAverage humidity: {avg_humidity}%, dew point: {avg_dew_point}°F. \nAdvice: Use a product that contains a film-forming humectant. Apply a leave-in conditioner, then a styling product containing film-forming humectant. Finally, scrunch your hair to help define your curls."
            else:
                photo = "https://images.pexels.com/photos/16210166/pexels-photo-16210166/free-photo-of-a-woman-lying-down.jpeg"
                result = f"Forecast: High humidity and low dew point. \nAverage humidity: {avg_humidity}%, dew point: {avg_dew_point}°F. \nAdvice: Use a product that contains both a film-forming humectant and an emollient. Apply a leave-in conditioner, then a styling product containing both ingredients. Finally, scrunch your hair to help define your curls."
        elif avg_dew_point > high_dew_point:
            photo = "https://images.pexels.com/photos/3768905/pexels-photo-3768905.jpeg"
            result = f"Forecast: Low humidity and high dew point. \nAverage humidity: {avg_humidity}%, dew point: {avg_dew_point}°F. \nAdvice: Use a product that contains an emollient. Apply a leave-in conditioner, then a styling product containing emollient. Finally, diffuse your hair or air dry it with a diffuser attachment to help add volume."
        else:
            photo = "https://images.pexels.com/photos/16210166/pexels-photo-16210166/free-photo-of-a-woman-lying-down.jpeg"
            result = f"Forecast: Low humidity and low dew point. \nAverage humidity: {avg_humidity}%, dew point: {avg_dew_point}°F. \nAdvice: No special styling is required. Keep your hair protected from the sun and wind, apply styling products while your hair is still damp and avoid over-styling."

        return {
            "photo": photo,
            "result": result
        }
    else:
        # If the GET request is unsuccessful, print the status code
        print("Error:", response.status_code)
        # error_message = "Could not fetch the weather data."
        default_photo = "https://images.pexels.com/photos/1049687/pexels-photo-1049687.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        return {"result": error_message, "photo": default_photo}

import logging

def get_weather_by_zip(zip_code, start_hour=9, end_hour=15):

    if not isinstance(start_hour, int):  # Check if start_hour is not an integer
        start_hour = 0  # or some other default value

    if not isinstance(end_hour, int):  # Check if end_hour is not an integer
        end_hour = 24  # or some other default value

    # URL for the Weather API
    url = BASE_URL + "weather?zip=" + zip_code + "&appid=" + API_KEY + "&units=imperial"
    logging.info(f'Fetching weather data from: {url}')

    # Print the constructed URL
    print("Geo URL: ", url)

    # Send a GET request to the API
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the JSON data from the response
        weather_data = response.json()
        logging.info(f'Received weather data: {weather_data}')

        # Extract the coordinates from the weather data
        lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]

        # Get the weather forecast for the coordinates and the core hours
        return get_weather_by_coordinates(lat, lon, start_hour, end_hour)
    else:
        # If the GET request is unsuccessful, print the status code
        logging.error(f"Error {response.status_code} when fetching weather data. Full response: {response.text}")
        return {
            "photo": None,
            "result": f"Could not fetch the weather data. Error: {response.status_code}"
        }
