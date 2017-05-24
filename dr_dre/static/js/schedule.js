jQuery(document).ready(function($){

    var ENDPOINT = '/api/v1/appointment/';

    var create_appt = function(data){
        $.ajax({
            url: ENDPOINT,
            type: "POST",
            data: data,
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
        $('#apptModal').modal('show');
        $('input#day').val(this.dataset['day']);
        $('input#hour').val(this.dataset['hour']);
        $('input#minutes').val(this.dataset['minutes']);
    });

    $('#userForm').submit(function(event) {
        event.preventDefault();
        $('#apptModal').modal('hide');
        var $form = $(this),
            day = $('input#day').val(),
            hour = $('input#hour').val(),
            min = $('input#minutes').val(),
            who = $form.find('input#name').val(),
            reason = $form.find('input#reason').val();

        create_appt({
            "date": day,
            "time_start": hour + ":" + min,
            "non_recurring": who,
            "reason": reason
        });
    });

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

var book_frame = function(data){
    var data = JSON.parse(data);
    var day_selector = '[data-day="' + data["date"] + '"]';
    var hour_selector = '[data-hour="' + data["hour_start"] + '"]';
    var min_selector = '[data-minutes="' + data["min_start"] + '"]';
    var selector = 'td' + day_selector + hour_selector + min_selector;
    var found = $(selector);
    found.removeClass('frame');
    found.removeClass('past');
    found.addClass('booked');
};
