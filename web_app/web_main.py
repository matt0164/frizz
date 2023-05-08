import os
import ipinfo
import requests
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

load_dotenv()

API_KEY = os.environ.get("API_KEY")
OPENCAGE_API_KEY = os.environ.get("OPENCAGE_API_KEY")
IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)


def get_weather_by_zip(zip_code):
    url = BASE_URL + "zip=" + zip_code + "&appid=" + API_KEY + "&units=imperial"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        humidity = weather_data["main"]["humidity"]
        temperature = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]

        humidity = round(humidity)
        temperature = round(temperature)
        wind_speed = round(wind_speed)

        if humidity < 50 and wind_speed < 10:
           photo = "https://images.pexels.com/photos/3048715/pexels-photo-3048715.jpeg"
           result = f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph. It's a great hair day and you can wear it any way you like!"
        else:
           photo = "https://images.pexels.com/photos/3768905/pexels-photo-3768905.jpeg"
           result = f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph. It's a bad hair day. Be careful!"

        return result, photo

    else:
        return None, None, "Could not retrieve weather data. Please try again later."


def get_weather_by_location():
        print("get_weather_by_location() called")
        return None, None

def get_lat_lon_by_city(city):
    results = geocoder.geocode(city)
    if results:
        lat = results[0]["geometry"]["lat"]
        lon = results[0]["geometry"]["lng"]
        return lat, lon
    return None, None

def get_weather_by_lat_lng(lat, lon):
    url = BASE_URL + "lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + API_KEY + "&units=imperial"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        humidity = weather_data["main"]["humidity"]
        temperature = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]

        humidity = round(humidity)
        temperature = round(temperature)
        wind_speed = round(wind_speed)

        if humidity < 50 and wind_speed < 10:
            photo = "https://images.pexels.com/photos/3048715/pexels-photo-3048715.jpeg"
            result = f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph. It's a great hair day and you can wear it any way you like!"
        else:
            photo = "https://images.pexels.com/photos/3768905/pexels-photo-3768905.jpeg"
            result = f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph. It's a bad hair day. Be careful!"

        return result, photo


def get_location():
    print("get_location() called")
    handler = ipinfo.getHandler(access_token=IPINFO_TOKEN)
    details = handler.getDetails()
    lat = details.latitude
    lon = details.longitude
    city = details.city
    return city
