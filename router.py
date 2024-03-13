from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
from sklearn.cluster import HDBSCAN
from alpha_shapes import Alpha_Shaper
import random
from polylabel import polylabel
import json

ALPHA = 0.5
MIN_CLUSTER_SIZE = 10

hdbscan = HDBSCAN(min_cluster_size=MIN_CLUSTER_SIZE, cluster_selection_method='leaf')

app = FastAPI()

app.mount('/public', StaticFiles(directory='public'), name='public')

def random_color(i = 4253766):
  if i == -1:
    return "#ddd"
  random.seed(i)
  r = lambda: random.randint(0, 255)
  return '#%02X%02X%02X' % (r(), r(), r())

@app.get("/")
async def root():
  return FileResponse('views/index.html')

@app.get("/contact")
async def contact():
  return FileResponse('views/contact.html')

@app.get("/features")
async def generate_features():
  features_out = {}
  
  # Test dataset
  # data = pd.read_csv("public/data/mockdata.csv")
  
  # Atlanta dataset
  data = pd.read_csv("public/data/zillow_all_active_atlanta.csv")
  data = data.rename(columns={'latitude': 'lat', 'longitude': 'lng'})
  
  data = data.drop_duplicates(subset=['lng', 'lat'])
  data = data.dropna(subset=['lng', 'lat'])
  data = data.fillna('N/A')
  
  data['cluster'] = hdbscan.fit_predict(data[['lng', 'lat']])
  
  # generate points
  point_list = []
  for i, row in data.iterrows():
    point = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [row['lng'], row['lat']]
      },
      "properties": {
        "cluster": row['cluster'],
        "color": random_color(row['cluster'])
      }
    }
    point_list.append(point)
  features_out['points'] = {
    "type": "FeatureCollection",
    "features": point_list
  }
  
  polygon_list = []
  center_list = []
  cluster_data = {}
  cluster_group_df = data.groupby('cluster')
  for cluster, cluster_df in cluster_group_df:
    if cluster == -1:
      continue
    
    cluster_data[cluster] = cluster_df.to_dict(orient='records')
    
    coords = cluster_df.apply(lambda x: (x['lng'], x['lat']), axis=1).tolist()
    if len(coords) < 3:
      continue
    shaper = Alpha_Shaper(coords)
    alpha_shape = shaper.get_shape(ALPHA)
    alpha_shape_coords = [list(coord) for coord in alpha_shape.exterior.coords]
    center_point = polylabel([alpha_shape_coords])
    center = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [float(center_point[0]), float(center_point[1])]
      },
      "properties": {
        "cluster": cluster,
        "color": random_color(cluster)
      }
    }
    center_list.append(center)
    polygon = {
      "type": "Feature",
      "properties": {
        "cluster": cluster,
        "color": random_color(cluster)
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          alpha_shape_coords
        ]
      }
    }
    polygon_list.append(polygon)
  features_out['centers'] = {
    "type": "FeatureCollection",
    "features": center_list
  }
  features_out['shapes'] = {
    "type": "FeatureCollection",
    "features": polygon_list
  }
  return {
    "features": features_out,
    "cluster_data": cluster_data
  }

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000)
