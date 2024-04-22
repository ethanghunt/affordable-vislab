import pandas as pd
import numpy as np
from shapely.geometry import Point, box
import json

# Load CSV data
df = pd.read_csv("zillow_all_active_atlantas.csv", low_memory=False)

# Load JSON data
with open("neighborhoods.json", 'r') as f:
    regions = json.load(f)

# Prepare a dictionary of bounding boxes for each region
region_boxes = {}
for region in regions:
    coordinates = region['multipoint']['coordinates']
    min_lon = min(coord[0] for coord in coordinates)
    max_lon = max(coord[0] for coord in coordinates)
    min_lat = min(coord[1] for coord in coordinates)
    max_lat = max(coord[1] for coord in coordinates)
    region_boxes[region['region_id']] = box(min_lon, min_lat, max_lon, max_lat)

# Function to find the region by checking bounding boxes
def find_region(longitude, latitude):
    point = Point(longitude, latitude)
    for region_id, bbox in region_boxes.items():
        if bbox.contains(point):
            return region_id
    return None  

# Apply the function to each row in the DataFrame
df['region_id'] = df.apply(lambda row: find_region(row['longitude'], row['latitude']), axis=1)


# Save the modified DataFrame to a new CSV file
df.to_csv("zillow_all_active_atlantas2.csv", index=False)
