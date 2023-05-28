import logging

from dotenv import load_dotenv
import os

import random

from flask import Flask, render_template, request, jsonify
from web_main import get_weather_by_zip, get_weather_by_location

load_dotenv(dotenv_path="/var/www/frizz/.env")

app = Flask(__name__)

# Enable debug mode temporarily for troubleshooting
app.debug = False

# Set up a logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/www/frizz/logs/frizz.log', level=logging.DEBUG)

def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

@app.route('/location', methods=['POST'])
def location():
    logger.debug('Received request for /location')
    data = request.get_json()
    lat = data['lat']
    lon = data['lng']
    result, photo = get_weather_by_lat_lng(lat, lon)
    return jsonify(result=result, photo=photo)

@app.route("/", methods=["GET", "POST"])
def index():
    logger.debug('Received request for index route')
    result = None
    photo = None
    color1 = random_color()
    color2 = random_color()

    if request.method == "POST":
        weather_option = request.form.get("weather_option")

        if weather_option == "zip_code":
            logger.debug('Weather option is zip_code')
            zip_code = request.form.get("zip_code")
            result, photo = get_weather_by_zip(zip_code)
        elif weather_option == "location":
            logger.debug('Weather option is location')
            result, photo = get_weather_by_location()

    return render_template("frizz_landing.html?v=2", result=result, photo=photo, color1=color1, color2=color2)
