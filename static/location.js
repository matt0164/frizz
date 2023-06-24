//location.js uses the browsers GPS functionality to get the current lat and long

//ensures code will only run after the DOM is fully ready, which can help avoid errors
// related to trying to access elements before they've been loaded

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

});