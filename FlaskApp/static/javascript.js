
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
let openmarkers = [];
let allmarkers = [];

function initMap(){
    fetch("/station")
    .then(
            response=>
            {
                return response.json();
            }
    ).then( 
            data=>
            {
                console.log("data: ", data);

                /*This section is here because the silly CSS section wouldn't set the height until the map had been initialised */
                var body = document.body;
                var html = document.documentElement;
                var height = (0.85)*(Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight));

                map=new google.maps.Map(document.getElementById("map"), {
                            center: {lat: 53.349, lng: -6.260},
                            zoom:14,
                        }
                );

                document.getElementById('map').style.height = height + 'px';
                console.log(map);

                data.forEach(
                    station => 
                    {
                        console.log(station);
                        var cr_datetime=new Date(station.created_date).toLocaleString('en-ie');
                        console.log("Timestamp: ", cr_datetime)

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
                        const marker=new google.maps.Marker(
                            {
                                position: { lat: station.position_lat, lng: station.position_long },
                                map: map,
                                infowindow: station_info_window,
                            }
                        );
                        
                        allmarkers.push(marker);

                        marker.addListener("click",function() 
                        {
                            allmarkers.forEach(function(marker) {
                                marker.infowindow.close(map, marker);
                             });

                             this.infowindow.open(map,marker);
                        }
                        );
                    }
                );

            }
        )
    .catch(
            err=>
        {
            console.log("Error: ",err);
        }
    );
}