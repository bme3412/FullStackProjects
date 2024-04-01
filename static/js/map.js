function initMap() {
    // Map options
    var options = {
        zoom: 15,
        center: {lat: venueLatitude, lng: venueLongitude}
    };

    // New map
    var map = new google.maps.Map(document.getElementById('map'), options);

    // Add marker
    var marker = new google.maps.Marker({
        position: {lat: venueLatitude, lng: venueLongitude},
        map: map,
        title: venueName
    });

    // Optional: Add info window
    var infoWindow = new google.maps.InfoWindow({
        content: `<h3>${venueName}</h3><p>Location details</p>`
    });

    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });
}

// Ensure the callback name in the Google Maps script URL matches this function name.
