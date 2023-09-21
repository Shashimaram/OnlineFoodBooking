$(document).ready(function(){

    // adding OpenHours
    $('.add_hour').on('click', function(e){
        e.preventDefault();
        // Get values from the form fields using jQuery
        var day = $('#id_day').val();
        var from_hours = $('#id_from_hours').val();
        var to_hours = $('#id_to_hours').val();
        var is_closed = document.getElementById("id_is_closed").checked;
        console.log(is_closed);
        var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        var url = $('#add_hour_url').val();
        if(is_closed) {
            is_closed == true;
            condition = "day != ''"
        }else{
            is_closed == false;
            condition = "day != '' && from_hours != '' && to_hours != ''"
        }
        if(eval(condition)){
            $.ajax({
                type: 'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hours':from_hours,
                    'to_hours':to_hours,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrfmiddlewaretoken,
                },
                success: function(response){
                    if(response.status == 'success'){
                        console.log(response);
                        const dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"];
                        const dayName = dayNames[response.day - 1];
                        if (response.is_closed=='Closed') {
                            var html = `<tr id="hour-${response.id}">
                                <td><b>${dayName}</b></td>
                                <td><b>Closed</b></td>
                                <td><a href="#" class='remove_hour' data-url="/accounts/vendor/opening-hours/remove/${response.id}/" >Remove</a></td>
                            </tr>`;
                        }else{
                            var html = `<tr id="hour-${response.id}">
                                <td><b>${dayName}</b></td>
                                <td><b>${response.from_hours} - ${response.to_hours}</b></td>
                                <td><a href="#" class='remove_hour' data-url="/accounts/vendor/opening-hours/remove/${response.id}/" >Remove</a></td>
                            </tr>`;
                        }

                                    // Append the new row to the "opening_hours" table
                        $('.open_table').append(html);
                        document.getElementById('opening_hours').reset();
                    }else{
                        console.log(response.message,'','error')
                    }
                }
            })
            // console.log("Add the entry");
        }else{
            console.log("please fill all the fields"," ",'info')
        }
    });


    // Remove open_hours from the document

    // $('.remove_hour').on('click',function(e){
    //     e.preventDefault();
    //     url = $(this).attr('data-url');
    //     console.log(url);
    //     $.ajax({
    //         type:"GET",
    //         url: url,
    //         success: function(response){
    //             $('#hour-'+response.id).remove();
    //         }
    //     })

    // })

});