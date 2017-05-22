jQuery(document).ready(function($){

    var ENDPOINT = '/api/v1/appointment/';

    var create_appt = function(data){
        $.ajax({
            url: ENDPOINT,
            type: "POST",
            data: {
                "date": data['day'],
                "time_start": data['hour'] + ":" + data['minutes'],
                "non_recurring": "Anon",
                "reason": "I broke a leg"
            },
            dataType: "json",
            success: function (data) {
                book_frame(JSON.stringify(data));
            },
            error: function (data) {
                console.log("Response " + JSON.stringify(data));
            }
        })
    };

    $('.frame').click(function(){
        create_appt(this.dataset);
    });

});

var book_frame = function(data){
    var data = JSON.parse(data);
    var day_selector = '[data-day="' + data["date"] + '"]';
    var hour_selector = '[data-hour="' + data["hour_start"] + '"]';
    var min_selector = '[data-minutes="' + data["min_start"] + '"]';
    var selector = '.frame' + day_selector + hour_selector + min_selector;
    console.log(selector);
    var found = $(selector);
    console.dir(found);
    found.removeClass('frame');
    found.addClass('booked');
};
