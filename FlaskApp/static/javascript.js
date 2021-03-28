
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
    fetch("/stations")
    .then(
            response => 
            {
                return response.json();
            }
    ).then(
        data => 
            {

            console.log("Data: ", data);

            /*This section is here because the silly CSS section wouldn't set the height until the map had been initialised */
            var body = document.body;
            var html = document.documentElement;
            var height = (0.85)*(Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight));

            map = new google.maps.Map(document.getElementById("map"), 
                {
                    center: {lat: 53.349804, lng: -6.260310},
                    zoom: 13.5,
                    markersArray: [], // Array to hold all markers
                });

            console.log("Map data is: ", map);

            data.forEach(
                station => 
                    {
                    //var numAvailableBikes = String(station.available_bikes);
                    var cr_datetime=new Date(station.created_date).toLocaleString('en-ie');
                    console.log("Timestamp: ", cr_datetime);

                    const station_info_window=new google.maps.InfoWindow(
                        {
                            content: "<h1 class='StationAvail'>" + station.name + "</h1>" 
                            +"<table class='StationClass'>"
                                +"<tr class='StationClassRow'>"
                                    +"<td class='StationClassDivider'>"
                                        +"<div class='StationInfoWindowPopupName'>Available Bikes</div>: " + station.available_bikes
                                    +"</td>"
                                    +"<td class='StationClassDivider'>"
                                        +"<div class='StationInfoWindowPopupName'>Available Stands</div>: " + station.available_bike_stands
                                    +"</td>"
                                +"</tr>"
                                +"<tr class='StationClassRow'>"
                                    +"<td class='StationClassDivider'>"
                                        +"<div class='StationInfoWindowPopupName'>Last Updated</div>: " + cr_datetime
                                    +"</td>"
                                +"</tr>"                                                   
                            +"</table>",
                        }
                    );

                    const marker = new google.maps.Marker(
                        {
                        // Add the co-ordinates and name to each marker and specify which map it belongs to
                        position: {lat: station.position_lat, lng: station.position_long},
                        // Add the station name and number as attributes to the marker, this can be used as an identifier
                        name: station.name,
                        number: station.number,
                        // Also add the available bikes and stands
                        available_bikes: station.available_bikes,
                        available_stands: station.available_bike_stands,
                        icon: determineAvailabilityPercent(station.available_bikes, station.available_bike_stands),
                        map: map,
                        //label: numAvailableBikes,
                        infowindow: station_info_window,
                        }
                    );
                        
                    map.markersArray.push(marker);

                    marker.addListener("click", function() 
                    {
                        map.markersArray.forEach(function(marker) {
                            marker.infowindow.close(map, marker);
                         });

                         this.infowindow.open(map,marker);
                         showChartHolder(this.number);
                    });
                    
                    

                });
                
        }).catch(
            err => 
            {
            console.log("Oops!", err);
            });
}


function filterMarkers(markerNumber) {
    // Function to make all markers but the selected marker invisible
    console.log("In filters marker function");

    console.log("selected marker is: " + markerNumber);

    // Loop through all the markers
    for (let i = 0; i < map.markersArray.length; i++) {
        
        let currentMarker = map.markersArray[i];
        // Check if the show all stations option was selected first
        
        if (markerNumber == "showAll") 
            {
                // Make all markers visible
                currentMarker.setVisible(true)
            }

        // Make all markers but the selected marker invisible
        else if (markerNumber == currentMarker.number) 
            {
                console.log("Marker found!");
                currentMarker.setVisible(true);
            } 
        
        else 
            {
                currentMarker.infowindow.close(map, currentMarker);
                currentMarker.setVisible(false);
            }
    }
}

function determineAvailabilityPercent(available_bikes, available_stands) {
  // Function to return a marker colour depending on the amount of available bikes remaining
    let totalStations = available_bikes + available_stands;
    let percentRemaining = (available_bikes / totalStations) * 100;
    // We will change the colour depending on the percentage and then return it
    let colour;
    if (percentRemaining == 0) {
        colour = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
    }
    else if (percentRemaining <= 25) {
        colour = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png";
    }
    else if (percentRemaining > 25) {
        colour = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
    }
    return colour;
}

function filterColours(markerColour) {
    // function to filter markers based on selected colour in radio buttons

    // First we can check if all colours was selected and just make all markers visible
    if (markerColour == "allColours") {
        for (let i = 0; i < map.markersArray.length; i++) {
            let currentMarker = map.markersArray[i];
            currentMarker.setVisible(true);
        }
    }
    else {
        // make an array to store all the markers of this colour
        let colouredMarkers = [];
        for (let i = 0; i < map.markersArray.length; i++) {
            let currentMarker = map.markersArray[i];
            if (markerColour == currentMarker.icon) {
                // Append all markers with the specified colour to the array
                colouredMarkers.push(currentMarker);
            }
            // First make all markers invisible as we're looping through
            currentMarker.infowindow.close(map, currentMarker);
            currentMarker.setVisible(false);
        }
        // Now we can make all the markers of the colour selected visible
        for (let i = 0; i < colouredMarkers.length; i++) {
            let currentMarker = colouredMarkers[i];
            currentMarker.setVisible(true);
        }
    }

}

function showChartHolder(stationNumber) {
    if (stationNumber != "showAll")
    {
        document.getElementById('chartHolder').style.display = "block";
    } else {
        document.getElementById('chartHolder').style.display = "none";
    }
}
