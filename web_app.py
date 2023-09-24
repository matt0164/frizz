from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from weather_fetch import get_weather_by_zip, get_weather_by_coordinates, get_weather_by_coordinates_or_zip
import logging
import random
import sys
from dotenv import load_dotenv
import os

from datetime import datetime
from dateutil.parser import parse

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_if_not_found")

# Enable CORS (Cross Origin Resource Sharing)
CORS(app)

# Generate a random color
def random_color():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

# Define the route for the home page ("/")
@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize variables for weather results and photo
    weather_result = session.get('weather_result', None)
    photo = session.get('photo', None)
    # Generate random colors
    color1 = random_color()
    color2 = random_color()

    # Default lat/lon (for New York, NY); You might want to update this
    lat, lon = 40.7128, -74.0060
    # Default core hours (from 9am to 3pm)
    start_hour, end_hour = 9, 15

    # Check if a POST request has been made
    if request.method == "POST":
        # Fetch the submitted lat, lon, start_hour, and end_hour
        data = request.get_json()
        lat = data.get("lat", lat)
        lon = data.get("lon", lon)
        start_hour = data.get("start_hour", start_hour)
        end_hour = data.get("end_hour", end_hour)
        zip_code = data.get("zip_code")

        weather_data = None

        if lat and lon:
            # Get the weather data for the coordinates and the core hours
            weather_data = get_weather_by_coordinates(lat, lon, start_hour, end_hour)
        elif zip_code:
            # Get the weather data for the zip code and the core hours
            weather_data = get_weather_by_zip(zip_code, start_hour, end_hour)

        if weather_data is not None:
            weather_result = weather_data["result"]
            photo = weather_data["photo"]

    # Render the main page with the weather data and random colors
    return render_template("frizz_landing.html", weather_result=weather_result, photo=photo, color1=color1, color2=color2)

#handle the incoming POST request, and call the new get_weather_by_coordinates_or_zip() function from weather_fetch.py
@app.route('/weather_general', methods=['POST'])
def get_weather():
    data = request.get_json()

    if 'start_hour' in data:
        start_hour_str = data['start_hour']
    else:
        # Handle the error, perhaps by assigning a default value or logging an error message
        start_hour_str = "default_value"

    data = request.get_json()
    start_hour_str = data.get('start_hour')
    end_hour_str = data.get('end_hour')

    result = get_weather_by_coordinates_or_zip(data)
    return jsonify(result)

# Define the route for fetching weather data
@app.route('/weather', methods=['POST'])
def weather():
    # The function to process the weather request
    data = request.get_json()  # Get data sent to this route
    lat = data.get('lat', None)  # Get lat if it exists, if not, set it to None
    lon = data.get('lon', None)  # Get lon if it exists, if not, set it to None
    result, photo = None, None  # Set default values

    if lat and lon:
        # Call get_weather_by_coordinates() if lat and lon are provided
        result, photo = get_weather_by_coordinates(lat, lon)
        session['weather_result'] = result  # Save weather result in session
        session['photo'] = photo  # Save photo in session
    else:
        result = 'Error: Location not found.'  # Set error message

    # Return results
    return jsonify({'result': result, 'photo': photo})

if __name__ == "__main__":
    print(sys.version)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.run(debug=False)
