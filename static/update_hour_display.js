function updateHourDisplay() {
    var startHourValue = document.getElementById('start_hour').value;
    var endHourValue = document.getElementById('end_hour').value;

    var startHourDate = new Date(startHourValue);
    var endHourDate = new Date(endHourValue);

    document.getElementById('start_hour_display').innerText = startHourDate.toLocaleString('en-US');
    document.getElementById('end_hour_display').innerText = endHourDate.toLocaleString('en-US');
}

document.addEventListener('DOMContentLoaded', function() {
    updateHourDisplay();
    document.getElementById('start_hour').addEventListener('change', updateHourDisplay);
    document.getElementById('end_hour').addEventListener('change', updateHourDisplay);
    // Rest of your code
});
