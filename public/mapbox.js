console.log("Hello from mapbox.js!")

let points1;
let points2;

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
        }
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
  // fetch('/features/points')
  //   .then(response => response.json())
  //   .then(function(data) {
  //     const features = data.map(d => ({
  //       type: 'Feature',
  //       geometry: {
  //         type: 'Point',
  //         coordinates: [d.lng, d.lat]
  //       },
  //       properties: {
  //         title: d.name,
  //         description: d.description,
  //         color: randomColor(d.cluster)
  //       }
  //     }));
  //     map.addSource('points1', {
  //       type: 'geojson',
  //       data: {
  //         type: 'FeatureCollection',
  //         features: features
  //       }
  //     });
  //     map.addLayer({
  //       id: 'points1',
  //       type: 'circle',
  //       source: 'points1',
  //       paint: {
  //         'circle-radius': 5,
  //         'circle-color': ['get', 'color']
  //       }
  //     });
  //   });
  // fetch('/alpha_shapes')
  //   .then(response => response.json())
  //   .then(function(data) {
  //     console.log(data)
  //     singleshape = data.features[0]
  //     console.log(singleshape)
  //     map.addSource('alpha_shapes', {
  //       type: 'geojson',
  //       data: data
  //     });
  //     map.addLayer({
  //       id: 'alpha_shapes',
  //       type: 'fill',
  //       source: 'alpha_shapes',
  //       layout: {},
  //       paint: {
  //         'fill-color': '#000',
  //         'fill-opacity': 0.5
  //       }
  //     });
  //     map.addLayer({
  //       id: 'alpha_shapes_line',
  //       type: 'line',
  //       source: 'alpha_shapes',
  //       layout: {},
  //       paint: {
  //         'line-color': '#000',
  //         'line-width': 2
  //       }
  //     })
  //   });
});
