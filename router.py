from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
from sklearn.cluster import HDBSCAN
import random
# from alpha_shapes import Alpha_Shaper
# from polylabel import polylabel
import json

ALPHA = 0.5
MIN_CLUSTER_SIZE = 10

hdbscan = HDBSCAN(min_cluster_size=MIN_CLUSTER_SIZE, cluster_selection_method='leaf')

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

@app.get("/")
async def root():
  return FileResponse('views/index.html')

@app.get("/contact")
async def contact():
  return FileResponse('views/contact.html')


@app.get('/neighborhoods')
async def official_neighborhoods():
  
  props = pd.read_csv('data/my_props_4.csv')
  props.rename(columns={'latitude': 'lat', 'longitude': 'lng'}, inplace=True)

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
        "color": random_color(row['region_id']),
        "opacity": 0.5
      }
    }
    point_list.append(point)
    points = {
    "type": "FeatureCollection",
    "features": point_list
  }
    
  with open('data/final/neighborhood_boundary.geojson', 'r') as f:
    boundaries = json.load(f)
  
  with open('data/final/neighborhood_boundary_subtracted.geojson', 'r') as f:
    subtracted_boundaries = json.load(f)

  return {
    "houses": points,
    "boundaries": boundaries,
    "subtracted_boundaries": subtracted_boundaries
  }

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000)
