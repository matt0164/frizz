//sets up a range slider which users can use to adjust the forecast time period. The range slider will default
// to show the forecast for the current day from 10 AM to 3 PM. When the user changes the slider, the time stamps
// below the slider will update to reflect the new forecast period.

//var dt_from = "2023-06-13 00:00:00";
//var dt_to = "2023-06-14 00:00:00";

var dt_from = new Date();
var dt_to = new Date();

// Add 24 hours to the current date and time
dt_to.setHours(dt_from.getHours() + 24);

var min_val = Date.parse(dt_from) / 1000 / 3600;
var max_val = Date.parse(dt_to) / 1000 / 3600;

// Set initial values to 10 AM and 3 PM of current day
var today = new Date();
var initial_from = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 10, 0, 0);
var initial_to = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 15, 0, 0);

function zeroPad(num, places) {
  var zero = places - num.toString().length + 1;
  return Array(+(zero > 0 && zero)).join("0") + num;
}

function formatDT(__dt) {
    var year = __dt.getFullYear();
    var month = zeroPad(__dt.getMonth() + 1, 2);
    var date = zeroPad(__dt.getDate(), 2);
    var hours = __dt.getHours();
    var minutes = zeroPad(__dt.getMinutes(), 2);
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    return year + '-' + month + '-' + date + ' ' + zeroPad(hours, 2) + ':' + minutes + ' ' + ampm;
};

$('.slider-time').html(formatDT(initial_from));
$('.slider-time2').html(formatDT(initial_to));

function updateForecastDates(ui) {
    var dt_cur_from = new Date(ui.values[0] * 1000 * 3600);
    var dt_cur_to = new Date(ui.values[1] * 1000 * 3600);

    // Set the updated hours to your global variable or directly to the elements
    document.getElementsByClassName('slider-time')[0].innerHTML = formatDT(dt_cur_from);
    document.getElementsByClassName('slider-time2')[0].innerHTML = formatDT(dt_cur_to);

    // Get the start and end hours
    var startHourValue = zeroPad(dt_cur_from.getHours(), 2) + ':00:00';
    var endHourValue = zeroPad(dt_cur_to.getHours(), 2) + ':00:00';

    // Fetch the new forecast
    fetchWeatherForecast(startHourValue, endHourValue);
}

$("#slider-range").slider({
    range: true,
    min: min_val,
    max: max_val,
    step: 1,
    values: [initial_from.getTime() / 1000 / 3600, initial_to.getTime() / 1000 / 3600],
    slide: function (e, ui) {
        var dt_cur_from = new Date(ui.values[0] * 1000 * 3600);
        $('.slider-time').html(formatDT(dt_cur_from));

        var dt_cur_to = new Date(ui.values[1] * 1000 * 3600);
        $('.slider-time2').html(formatDT(dt_cur_to));
    },
    change: updateForecastDates
});
