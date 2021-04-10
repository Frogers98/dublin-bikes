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
let markersArray = [];
let geoJson = {};
geoJson["type"] = "FeatureCollection";
geoJson["features"] = [];

let directionsService;
let directionsRenderer;

function initMap() {
    // Load google charts
    google.charts.load('current', {'packages': ['corechart']});

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    var styleArray = [
        {"elementType": "geometry", "stylers": [{"color": "#f5f5f5"}]},
        {"elementType": "labels.icon", "stylers": [{"visibility": "off"}]},
        {"elementType": "labels.text.stroke", "stylers": [{"color": "#f5f5f5"}]},
        {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text.fill", "stylers": [{"color": "#bdbdbd"}]
        },
        {
            "featureType": "poi",
            "elementType": "geometry", "stylers": [{"color": "#eeeeee"}]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text.fill", "stylers": [{"color": "#757575"}]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry", "stylers": [{"color": "#e5e5e5"}]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry.fill", "stylers": [{"color": "#c0e7c5"}]
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text.fill", "stylers": [{"color": "#9e9e9e"}]
        },
        {
            "featureType": "road",
            "elementType": "geometry", "stylers": [{"color": "#ffffff"}]
        },
        {
            "featureType": "road.arterial",
            "elementType": "labels.text.fill", "stylers": [{"color": "#757575"}]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry", "stylers": [{"color": "#dadada"}]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.text.fill", "stylers": [{"color": "#616161"}]
        },
        {
            "featureType": "road.local",
            "elementType": "labels.text.fill", "stylers": [{"color": "#9e9e9e"}]
        },
        {
            "featureType": "transit.line",
            "elementType": "geometry", "stylers": [{"color": "#e5e5e5"}]
        },
        {
            "featureType": "transit.station",
            "elementType": "geometry", "stylers": [{"color": "#eeeeee"}]
        },
        {
            "featureType": "water",
            "elementType": "geometry", "stylers": [{"color": "#c9c9c9"}]
        },
        {
            "featureType": "water",
            "elementType": "geometry.fill", "stylers": [{"color": "#cce3f5"}]
        },
        {
            "featureType": "water",
            "elementType": "labels.text.fill", "stylers": [{"color": "#9e9e9e"}]
        }
    ]

    map = new google.maps.Map(document.getElementById("map"),
        {
            center: {lat: 53.349804, lng: -6.260310},
            zoom: 13.5,
            // markersArray: [], // Array to hold all markers
        });

    map.setOptions({styles: styleArray});

    directionsRenderer.setMap(map);
    // directionsRenderer.setPanel(document.getElementById("right-panel"));
    directionsRenderer.setPanel(document.getElementById("directionsPanel"));

    // const directionsDisplay = document.getElementById("directionsPanel")
    // map.controls[google.maps.ControlPosition.BOTTOM_RIGHT].push(directionsDisplay);

    fetch("/stations")
        .then(
            response => {
                return response.json();
            }
        ).then(
        data => {

            console.log("Data: ", data);

            /*This section is here because the silly CSS section wouldn't set the height until the map had been initialised */
            var body = document.body;
            var html = document.documentElement;
            var height = (0.85) * (Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight));

            // console.log("Map data is: ", map);

            data.forEach(
                station => {
                    //var numAvailableBikes = String(station.available_bikes);
                    var cr_datetime = new Date(station.created_date).toLocaleString('en-ie');
                    // console.log(station.name, "Timestamp: ", cr_datetime);
                    console.log(station.position_lat);

                    // Create geoJSON features for distance matrix
                    var newFeature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            // Longitude comes first for geoJson
                            "coordinates": [station.position_long, station.position_lat]
                        },
                        "properties": {
                            "name": station.name,
                            "number": station.number,
                            "available_bikes": station.available_bikes,
                            "available_bike_stands": station.available_bike_stands,
                        }
                    }

                    geoJson["features"].push(newFeature);

                    const station_info_window = new google.maps.InfoWindow(
                        {
                            content: "<h1 class='StationAvail'>" + station.name + "</h1>"
                                + "<table class='StationClass'>"
                                + "<tr class='StationClassRow'>"
                                + "<td class='StationClassDivider'>"
                                + "<div class='StationInfoWindowPopupName'>Available Bikes</div>: " + station.available_bikes
                                + "</td>"
                                + "<td class='StationClassDivider'>"
                                + "<div class='StationInfoWindowPopupName'>Available Stands</div>: " + station.available_bike_stands
                                + "</td>"
                                + "</tr>"
                                + "<tr class='StationClassRow'>"
                                + "<td class='StationClassDivider'>"
                                + "<div class='StationInfoWindowPopupName'>Last Updated</div>: " + cr_datetime
                                + "</td>"
                                + "</tr>"
                                + "</table>",
                        }
                    );

                    google.maps.event.addListener(map, "click", function () {
                        station_info_window.close();
                    });

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

                    markersArray.push(marker);

                    marker.addListener("click", function () {
                        markersArray.forEach(function (marker) {
                            marker.infowindow.close(map, marker);
                        });

                        map.panTo(marker.position);
                        this.infowindow.open(map, marker);
                        showChartHolder(marker.number);
                        graphDailyInfo(marker.number, marker.name);
                        graphHourlyInfo(marker.number, marker.name);

                        // Dynamically set the min and max date for requesting predicted availability
                        // The min will be set to today and the max will be set for 5 days from now
                        // Adapted from https://stackoverflow.com/questions/17182544/disable-certain-dates-from-html5-datepicker
                        var today = new Date().toISOString().split('T')[0];
                        document.getElementById("predictionDate").setAttribute('min', today);
                        // We can also set the value to today so it will already be filled like that
                        document.getElementById("predictionDate").setAttribute('value', today);

                        var maxDay = addDays(new Date(), 5);
                        maxDay = maxDay.toISOString().split('T')[0]
                        document.getElementById("predictionDate").setAttribute('max', maxDay);


                        // This will add the event listener for requesting predicted availability
                        // Adapted from https://stackoverflow.com/questions/23640351/how-to-convert-html5-input-type-date-and-time-to-javascript-datetime
                        // Leaving this here means that we can keep track of the clicked station
                        // Only potential issue with this is if someone tries to click the button but hasn't already selected a station
                        // In which case nothing will happen at all as this listener won't have been created yet.
                        let predictionButton = document.getElementById("predictButton")
                        // First we need to remove the initial onclick function we gave the button which was to display an error message
                        // if clicked before selecting a station
                        predictionButton.onclick = null;
                        // Now we can add the new event listener to run a different function once the button is clicked
                        predictionButton.addEventListener("click", function () {
                            let predictionDate = document.getElementById("predictionDate").value;
                            let predictionTime = document.getElementById("predictionTime").value;

                            // console.log(prediction_request);
                            // alert("This worked!, selected station was " + marker.name);

                            // Pass the station number and the requested date/time to our function that will then request
                            // The prediction from our ML model in the backend
                            getAvailabilityPrediction(marker.number, predictionDate, predictionTime)
                        });
                    });
                });

            map.data.addGeoJson(geoJson, {idPropertyName: "number"});
            // Duplicate markers added, hiding these
            map.data.setStyle({visible: false});

            var input = document.getElementById('enterLocation');
            var options = {
                componentRestrictions: {country: "ie"},
                fields: ["formatted_address", "geometry", "name"],
                origin: map.getCenter(),
                strictBounds: false
            };

            // Create autocomplete input box
            autocomplete = new google.maps.places.Autocomplete(input, options);
            autocomplete.bindTo("bounds", map);
            const enteredLocationMarker = new google.maps.Marker({map: map});
            enteredLocationMarker.setVisible(false);
            let enteredLocation = map.getCenter();

            // Event when entered location changes - pan to new location, update listed stations
            autocomplete.addListener("place_changed", async () => {
                enteredLocationMarker.setVisible(false);
                enteredLocation = map.getCenter();
                const place = autocomplete.getPlace();

                if (!place.geometry || !place.geometry.location) {
                    window.alert("No details available for input: '" + place.name + "'");
                    return;
                }

                enteredLocation = place.geometry.location;
                console.log("ORIGIN LOCATION", enteredLocation.lat(), enteredLocation.lng());
                map.setCenter(enteredLocation);
                map.setZoom(15);
                // console.log(place)

                enteredLocationMarker.setPosition(enteredLocation);
                enteredLocationMarker.setVisible(true);

                const rankedStations = await calculateDistances(map.data, enteredLocation);
                showStationsList(map.data, rankedStations, enteredLocation);
            });

            //Add event lis

        }).catch(
        err => {
            console.log("Oops!", err);
        });
}

