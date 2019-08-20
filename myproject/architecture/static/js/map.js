$(function() {
    var circles = [];
    var markers = [];
    var mymap = L.map('mapid').setView([52.233,21], 13);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mymap);

    var my_points = $('.map_datapoints');
    for (var i = 0; i < my_points.length; i++) {
        var longitude = parseFloat(my_points[i].dataset.longitude);
        var latitude = parseFloat(my_points[i].dataset.latitude);
        var adress = "project/" + my_points[i].dataset.id;
        var name = my_points[i].dataset.name;
        var marker = L.marker([longitude, latitude]).addTo(mymap);
        marker.bindPopup(`<a href="${adress}">${name}</a>`);
    }
    var popup = L.popup();
    function onMapClick(e) {
        var user_id = $('#user-data').data('id');
        if (user_id === 'None') {
            popup
            .setLatLng(e.latlng)
            .setContent(`<a href="login"><b>Log in to add projects</a>`)
            .openOn(mymap);
        } else {
            var url_attrs = `lat=${e.latlng.lng}&lon=${e.latlng.lat}&user_id=${user_id}`
            popup
            .setLatLng(e.latlng)
            .setContent(`<a href="project/add?${url_attrs}">Add a project in this location</a>`)
            .openOn(mymap);
        }
    }

    mymap.on('click', onMapClick);
});

