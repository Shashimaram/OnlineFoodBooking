$(document).ready(function(){
    $('.add_hour').on('click', function(e){
        e.preventDefault();
        // Get values from the form fields using jQuery
        var day = $('#id_day').val();
        var from_hours = $('#id_from_hours').val();
        var to_hours = $('#id_to_hours').val();
        var is_closed = $('#id_is_closed').prop('checked');
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();

        console.log(day, from_hours, to_hours, is_closed, csrf_token);
    });

});