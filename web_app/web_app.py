import random

from flask import Flask, render_template, request
from web_main import get_weather_by_zip, get_weather_by_location

app = Flask(__name__)

def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    photo = None
    color1 = random_color()
    color2 = random_color()

    if request.method == "POST":
        weather_option = request.form.get("weather_option")

        if weather_option == "zip_code":
            zip_code = request.form.get("zip_code")
            result, photo = get_weather_by_zip(zip_code)
        elif weather_option == "location":
            result, photo = get_weather_by_location()

    return render_template("index.html", result=result, photo=photo, color1=color1, color2=color2)

if __name__ == "__main__":
    app.run(debug=True)