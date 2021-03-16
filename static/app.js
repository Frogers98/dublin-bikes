 let map;

    function initMap() {
        fetch("/stations").then(response => {
            return response.json();
        }).then(data => {
            console.log("data:", data);

            map = new google.maps.Map(document.getElementById("map"), {
                center: {lat: 53.349804, lng: -6.260310},
                zoom: 12,
            });

            data.forEach(station => {
                const marker = new google.maps.Marker({
                    position: {lat: station.position_lat, lng: station.position_long},
                    //label: station.name,
                    map: map,
                })
                marker.addListener("click", () => {
                    const infowindow = new google.maps.InfoWindow({
                        content: '<p>Station Name: ' + station.name + '</p>',
                    });
                    infowindow.open(map, marker);
                });
            })
        }).catch(err => {
            console.log("Oops!", err);
        })
    }
console.log("TESTING")
    // Fill the selector - adapted from https://www.codebyamir.com/blog/populate-a-select-dropdown-list-with-json

//  let dropdown = document.getElementById('stationSelector');
// dropdown.length = 0;
//
// let defaultOption = document.createElement('option');
// defaultOption.text = 'Choose a Station';
//
// dropdown.add(defaultOption);
// dropdown.selectedIndex = 0;
//
//
// fetch("/stations")
//   .then(
//     function(response) {
//       if (response.status !== 200) {
//         console.warn('Looks like there was a problem. Status Code: ' +
//           response.status);
//         return;
//       }
//
//       // Examine the text in the response
//       response.json().then(function(data) {
//         let option;
//
//     	// for (let i = 0; i < data.length; i++) {
//         //   option = document.createElement('option');
//       	//   option.text = data[i].name;
//       	//   option.value = data[i].abbreviation;
//       	//   dropdown.add(option);
//     	// }
//           data.forEach(station => {
//             option = document.createElement('option');
//             option.text = station.name;
//             option.value = station.name;
//             dropdown.add(option);
//
//           });
//       });
//     }
//   )
//   .catch(function(err) {
//     console.error('Fetch Error -', err);
//   });