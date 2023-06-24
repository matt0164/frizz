//fetch_forecast.js: This script fetches the weather forecast data from a Flask app based on either
//GPS coordinates or a Zip code. The forecast time period is also passed to the Flask app.
//Once the weather forecast is fetched, it is displayed in the 'weather_result' div.
//If there is an associated photo, it is also displayed in the 'weather_photo' div. If there is an error
//in fetching the weather forecast, an error message is displayed in the 'weather_result' div.

window.fetchWeatherForecast = function() {

    // Get the GPS coordinates unless they are null
    var lat = null;
    var lon = null;
    if (document.getElementById('lat')) {
        lat = document.getElementById('lat').value;
    }
    if (document.getElementById('lon')) {
        lon = document.getElementById('lon').value;
    }

    // Get the Zip code value unless its null
    var zipCode = null;
    if (document.getElementById('zip_code')) {
        zipCode = document.getElementById('zip_code').value;
    }

    // Prepare the data to be sent
    var data = {};

    // Get the start and end hours
    var startHourValue = document.getElementsByClassName('slider-time')[0].innerHTML;
    var endHourValue = document.getElementsByClassName('slider-time2')[0].innerHTML;

    if(zipCode) {
        data.weather_option = 'zip';
        data.zip_code = zipCode;
    } else if(lat && lon) {
        data.weather_option = 'location';
        data.lat = lat;
        data.lon = lon;
    }
    data.start_hour = startHourValue;
    data.end_hour = endHourValue;

    // Set up the URL to your Flask app's endpoint
    var url = '/weather_general';

    // Fetch the weather forecast from your Flask app
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(function(response) {
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    }).then(function(json) {
        // Update the forecast and advice
        document.getElementById('weather_result').innerText = json.result;

        //test to see if the json.photo is providing the correct URL
        console.log(json.photo);

        // If there's a photo, update the photo src and display the photo
        if (json.photo) {
            document.getElementById('weather_photo').src = json.photo;
            document.getElementById('weather_photo').style.display = 'block';
        }

        // Make the resultDiv visible
        document.getElementById('resultDiv').style.display = 'block';

    }).catch(function() {
        document.getElementById('weather_result').innerText = "An error occurred while fetching the weather forecast.";
    });
}

// Ensuring the function is called only after the DOM has loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchWeatherForecast();
});