async function calculateDistances(data, origin) {

    // Distance matrix used to calculate walking distance between location entered and nearest stations
    const originLatLng = new google.maps.LatLng(origin.lat(), origin.lng());
    console.log("ORIGIN LATLNG", originLatLng.lat(), originLatLng.lng());

    const stations = [];
    const destinations = [];
    const stationDistances = [];

    data.forEach((station) => {
        const stationNum = station.getProperty("number");
        const stationLatLng = station.getGeometry().get();
        // console.log("STATION LATLNG", stationLatLng.lat(), stationLatLng.lng())

        // Distance matrix only works for up to 25 destinations, narrowing down stations
        const distanceBetween = google.maps.geometry.spherical.computeDistanceBetween(stationLatLng, originLatLng);

        const stationDistance = {
            stationNumber: stationNum,
            stationGEOM: stationLatLng,
            stationDist: distanceBetween,
        }

        stationDistances.push(stationDistance);
    });

    stationDistances.sort((first, second) => {
        return first.stationDist - second.stationDist;
    });

    const slicedDistances = stationDistances.slice(0, 10);
    console.log("NEW ARRAY LENGTH", slicedDistances.length);
    console.log("CLOSEST", stationDistances[0]);

    slicedDistances.forEach((station) => {
        stations.push(station.stationNumber);
        destinations.push(station.stationGEOM);
    });

    console.log(stations.length);
    console.log(destinations.length);

    const service = new google.maps.DistanceMatrixService();
    const getDistanceMatrix =
        (service, parameters) => new Promise((resolve, reject) => {
            service.getDistanceMatrix(parameters, (response, status) => {
                if (status != google.maps.DistanceMatrixStatus.OK) {
                    reject(response);
                } else {
                    const distances = [];
                    const results = response.rows[0].elements;
                    for (let j = 0; j < results.length; j++) {
                        const element = results[j];
                        const distanceText = element.distance.text;
                        const distanceVal = element.distance.value;
                        const distanceObject = {
                            stationNumber: stations[j],
                            distanceText: distanceText,
                            distanceVal: distanceVal,
                        };
                        distances.push(distanceObject);
                    }
                    resolve(distances);
                }
            });
        });

    const distancesList = await getDistanceMatrix(service, {
        origins: [originLatLng],
        destinations: destinations,
        travelMode: 'WALKING',
        unitSystem: google.maps.UnitSystem.METRIC,
    });

    distancesList.sort((first, second) => {
        return first.distanceVal - second.distanceVal;
    });

    console.log(distancesList[0]);
    return distancesList;
}

