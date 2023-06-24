// sliders.js

window.updateHourDisplay = function(hourInputId, hourDisplayId) {
    // Convert the 24-hour format to AM/PM format
    var hour = document.getElementById(hourInputId).value;
    var ampm = hour >= 12 ? 'PM' : 'AM';
    hour = hour % 12;
    hour = hour ? hour : 12;  // the hour '0' should be '12'

    // Fetch the current date
    var date = new Date();

    // Display the date and hour
    document.getElementById(hourDisplayId).innerText = (date.getMonth() + 1) + '/' + date.getDate() + '/' + date.getFullYear() + ' ' + hour + ':00 ' + ampm;
}

// Call updateHourDisplay function initially for 'start_hour' and 'end_hour'
updateHourDisplay('start_hour', 'start_hour_display');
updateHourDisplay('end_hour', 'end_hour_display');

// Add event listeners for the input changes
document.getElementById('start_hour').addEventListener('input', function() {
    updateHourDisplay('start_hour', 'start_hour_display');
});

document.getElementById('end_hour').addEventListener('input', function() {
    updateHourDisplay('end_hour', 'end_hour_display');
});
