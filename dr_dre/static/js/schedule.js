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
    }).done(function (data) {
            console.log("Response " + JSON.stringify(data));
        }
    ).error(function (data) {
            console.log("Response " + JSON.stringify(data));
        }
    )
}

$('.frame').click(function(){
    create_appt(this.dataset);
});


});