mapboxgl.accessToken = 'pk.eyJ1IjoiZ2FsZHJvbiIsImEiOiJjbHRhYzltZG4wNDN1MmlsbThnOWx2aHlsIn0.XnK4cKK9Xxbt-p0RQPm75g';
const map = new mapboxgl.Map({
	container: 'mapbox', // container ID
	style: 'mapbox://styles/mapbox/streets-v12', // style URL
	center: [-84.5, 33.7], // starting position [lng, lat]
	zoom: 9.6, // starting zoom
  maxBounds: [[-85.68856261783463, 33.2109980948708], [-83.10992717367886, 34.362195482591545]],
  minZoom: 2,
});


function boundsFromPoints(points) {
  const bounds = new mapboxgl.LngLatBounds();
  points.forEach(point => {
    bounds.extend(point);
  });
  return bounds;
}

function displayClusterInfo(cluster_data) {
  console.log(cluster_data)
}

map.on('load', function() {
  fetch('/neighborhoods')
  .then(response => response.json())
  .then(function(data) {
    const houses = data.houses
    const neighborhoods = data.neighborhoods
    console.log("houses", houses)

    map.addSource('houses', {
      type: 'geojson',
      data: houses
    });
    map.addLayer({
      id: 'houses',
      type: 'circle',
      source: 'houses',
      paint: {
        'circle-radius': 5,
        'circle-color': ['get', 'color'],
        'circle-opacity': ['get', 'opacity']
      },
    });
  });
});

// map.on('load', function() {
//   fetch('/features')
//   .then(response => response.json())
//   .then(function(data) {
//     const features = data.features
//     const cluster_data = data.cluster_data
//     console.log("features", features)

//     map.addSource('points', {
//       type: 'geojson',
//       data: features['points']
//     });
//     map.addLayer({
//       id: 'points',
//       type: 'circle',
//       source: 'points',
//       paint: {
//         'circle-radius': 5,
//         'circle-color': ['get', 'color']
//       },
//     });
//     map.addSource('centers', {
//       type: 'geojson',
//       data: features['centers']
//     });
//     map.addLayer({
//       id: 'centers',
//       type: 'circle',
//       source: 'centers',
//       paint: {
//         'circle-radius': 5,
//         'circle-color': ['get', 'color']
//       }
//     });
//     map.addSource('shapes', {
//       type: 'geojson',
//       data: features['shapes']
//     });
//     map.addLayer({
//       id: 'shapes',
//       type: 'fill',
//       source: 'shapes',
//       paint: {
//         'fill-color': ['get', 'color'],
//         'fill-opacity': 0.2
//       }
//     });
//     map.addLayer({
//       id: 'shapes_line',
//       type: 'line',
//       source: 'shapes',
//       paint: {
//         'line-color': ['get', 'color'],
//         'line-width': 1.5,
//         'line-opacity': 0.8
//       }
//     });

//     map.on('click', 'shapes', (e) => {
//       const cluster_id = e.features[0].properties.cluster;
//       const cluster_polygon = features['shapes']
//         .features
//         .filter(feature => feature.properties.cluster === cluster_id)[0]
//         .geometry
//         .coordinates[0];
//       map.fitBounds(boundsFromPoints(cluster_polygon), {
//         padding: 50
//       });
//       displayClusterInfo(cluster_data[cluster_id]);
//     });
//   });
// });
