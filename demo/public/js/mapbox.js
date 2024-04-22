mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN_HERE;

let hoveredPolygonId = null;

function boundsFromPoints(points) {
  const bounds = new mapboxgl.LngLatBounds();
  points.forEach(point => {
    bounds.extend(point);
  });
  return bounds;
}

// flatten nested arrays of coordinates until it is a flat array of coordinates
function flattenCoordinates(geometry) {
  let flat = geometry.flat(Infinity);
  // then group by 2s to make lnglat pairs
  flat = flat.reduce((acc, curr, i) => {
    if (i % 2 === 0) {
      acc.push([curr, flat[i + 1]]);
    }
    return acc;
  }, []);
  return flat;
}

function displayClusterInfo(cluster_data) {
  console.log(cluster_data)
}

fetch('/neighborhoods')
.then(response => response.json())
.then(function(data) {
  const houses = data.houses
  const boundaries = data.boundaries
  const subtracted_boundaries = data.subtracted_boundaries

  console.log("boundaries", boundaries)
  console.log("houses", houses)
  console.log("subtracted_boundaries", subtracted_boundaries)

  // select .main-display element
  const mainDisplay = document.getElementsByClassName('main-display')[0];
  mainDisplay.innerHTML = `
  <div class="data-vis-container">
    <div class="info-panel"></div>
    <div class="mapbox-holder">
      <div id="mapbox"></div>
      <div class="legend">
        <div>Median House Prices</div>
        <div><i class="fa-solid fa-square" style="color: rgb(246, 160, 158);"></i> < 260,000</div>
        <div><i class="fa-solid fa-square" style="color: rgb(221, 135, 133);"></i> 260,000 - 420,000</div>
        <div><i class="fa-solid fa-square" style="color: rgb(196, 110, 108);"></i> 420,000 - 560,000</div>
        <div><i class="fa-solid fa-square" style="color: rgb(171, 85, 83);"></i> > 560,000</div>
      </div>
    </div
  </div>
  `

  const map = new mapboxgl.Map({
    container: 'mapbox', // container ID
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [-84.5, 33.7], // starting position [lng, lat]
    zoom: 9.6, // starting zoom
    // maxBounds: [[-85.68856261783463, 33.2109980948708], [-83.10992717367886, 34.362195482591545]],
    // minZoom: 2,
  });

  map.on('load', function() {

    map.addSource('houses', {
      type: 'geojson',
      data: houses
    });
    map.addSource('subtracted_boundaries', {
      type: 'geojson',
      data: subtracted_boundaries
    });
    map.addLayer({
      id: 'houses',
      type: 'circle',
      source: 'houses',
      paint: {
        'circle-radius': 5,
        'circle-color': ['get', 'color'],
        'circle-opacity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          10.5, 0,
          11, 1,

        ]
      },
    });
    map.addLayer({
      id: 'subtracted_boundaries',
      type: 'line',
      source: 'subtracted_boundaries',
      paint: {
        'line-color': ['get', 'color'],
        'line-width': 1.5,
        'line-opacity': 0.8
      }
    });
    map.addLayer({
      id: 'subtracted_boundaries_fill',
      type: 'fill',
      source: 'subtracted_boundaries',
      paint: {
        'fill-color': ['get', 'color'],
        // opacity starts at 0.9 and goes to 0.4 when zoomed in
        'fill-opacity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          9.8, 0.9,
          11, 0.3
        ]
      }
    });

    map.on('click', 'subtracted_boundaries_fill', (e) => {
      // select info-panel attribute
      const data_vis_container = document.getElementsByClassName('data-vis-container')[0];
      // add class to data-vis-container
      data_vis_container.classList.add('info-pane-open');

      let region_id = e.features[0].properties.region_id;
      const info = document.getElementsByClassName('info-panel')[0];
      console.log("region_id", e.features[0].properties.region_id)
      const props = e.features[0].properties;
      info.innerHTML = `
        <div>${props.name}</div>
        <div class="info-part">
          <div>Housing Affordability Index</div>
          <div>${Math.round(props.hai * 100) / 100}</div>
        </div>
        <div class="info-part">
          <div>Doordash Rating</div>
          <div>${props.doordash_rating}</div>
        </div>
        <div class="info-part">
          <div>Median Price Estimate</div>
          <div>${Math.round(props.sold_price).toLocaleString()}</div>
        </div>
        <div class="info-part">
          <div>Average School Ratings</div>
          <div>${(Math.round(props.school_rating * 100)/100).toLocaleString()}</div>
        </div>
      `;

      // find geometry by matching region_id to subtracted_boundaries object
      const geometry = subtracted_boundaries.features.find(feature => feature.properties.region_id === region_id).geometry;
      const coordinates = geometry.coordinates;
      let lnglats = flattenCoordinates(coordinates);
      let bounds = boundsFromPoints(lnglats);
      map.fitBounds(bounds, {
        padding: 50
      });
    });

  });
});