let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in','us']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typingg...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields

    // console.log('place name=>', place.name)
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(resuls, status){
        // console.log('resuls=>', resuls)
        // console.log('status=>', status)
        if (status === google.maps.GeocoderStatus.OK){
            var latitude = resuls[0].geometry.location.lat();
            var longitude = resuls[0].geometry.location.lng();

            console.log('latitude=>', latitude)
            console.log('longitude=>', longitude)

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
        }
    });
    console.log(place.address_components)
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {

            // get country
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city

            if (place.address_components[i].types[j] == 'locality') {
                $('#id_city').val(place.address_components[i].long_name);
            }

            if (place.address_components[i].types[j] == 'postal_code') {
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
            }
        }
    }
}

$(document).ready(function() {

    // $('#cart-counter').on('load', function(e){
    //     e.preventDefault();
    // })

    // adding items to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');
        data={
            food_id:food_id,
             url:url
            }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success:function(response){

                if (response.status == 'login_required'){
                    console.log(response.message,'','info').then(function(){
                        window.location='/accounts/login';
                    })

                }else if (response.status == 'Failed'){
                    console.log(response.message,'','error')
                }
                else{
                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    console.log(response);

                    // subtotal, tax, grand total
                    applyCartAmounts(
                        response.cart_amounts["subtotal"],
                        response.cart_amounts["tax"],
                        response.cart_amounts["grand_total"],
                    )
                }
            }
        })
    })

    // Place the item quantity  on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty');
        // console.log(qty);
        $('#'+the_id).html(qty);
    })

    // decrease items to cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');
        var cart_id = $(this).attr('id');
        data={
            food_id:food_id,
                url:url
            }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success:function(response){
                if (response.status == 'login_required'){
                    console.log(response.message,'','info').then(function(){
                        window.location='/accounts/login';
                    })
                }else if (response.status == 'Failed'){
                    console.log(response.message,'','error')
                }else{
                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    applyCartAmounts(
                        response.cart_amounts["subtotal"],
                        response.cart_amounts["tax"],
                        response.cart_amounts["grand_total"],
                    )
                    if(window.location.pathname=='/cart/'){
                        removeItemElement(response.qty,cart_id);
                        checkEmptyCart();


                    }

                }
            }
        })
    })


    // decrease items to cart
    $('a.delete_cart').on('click', function(e){
        e.preventDefault();

        var cart_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: "GET",
            url: url,
            success: function(response){
                if (response.status == 'failed'){
                    console.log(response.message, '', 'error');
                } else {
                    $('#cart-counter').html(response.cart_counter['cart_count']);

                    console.log(response.status, response.message, 'success');

                    applyCartAmounts(
                        response.cart_amounts["subtotal"],
                        response.cart_amounts["tax"],
                        response.cart_amounts["grand_total"],
                    )

                    // Move the removeItemElement function call inside the success callback
                    removeItemElement(0, cart_id);
                    checkEmptyCart();
                }
            }
        })
    })

    function removeItemElement(cartitemqty, cart_id) {

        if (cartitemqty <= 0) {
            // Remove the Cart item by element
            console.log(cart_id);
            $("#cart-item-" + cart_id).remove();
        }

    }

    function checkEmptyCart(){
        var cart_counter = document.getElementById("cart-counter").innerHTML
        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = 'block';
        }
    }

    function applyCartAmounts(subtotal,tax,grand_total) {
        if (window.location.pathname == "/cart/") {
            $("#subtotal").html(subtotal)
            $("#total").html(grand_total)
            $("#tax").html(tax)
        }
    }


    // Document ready close
});