let map;

function initMap() {
    fetch("/stations").then(response => {
        return response.json();
    }).then(data => {
        console.log("data:", data);

        map = new google.maps.Map(document.getElementById("map"), {
            center: {lat: 53.349804, lng: -6.260310},
            zoom: 12,
            markersArray: [], // Array to hold all markers
        });
        data.forEach(station => {
            const marker = new google.maps.Marker({
                // Add the co-ordinates and name to each marker and specify which map it belongs to
                position: {lat: station.position_lat, lng: station.position_long},
                // Add the station name as an attribute to the marker, this can be used as an identifier
                name: station.name,
                map: map,
            })
            marker.addListener("click", () => {
                const infowindow = new google.maps.InfoWindow({
                    content: '<p>Station Name: ' + station.name + '</p>',
                });
                infowindow.open(map, marker);
            });
            map.markersArray.push(marker)
        })
    }).catch(err => {
        console.log("Oops!", err);
    })

}

function filterMarkers(markerName) {
    // Function to make all markers but the selected marker invisible
    console.log("In filters marker function");
    console.log("selected marker is: " + markerName);
    // Loop through all the markers
    for (let i = 0; i < map.markersArray.length; i++) {
        let currentMarker = map.markersArray[i];
        // Make all markers but the selected marker invisible
        if (markerName == currentMarker.name) {
            console.log("Marker found!");
            currentMarker.setVisible(true);
        } else {
            currentMarker.setVisible(false);
        }
    }
}