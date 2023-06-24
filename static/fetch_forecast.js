// fetch_forecast.js

window.fetchWeatherForecast = function() {

    // Get the start and end hours
    var startHourValue = document.getElementById('start_hour').value;
    var endHourValue = document.getElementById('end_hour').value;

    // Get the GPS coordinates
    var lat = document.getElementById('lat').value;
    var lon = document.getElementById('lon').value;

    // Get the Zip code value unless its null
    var zipCode = null;
    if (document.getElementById('zip_code')) {
        zipCode = document.getElementById('zip_code').value;
    }

    // Prepare the data to be sent
    var data = {};
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
document.addEventListener('load', function() {
    fetchWeatherForecast();
});