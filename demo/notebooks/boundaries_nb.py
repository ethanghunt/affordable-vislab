# %%
import pandas as pd
from alpha_shapes import Alpha_Shaper
import shapely.geometry
import shapely
import json
import random

# %%
df = pd.read_csv('../data/final/properties.csv')

df['lnglat'] = df.apply(lambda x: (x['longitude'], x['latitude']), axis=1)

neighborhoods = []
for group in df.groupby('region_id'):
  neighborhood = {}
  points = group[1]['lnglat'].tolist()
  scatter = shapely.geometry.MultiPoint(points)
  if len(points) > 3:
    try:
      shaper = Alpha_Shaper(points)
      boundary = shaper.get_shape(5)
      boundary_json = shapely.geometry.mapping(boundary)
    except:
      print('Error in alpha shape for region_id', group[0])
      boundary, boundary_json = None, None
  else:
    boundary, boundary_json = None, None
  neighborhood = {
    'region_id': group[0],
    'scatter': scatter,
    'boundary': boundary,
    'scatter_json': shapely.geometry.mapping(scatter),
    'boundary_json': boundary_json,
  }
  neighborhoods.append(neighborhood)
display(neighborhoods[0]['scatter'])
display(neighborhoods[0]['boundary'])

# %%
def random_color(i = 4253766):
  if i == -1:
    return "#ccc"
  if i == 'N/A':
    return '#ccc'
  random.seed(i)
  r = lambda: random.randint(0, 255)
  return '#%02X%02X%02X' % (r(), r(), r())

# %%
display(neighborhoods[7]['scatter_json'])
display(neighborhoods[7]['boundary_json'])

# %%
shapely.to_geojson(neighborhoods[0]['scatter'])

# %%
neighborhoods_json = [{'region_id': n['region_id'], 'scatter': n['scatter_json'], 'boundary': n['boundary_json']} for n in neighborhoods]
# dump to json
# with open('../data/final/neighborhood_boundary.json', 'w') as f:
#   json.dump(neighborhoods_json, f)
  
scatter_geojson = {
  'type': 'FeatureCollection',
  'features': [{
    'type': 'Feature',
    'geometry': n['scatter_json'],
    'properties': {'region_id': n['region_id'], 'color': random_color(n['region_id'])}
  } for n in neighborhoods]
}
with open('../data/final/neighborhood_scatter.geojson', 'w') as f:
  json.dump(scatter_geojson, f)
  
boundary_geojson = {
  'type': 'FeatureCollection',
  'features': [{
    'type': 'Feature',
    'geometry': n['boundary_json'],
    'properties': {'region_id': n['region_id'], 'color': random_color(n['region_id'])}
  } for n in neighborhoods if n['boundary_json'] is not None]
}
# with open('../data/final/neighborhood_boundary.geojson', 'w') as f:
#   json.dump(boundary_geojson, f)

# %%
# sort neighborhoods by size
neighborhoods_by_size = sorted(neighborhoods, key=lambda x: len(x['scatter'].geoms), reverse=True)
neighborhoods_by_size = [{'region_id': n['region_id'], 'boundary': n['boundary']} for n in neighborhoods_by_size]
neighborhoods_by_size

# neighborhoods with boundary
neighborhoods_by_size = [n for n in neighborhoods_by_size if (n['boundary'] is not None) and not n['boundary'].is_empty]
for n in neighborhoods_by_size:
  n['boundary_json'] = shapely.geometry.mapping(n['boundary'])

# subtract larger neighborhoods from all smaller neighborhoods
for i, n in enumerate(neighborhoods_by_size):
  for j in range(i+1, len(neighborhoods_by_size)):
    n['boundary'] = n['boundary'].difference(neighborhoods_by_size[j]['boundary'])
    n['boundary_json'] = shapely.geometry.mapping(n['boundary'])

# %%
# with open('../data/final/neighborhood_boundary_subtracted.geojson', 'w') as f:
#   json.dump({
#     'type': 'FeatureCollection',
#     'features': [{
#       'type': 'Feature',
#       'geometry': n['boundary_json'],
#       'properties': {'region_id': n['region_id'], 'color': random_color(n['region_id'])}
#     } for n in neighborhoods_by_size]
#   }, f)

# %%
neighborhoods_by_size


