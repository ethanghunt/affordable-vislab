from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import pandas as pd
from sklearn.cluster import HDBSCAN
from alpha_shapes import Alpha_Shaper
import random

ALPHA = 1

app = FastAPI()

app.mount('/public', StaticFiles(directory='public'), name='public')

def random_color(i = 4253766):
  if i == -1:
    return "#eee"
  random.seed(i)
  r = lambda: random.randint(0, 255)
  return '#%02X%02X%02X' % (r(), r(), r())

@app.get("/features")
async def generate_features():
  features_out = {}
  data = pd.read_csv("public/mockdata.csv")
  data = data.drop_duplicates(subset=['lng', 'lat'])
  hdbscan = HDBSCAN(min_cluster_size=5, cluster_selection_method='leaf')
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
  cluster_group_df = data.groupby('cluster')
  for cluster, cluster_df in cluster_group_df:
    if cluster == -1:
      continue
    coords = cluster_df.apply(lambda x: (x['lng'], x['lat']), axis=1).tolist()
    shaper = Alpha_Shaper(coords)
    alpha_shape = shaper.get_shape(ALPHA)
    alpha_shape = pd.DataFrame(alpha_shape.exterior.coords.xy).T.rename(columns={0: 'lng', 1: 'lat'})
    polygon = {
      "type": "Feature",
      "properties": {
        "cluster": cluster,
        "color": random_color(cluster)
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          alpha_shape.values.tolist()
        ]
      }
    }
    polygon_list.append(polygon)
  features_out['shapes'] = {
    "type": "FeatureCollection",
    "features": polygon_list
  }
  return features_out

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000)
