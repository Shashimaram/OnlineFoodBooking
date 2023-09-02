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
    })
    console.log(place.address_components)
}