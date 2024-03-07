mapboxgl.accessToken = 'pk.eyJ1IjoiZ2FsZHJvbiIsImEiOiJjbHRhYzltZG4wNDN1MmlsbThnOWx2aHlsIn0.XnK4cKK9Xxbt-p0RQPm75g';
const map = new mapboxgl.Map({
	container: 'mapbox', // container ID
	style: 'mapbox://styles/mapbox/streets-v12', // style URL
	center: [-74.5, 40], // starting position [lng, lat]
	zoom: 9, // starting zoom
});

map.on('load', function() {
  fetch('/features')
  .then(response => response.json())
  .then(function(features) {
    map.addSource('points', {
      type: 'geojson',
      data: features['points']
    });
    map.addLayer({
      id: 'points',
      type: 'circle',
      source: 'points',
      paint: {
        'circle-radius': 5,
        'circle-color': ['get', 'color']
      },
      minzoom: 5,
    });
    map.addSource('shapes', {
      type: 'geojson',
      data: features['shapes']
    });
    map.addLayer({
      id: 'shapes',
      type: 'fill',
      source: 'shapes',
      paint: {
        'fill-color': ['get', 'color'],
        'fill-opacity': 0.5
      }
    });
    map.addLayer({
      id: 'shapes_line',
      type: 'line',
      source: 'shapes',
      paint: {
        'line-color': ['get', 'color'],
        'line-width': 2
      }
    });
  });
});
