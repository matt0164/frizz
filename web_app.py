# web_app.py serves as the entry point for the Flask application. It imports the necessary modules, sets up
# the Flask app, defines the routes, and handles the logic for retrieving weather data based on zip code
# or location. The routes interact with the HTML templates by rendering them and passing data from the
# Python scripts to be displayed dynamically. Additionally, it interacts with JavaScript files by receiving
# data via AJAX requests and triggering updates on the web page. it interacts with JavaScript files by receiving
# data via AJAX requests and triggering updates on the web page.

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from weather_fetch import get_weather
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
    # Default core hours (from 10am to 3pm)
    start_hour, end_hour = 10, 15

    # Fetch the submitted lat, lon, start_hour, and end_hour if a POST request
    if request.method == "POST":
        # Fetch the submitted lat, lon, start_hour, and end_hour
        data = request.get_json()
        lat = data.get("lat", lat)
        lon = data.get("lon", lon)
        start_hour = data.get("start_hour", start_hour)
        end_hour = data.get("end_hour", end_hour)

    # Get the weather data for the coordinates and the core hours
        weather_data = get_weather(lat, lon, start_hour, end_hour)

    else:
        # If it's a GET request, get the parameters from the URL
        # It can  take latitude, longitude, start hour, and end hour parameters from the URL in a GET request, like
        # this: http://localhost:5000/?lat=40.7128&lon=-74.0060&start_hour=10&end_hour=15.
        lat = request.args.get("lat", default=lat, type=float)
        lon = request.args.get("lon", default=lon, type=float)
        start_hour = request.args.get("start_hour", default=start_hour, type=int)
        end_hour = request.args.get("end_hour", default=end_hour, type=int)

        # Get the weather data for the coordinates and the core hours
        weather_data = get_weather(lat, lon, start_hour, end_hour)

        if weather_data is not None:
            weather_result = weather_data["result"]
            photo = weather_data["photo"]

    # Render the main page with the weather data and random colors
        return render_template("frizz_landing.html", weather_result=weather_result, photo=photo, color1=color1,
                           color2=color2)

#handle the incoming POST request, and call the new get_weather function from weather_fetch.py
# this is an endpoint called /weather that gets the lat long from the data
# in location.js there is a var called data that contains the lat long and start and end hour
#
@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()  # Get data sent to this route

    lat = data.get('lat')  # Get latitude from the data
    lon = data.get('lon')  # Get longitude from the data
    start_hour = data.get('start_hour', 10)  # Default start hour to 10 if not provided
    end_hour = data.get('end_hour', 15)  # Default end hour to 15 if not provided

    # If latitude and longitude are not provided, return an error message
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required.'}), 400

    # Fetch the weather data
    weather_data = get_weather(lat, lon, start_hour, end_hour)

    if weather_data is not None:
        session['weather_result'] = weather_data["result"]
        session['photo'] = weather_data["photo"]
        return jsonify({'result': weather_data["result"], 'photo': weather_data["photo"]}), 200
    else:
        return jsonify({'error': 'No weather data found.'}), 400

if __name__ == '__main__':
    app.run(debug=False)