const fetchWeatherForecast = async () => {
    // Get the form data
    const lat = document.getElementById('lat').value;
    const lon = document.getElementById('lon').value;

    // Create the request data
    const data = {
        weather_option: 'location',
        lat: lat,
        lon: lon
    };

    // Send the request to the server
    const response = await fetch('/weather_general', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    // Process the response
    if (response.ok) {
        const weatherData = await response.json();
        // Update the page with the new weather data
    } else {
        // Handle the error
    }
};
