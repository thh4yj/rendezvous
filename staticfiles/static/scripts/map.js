/***************************************************************************************
*  Code reference for Google Maps API
*  Author: Daniel Vassallo, Ahmad Awais
*  Date Published: 06/17/2010 edited 07/28/2019
*  Date Accessed: 10/17/2020
*  URL: https://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example
***************************************************************************************/

function httpGet(lat_long)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'https://maps.googleapis.com/maps/api/geocode/json?address='+lat_long+'&key=AIzaSyAUzV7coemJt7p9YGTe9XROg-0APz7EAXA', false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

var locations = []
var events = event_json.replace(/&#x27;/g,'"').replace(/\/static\//g, '');

var events_json = JSON.parse(events); //add double quotes to become json objects
for(var i = 0; i < events_json.length; i++) {
  var obj = events_json[i];
  var lat_long = obj.address.replace(/ /g, '%20');
  var myJson = httpGet(lat_long);
  //console.log(myJson);
  var status = JSON.parse(myJson).status;
  if(status != "OK"){
    obj = null;
  }
  else{
    var geo_location = JSON.parse(myJson).results[0].geometry.location;
    obj["lat"] = geo_location["lat"]
    obj["lng"] = geo_location["lng"]
  }
}
var locations = events_json
console.log(locations)


var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13, // Changed zoom to 13 to give more definition to the surrounding area
  mapTypeId: google.maps.MapTypeId.ROADMAP
});

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(function (position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      map.setCenter(initialLocation);
      //console.log(locations)
      var marker = new google.maps.Marker({
        position: initialLocation,
        map: map,
        title: 'Your position',
        draggable: true,
        icon : {url: 'https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_blue.png'},
      });
  });
}

var infowindow = new google.maps.InfoWindow();

var marker, i;

for (i = 0; i < locations.length; i++) {  
  marker = new google.maps.Marker({
    position: new google.maps.LatLng(locations[i]["lat"], locations[i]["lng"]),
    map: map
  });

  google.maps.event.addListener(marker, 'click', (function(marker, i) {
    return function() {
      infowindow.setContent(locations[i]["title"]);
      infowindow.open(map, marker);
    }
  })(marker, i));
}

