import tkinter as tk
import requests
import geocoder
from tkinter import messagebox, PhotoImage
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather_by_zip():
    zip_code = zip_entry.get()
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
            photo = PhotoImage(file="C:\\Users\\matta\\PycharmProjects\\NewFrizzApr23\\goodhair.png")
            result_label.config(image=photo)
            result_label.photo = photo
            humidity_label.config(text=f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph.", font=("Helvetica", 14))
        else:
            photo = PhotoImage(file="C:\\Users\\matta\\PycharmProjects\\NewFrizzApr23\\badhair.png")
            result_label.config(image=photo)
            result_label.photo = photo
            humidity_label.config(text=f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph.", font=("Helvetica", 14))
    else:
        messagebox.showerror("Error", "Could not retrieve weather data. Please try again later.")

def get_weather_by_location():
    g = geocoder.ip('me')
    lat, lon = g.latlng
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
            photo = PhotoImage(file="C:\\Users\\matta\\PycharmProjects\\NewFrizzApr23\\goodhair.png")
            result_label.config(image=photo)
            result_label.photo = photo

            humidity_label.config(text=f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph.", font=("Helvetica", 14))

        else:
            photo = PhotoImage(file="C:\\Users\\matta\\PycharmProjects\\NewFrizzApr23\\badhair.png")
            result_label.config(image=photo)
            result_label.photo = photo

            humidity_label.config(text=f"The humidity is {humidity}% and the temperature is {temperature}°F with a wind speed of {wind_speed} mph.", font=("Helvetica", 14))

root = tk.Tk()
root.title("The Frizz Wiz - The ultimate tool how to wear your hair based on today's weather")
root.geometry("1000x1000")

zip_frame = tk.Frame(root)
zip_frame.pack(pady=20)

zip_label = tk.Label(zip_frame, text="Enter Zip Code:")
zip_label.pack(side="left")

zip_entry = tk.Entry(zip_frame)
zip_entry.pack(side="left")

zip_button = tk.Button(zip_frame, text="Get Weather by Zip Code", command=get_weather_by_zip)
zip_button.pack(side="left", padx=10)

location_button = tk.Button(root, text="Get Weather by Location", command=get_weather_by_location)
location_button.pack(pady=20)

result_frame = tk.Frame(root)
result_frame.pack(pady=20)

result_label = tk.Label(result_frame)
result_label.pack()

humidity_frame = tk.Frame(root)
humidity_frame.pack(pady=20)

humidity_label = tk.Label(humidity_frame, font=("Helvetica", 14))
humidity_label.pack()

temp_frame = tk.Frame(root)
temp_frame.pack(pady=20)

temp_label = tk.Label(temp_frame, font=("Helvetica", 14))
temp_label.pack()

wind_frame = tk.Frame(root)
wind_frame.pack(pady=20)

wind_label = tk.Label(wind_frame, font=("Helvetica", 14))
wind_label.pack()

root.mainloop()