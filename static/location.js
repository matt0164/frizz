//location.js: This script uses the browser's geolocation API to get the user's current latitude and longitude
// when the 'location-btn' is clicked. The latitude and longitude are then stored in hidden fields in a form
//and the fetchWeatherForecast function from the fetch_forecast.js script is called.

document.addEventListener('DOMContentLoaded', function() {

    function getLocationAndUpdateForm() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Update the hidden lat and lon fields in the form
                document.getElementById('lat').value = latitude;
                document.getElementById('lon').value = longitude;

                // Call the weather forecast fetch function
                window.fetchWeatherForecast();  // Use window object
            }, function() {
                // Handle location errors here
                handleGpsFailure();
            });
        } else {
            // Geolocation is not supported
            handleGpsFailure();
        }
    }

window.addEventListener('load', function() {
    document.getElementById('location-btn').addEventListener('click', getLocationAndUpdateForm);
});

// Check if the slider elements exist before adding the event listeners
    if (document.getElementById('start_hour_slider')) {
        document.getElementById('start_hour_slider').addEventListener('change', fetchWeatherForecast);
    }
    if (document.getElementById('end_hour_slider')) {
        document.getElementById('end_hour_slider').addEventListener('change', fetchWeatherForecast);
    }

    // Call fetchWeatherForecast() initially to fetch the weather forecast once the DOM is loaded
    fetchWeatherForecast();

});