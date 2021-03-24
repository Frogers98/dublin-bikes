
/*--------- Site Javascript -------------*/


/* 
-------------------
TABLE OF CONTENTS
-------------------

-1. Header
-2. Footer

------------------
END
------------------

Note: Use CTRL+F and the Number with a dot to navigate to that section.

*/

let map;

function initMap() {
    fetch("/stations").then(response => {
        return response.json();
    }).then(data => {
        console.log("data:", data);
        var test = getLatestUpdate();
        console.log("DEBUG IS" + test)
        map = new google.maps.Map(document.getElementById("map"), {
            center: {lat: 53.349804, lng: -6.260310},
            zoom: 12,
            markersArray: [], // Array to hold all markers
        });
        data.forEach(station => {
            const marker = new google.maps.Marker({
                // Add the co-ordinates and name to each marker and specify which map it belongs to
                position: {lat: station.position_lat, lng: station.position_long},
                // Add the station name and number as attributes to the marker, this can be used as an identifier
                name: station.name,
                number: station.number,
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

function getLatestUpdate() {
    //Function to get the latest update from availability table
    fetch("/availability").then(response => {
        return response.json();
    }).then(availabilityData =>{
        return availabilityData;
    })
}

function filterMarkers(markerNumber) {
    // Function to make all markers but the selected marker invisible
    console.log("In filters marker function");
    console.log("selected marker is: " + markerNumber);
    // Loop through all the markers
    for (let i = 0; i < map.markersArray.length; i++) {
        let currentMarker = map.markersArray[i];
        // Check if the show all stations option was selected first
        if (markerNumber == "showAll") {
            // Make all markers visible
             currentMarker.setVisible(true)
        }
        // Make all markers but the selected marker invisible
        else if (markerNumber == currentMarker.number) {
            console.log("Marker found!");
            currentMarker.setVisible(true);
        } else {
            currentMarker.setVisible(false);
        }
    }
}
