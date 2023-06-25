//location.js: This script uses the browser's geolocation API to get the user's current latitude and longitude
// when the 'location-btn' is clicked. The latitude and longitude are then stored in hidden fields in a form.
// Once the location data is fetched, an AJAX request is made to the '/weather_general' endpoint of the Flask app
// to fetch the weather data. The fetched weather data is then displayed in the appropriate UI elements.

document.addEventListener('DOMContentLoaded', function() {

  // This function is called when the Geolocation API fails to get the user's current position.
  // It logs an error message to the console for debugging purposes.
  function handleGpsFailure() {
    console.error("Geolocation is not supported or failed to get the current position.");
  }

  // This function is responsible for fetching the user's location and sending the latitude and longitude to
  // the Flask app to get the weather data.
  function getLocationAndUpdateForm() {
    // Check if Geolocation is supported by the browser
    if (navigator.geolocation) {
        // Use the Geolocation API to get the user's current position
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // Update the hidden lat and lon fields in the form
            document.getElementById('lat').value = latitude;
            document.getElementById('lon').value = longitude;

            // Prepare the data to be sent in the AJAX request. The weather option is set to 'location'
            // and the latitude and longitude values are set to the fetched location data.
            var data = {
//                weather_option: 'location',
                lat: latitude,
                lon: longitude
            };

            // Make an AJAX request to the '/weather' endpoint of the Flask app with the prepared data.
            // The request type is 'POST' and the request data type is JSON.
            $.ajax({
                url: '/weather',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json',
                // The success callback is called when the request is successful. The response from the server is passed to this callback.
                success: function(response) {
                    // Update the 'weather_result' div with the fetched weather data.
                    $('#weather_result').text(response.result);
                    // If there's a photo in the response, update the 'weather_photo' img src and display the photo.
                    if (response.photo) {
                        $('#weather_photo').attr('src', response.photo);
                        $('#weather_photo').show();
                        $('#resultDiv').show();
                    }
                },
                // The error callback is called when the request fails. The error data is passed to this callback.
                error: function(error) {
                    console.log(error);
                    // If the request fails, update the 'weather_result' div with an error message.
                    $('#weather_result').text("An error occurred while fetching the weather forecast.");
                }
            });
        }, function() {
            // Handle location errors here
            handleGpsFailure();
        });
    } else {
        // Geolocation is not supported
        handleGpsFailure();
    }
  }

// This will call getLocationAndUpdateForm function when the button is clicked
document.getElementById('location-btn').addEventListener('click', getLocationAndUpdateForm);

});