function showStationsList(data, stations, originLocation) {
    if (stations.length == 0) {
        console.log("empty stations list");
        return;
    }
    // let panel = document.getElementById("side_panel_default");
    // // panel.style.display = "block";
    //
    // hideCharts("stationSelector", "showAll");
    //

    const nearestStationTable = document.getElementById("nearestStationHolder");

    while (nearestStationTable.lastChild) {
        nearestStationTable.removeChild(nearestStationTable.lastChild);
    }

    for (var i = 0; i < 5; i++) {
        const currentStationObject = stations[i];
        const currentStationNumber = currentStationObject.stationNumber;
        const currentStationDetails = data.getFeatureById(currentStationNumber);
        const currentStationName = currentStationDetails.getProperty("name");
        const currentStationDistText = currentStationObject.distanceText;
        const currentStationBikes = currentStationDetails.getProperty("available_bikes");
        const currentStationStands = currentStationDetails.getProperty("available_bike_stands");
        const stationLatLng = currentStationDetails.getGeometry().get();

        const stationNameRow = nearestStationTable.insertRow();
        stationNameRow.setAttribute("id", "stationNameRow");
        stationNameRow.addEventListener("click", function () {
            nearestStationInfo(currentStationNumber);
        });
        // document.getElementById("nearestStationHolder").appendChild(stationNameRow);
        const stationNameCell = stationNameRow.insertCell();
        stationNameCell.innerHTML = currentStationName;

        const walkingDistRow = nearestStationTable.insertRow();
        walkingDistRow.setAttribute("id", "walkingDistRow");
        const walkingDistCell = walkingDistRow.insertCell();
        walkingDistCell.innerHTML = "Walking distance: " + currentStationDistText;

        const availBikesRow = nearestStationTable.insertRow();
        availBikesRow.setAttribute("id", "availBikesRow");
        const availBikesCell = availBikesRow.insertCell();
        availBikesCell.innerHTML = "Available bikes: " + currentStationBikes;

        const availStandsRow = nearestStationTable.insertRow();
        availStandsRow.setAttribute("id", "availStandsRow");
        const availStandsCell = availStandsRow.insertCell();
        availStandsCell.innerHTML = "Available stands: " + currentStationStands;

        const getDirectionsRow = nearestStationTable.insertRow();
        getDirectionsRow.setAttribute("id", "getDirectionsRow");
        getDirectionsRow.addEventListener("click", function () {
            calculateAndDisplayRoute(originLocation, stationLatLng)
        });
        const getDirectionsCell = getDirectionsRow.insertCell();
        getDirectionsCell.innerHTML = "Get directions";
    }
}

