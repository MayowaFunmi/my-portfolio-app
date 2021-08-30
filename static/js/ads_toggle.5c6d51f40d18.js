$(document).ready(function () {
    var colors = ['yellow', 'blue', 'red', 'black','white'];
    var i = 0;
    setInterval(function() {
        $('#change_color').css('color', colors[i]);
        i = (i == (colors.length - 1)) ? 0 : i+1;
    }, 1000);
});