$(function() {
    $('#btnSearch').click(function() {
        $.ajax({
            url: '/search',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var content = $.parseJSON(response);
                console.log(response);
                if ( content.error == undefined ){
                    var maplink = 'https://www.nationalnanpa.com/area_code_maps/usmaps/'+ content.shortcode.toLowerCase() + '.gif';
                    $("#ac-output").html("<h2>Area code "+content.areacode+": "+content.region+"</h2><p>"+content.cities+"</p>");
                    $("#ac-map").html('<img src="'+maplink+'" />');
                } else {
                    $("#ac-output").html('<h2>'+content.error+'</h2>');   
                    $("#ac-map").html('');
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#inputAreaCode').keypress(function(e){
        if ( e.which == 13 ){
            e.preventDefault();
            $('#btnSearch').click();
        }
    });
});