function filterMarkers(markerNumber) {
    // Function to make all markers but the selected marker invisible
    console.log("In filters marker function");

    console.log("selected marker is: " + markerNumber);

    // Loop through all the markers
    for (let i = 0; i < markersArray.length; i++) {

        let currentMarker = markersArray[i];
        // Check if the show all stations option was selected first

        if (markerNumber == "showAll") {
            // Make all markers visible
            currentMarker.setVisible(true);
            currentMarker.infowindow.close(map, currentMarker);
        }

        // Make all markers but the selected marker invisible
        else if (markerNumber == currentMarker.number) {
            console.log("Marker found!");
            currentMarker.setVisible(true);
            google.maps.event.trigger(currentMarker, 'click');
        } else {
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
    } else if (percentRemaining <= 25) {
        colour = "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png";
    } else if (percentRemaining > 25) {
        colour = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
    }
    return colour;
}

function filterColours(markerColour) {
    // function to filter markers based on selected colour in radio buttons

    // First we can check if all colours was selected and just make all markers visible
    if (markerColour == "allColours") {
        for (let i = 0; i < markersArray.length; i++) {
            let currentMarker = markersArray[i];
            currentMarker.setVisible(true);
        }
    } else {
        // make an array to store all the markers of this colour
        let colouredMarkers = [];
        for (let i = 0; i < markersArray.length; i++) {
            let currentMarker = markersArray[i];
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
    if (stationNumber != "showAll") {
        document.getElementById('chartHolder').style.display = "block";
    } else {
        // Zoom out and recentre
        map.setZoom(13);
        map.panTo({lat: 53.349804, lng: -6.260310});
        document.getElementById('chartHolder').style.display = "none";
    }
}

function graphDailyInfo(stationNumber, stationName) {
    // Function to graph the average availability by day for a clicked station
    console.log("IN graphDailyINfo Station number is: " + stationNumber)

    console.log("Station info for station" + stationNumber)
    // Clear the div so the backhround image of a loading spinner can be seen
    document.getElementById("chart1").innerHTML = "";
    // Fetch the data
    fetch(`single_station_availability_stat_by_date/${stationNumber}`).then(
        response => {
            return response.json();
        }
    ).then(
        data => {
            console.log("data for this station is:");
            console.log(data);

            // Info for the graph such as title
            var options = {
                title: `Average availability by day for ${stationName}`,
                vAxis: {title: "Number of bikes available"},
                hAxis: {title: "Date"},
            };
            // Load the chart object from the api
            var chart_data = new google.visualization.DataTable();
            // Make columns for the chart and specify their type and title
            chart_data.addColumn('datetime', 'Date');
            chart_data.addColumn('number', 'Available bikes');
            // Loop through each days average data that was retrieved from flask, add info from each day as a row in the google DataTable
            data.forEach(entry => {
                chart_data.addRow([new Date(entry.created_date_date), parseInt(entry.available_bikes)])
            })
            // Specify where the chart will be drawn and draw it
            var chart = new google.visualization.ColumnChart(document.getElementById('chart1'));
            chart.draw(chart_data, options);

        });
}

function graphHourlyInfo(stationNumber, stationName) {
    // Function to graph the average availability by hour for a clicked station
    console.log("IN graphHourlyINfo Station number is: " + stationNumber)

    console.log("Station info for station" + stationNumber)
    // Clear the div so the backhround image of a loading spinner can be seen
    document.getElementById("chart2").innerHTML = "";
    // Fetch the data
    fetch(`single_station_availability_stat_by_hourno/${stationNumber}`).then(
        response => {
            return response.json();
        }
    ).then(
        data => {
            console.log("data for this station is:");
            console.log(data);

            // Info for the graph such as title
            var options = {
                title: `Average availability by hour for ${stationName}`,
                vAxis: {title: "Number of bikes available"},
                hAxis: {title: "Hour"},
            };
            // Load the chart object from the api
            var chart_data = new google.visualization.DataTable();
            // Make columns for the chart and specify their type and title
            chart_data.addColumn('number', 'Date');
            chart_data.addColumn('number', 'Available bikes');
            // Loop through each days average data that was retrieved from flask, add info from each day as a row in the google DataTable
            data.forEach(entry => {
                chart_data.addRow([entry.created_date_hourno, parseInt(entry.available_bikes)])
            })
            // Specify where the chart will be drawn and draw it
            var chart = new google.visualization.ColumnChart(document.getElementById('chart2'));
            chart.draw(chart_data, options);

        });
}

// Reset chart/station info when location is entered, maybe not the most efficient approach
function hideCharts(id, valueToSelect) {
    let targetSelect = document.getElementById(id);
    targetSelect.value = valueToSelect;
    showChartHolder(valueToSelect);
    for (let i = 0; i < markersArray.length; i++) {
        let currentMarker = markersArray[i];
        currentMarker.setVisible(true);
        currentMarker.infowindow.close();
    }
}

function nearestStationInfo(stationNumber) {
    directionsRenderer.set('directions', null);
    for (let i = 0; i < markersArray.length; i++) {
        let currentMarker = markersArray[i];
        if (currentMarker.number == stationNumber) {
            currentMarker.infowindow.open(map, currentMarker);
        } else {
            currentMarker.infowindow.close(map, currentMarker);
        }
    }
}

function calculateAndDisplayRoute(originLocation, stationLocation) {
    directionsService.route(
        {
            origin: originLocation,
            destination: stationLocation,
            travelMode: google.maps.TravelMode.WALKING,
        },
        (response, status) => {
            if (status === "OK") {
                const directionsDisplay = document.getElementById("directionsPanel");
                directionsDisplay.style.display = "block";
                directionsRenderer.setDirections(response);
            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );
}

function NoStationPredictReq() {
    // Function that will be called if the request prediction button is clicked before first clicking a station
    alert("Please select a marker to view available prediction times.\nWe can only show predictions from between today and the next 5 days.")
}

function getAvailabilityPrediction(stationNumber, requestedDate, requestedTime) {
    console.log("In prediction function, station number is: " + stationNumber)
    console.log("Requested date is: " + requestedDate)
    console.log("Requested time is: " + requestedTime)
    // Check if the requested prediction date is the default date from 2010, if so alert an error message

    let prediction_request = new String(requestedDate + " " + requestedTime);

    fetch(`/test_model/${requestedTime}/${stationNumber}`).then(
        response => {
            return response.json();
        }
    ).then(
        prediction => {
            console.log("This is where the prediction will go, instead of a prediction the station name is: " + prediction);
            console.log("Requested time was " + prediction_request);
            //alert("This worked should see details in console!");
            // We can now pass this output back to our html
            document.getElementById("predictionOutput").innerHTML = `There should be ${prediction} bikes at this station at ${prediction_request}`
        });

}

function addDays(date, days) {
    // Function to add a certain amount of days to a date
    // This is currently used to find the date five days from the current date to set the max date in the date picker
    // Taken from https://stackoverflow.com/questions/563406/add-days-to-javascript-date
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}