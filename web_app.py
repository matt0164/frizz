from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from weather_fetch import get_weather_by_zip, get_weather_by_coordinates, get_weather_by_coordinates_or_zip
import logging
import random
import sys
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Session key from environment variable
SESSION_KEY = os.environ.get("SESSION_KEY")

def create_app():
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
        return render_template("frizz_landing.html", weather_result=weather_result, photo=photo, color1=color1,
                               color2=color2)

    # handle the incoming POST request, and call the new get_weather_by_coordinates_or_zip() function from weather_fetch.py
    @app.route('/weather_general', methods=['POST'])
    def get_weather():
        data = request.get_json()
        result = get_weather_by_coordinates_or_zip(data)
        return jsonify(result)

    # Define the route for fetching weather data
    @app.route('/weather', methods=['POST'])
    def weather():
        # The function to process the weather request
        data = request.get_json()  # Get data sent to this route
        weather_option = data.get('weather_option')  # Get the weather_option from the data

        # If the weather_option is 'zip'
        if weather_option == 'zip':
            zip_code = data.get('zip_code')  # Get the zip code from the data
            # If the zip code is not provided, return an error message
            if not zip_code:
                return jsonify({'error': 'Zip code is required.'}), 400
            # If the zip code is provided, fetch the weather data
            weather_data = get_weather_by_zip(zip_code)
            return jsonify(weather_data)

        # If the weather_option is 'location'
        elif weather_option == 'location':
            lat = data.get('lat')  # Get latitude from the data
            lon = data.get('lon')  # Get longitude from the data

            # If latitude and longitude are not provided, return an error message
            if not lat or not lon:
                return jsonify({'error': 'Latitude and longitude are required.'}), 400

            # If latitude and longitude are provided, fetch the weather data
            weather_data = get_weather_by_coordinates(lat, lon)
            return jsonify(weather_data)

        else:
            return jsonify({'error': 'Invalid weather option.'}), 400

    # Define the route for fetching location data
    @app.route('/location', methods=['POST'])
    def location():
        data = request.get_json()  # gets the JSON data sent by the JavaScript
        lat = data.get("lat")
        lon = data.get("lon")
        weather_option = data.get('weather_option')  # Get the weather_option from the data

        # Default core hours (from 9am to 3pm)
        start_hour, end_hour = 9, 15

        if weather_option == "location":
            if lat and lon:
                # Get the weather data for the coordinates and the core hours
                weather_data = get_weather_by_coordinates(lat, lon, start_hour, end_hour)
                if weather_data is not None:
                    session['weather_result'] = weather_data["result"]
                    session['photo'] = weather_data["photo"]
            else:
                return jsonify({'error': 'Latitude and longitude are required.'}), 400
        else:
            return jsonify({'error': 'Invalid weather option.'}), 400

        return redirect(url_for('index'))

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
