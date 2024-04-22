from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
import random
import json

app = FastAPI()

app.mount('/public', StaticFiles(directory='public'), name='public')

city_map = {
  'avondale est': 'avondale estates',
  'east pt': 'east point',
  'lithia spgs': 'lithia springs',
}

def random_color(i = 4253766):
  if i == -1:
    return "#ccc"
  if i == 'N/A':
    return '#ccc'
  random.seed(i)
  r = lambda: random.randint(0, 255)
  return '#%02X%02X%02X' % (r(), r(), r())

def decile_color(decile, base_rgb = (146, 60, 58)):
  difference_interval = 30
  if decile == None:
    return '#ccc'
  rgb = [int(x - (decile - 5) * difference_interval) for x in base_rgb]
  return 'rgb' + str(tuple(rgb))

def clean_region_name(region_id):
  if region_id[:4] == 'nan_':
    region_id = region_id[4:]
  region_name = region_id.title()
  region_name = region_name.replace('_', ' ')
  return region_name

@app.get("/")
async def root():
  return FileResponse('views/index.html')

@app.get("/contact")
async def contact():
  return FileResponse('views/contact.html')


@app.get('/neighborhoods')
async def official_neighborhoods():
  
  props = pd.read_csv('data/final/properties.csv')
  props.rename(columns={'latitude': 'lat', 'longitude': 'lng'}, inplace=True)

  with open('data/final/region_stats.json', 'r') as f:
    region_stats = json.load(f)
  
  for region_stat in region_stats:
    for stat in region_stat:
      if region_stat[stat] == 'NaN':
        region_stat[stat] = None
    region_stat['color'] = decile_color(region_stat['Sold Price Quartile'])
  
  region_stats = {
    region_stat['region_id']: region_stat for region_stat in region_stats
  }
  
  point_list = []
  for i, row in props.iterrows():
    point = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [row['lng'], row['lat']]
      },
      "properties": {
        "region_id": row['region_id'],
        "color": region_stats.get(row['region_id'], {}).get('color', '#ccc'),
        "opacity": 0.5
      }
    }
    point_list.append(point)
    points = {
    "type": "FeatureCollection",
    "features": point_list
  }
  
  with open('data/final/neighborhood_boundary_subtracted.geojson', 'r') as f:
    subtracted_boundaries = json.load(f)
  
  for i, feature in enumerate(subtracted_boundaries['features']):
    region_id = feature['properties']['region_id']
    feature['id'] = region_id
    additional_features = {
      'color': region_stats[region_id]['color'],
      'name': clean_region_name(region_id),
      'price_level': region_stats[region_id]['Average Price Level'],
      'doordash_rating': region_stats[region_id]['Doordash Rating'],
      'sold_price': region_stats[region_id]['Sold Price'],
      'hai': region_stats[region_id]['HAI'],
      'sold_price_quartile': region_stats[region_id]['Sold Price Quartile'],
      'doordash_rating_quartile': region_stats[region_id]['Doordash Rating Quartile'],
      'school_rating': region_stats[region_id]['School Ratings'],
      'school_rating_quartile': region_stats[region_id]['School Ratings Quartile'],
    }
    feature['properties'].update(additional_features)

  return {
    "houses": points,
    "subtracted_boundaries": subtracted_boundaries
  }

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000)
