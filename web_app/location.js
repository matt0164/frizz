function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // Send latitude and longitude to the server using an AJAX request
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/location', true);
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            xhr.send(JSON.stringify({lat: latitude, lng: longitude}));

            xhr.onload = function() {
                if (xhr.status == 200) {
                    location.reload();
                }
            };
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

window.addEventListener('load', function() {
    document.getElementById('location-btn').addEventListener('click', getLocation);
});