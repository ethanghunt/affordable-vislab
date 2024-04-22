# %%
import pandas as pd
import geopandas as gpd
import shapely
import numpy as np

# %%


# %%
df = pd.read_csv('../data/zillow_all_offmarket-atlanta-with-walk-scores.csv')
df = df[['propertyId', 'address_city', 'address_county', 'address_zip', 'latitude', 'longitude']]
clean_df = df.dropna()
clean_df.to_csv('../data/properties.csv', index=False)

# %%
clean_df

# %%
city_geo_df = pd.read_pickle('../data/city_geometries_df.pkl')
city_geo_df

# %%
neighborhood_df = gpd.read_file('../data/Official_Neighborhoods.geojson')
neigh_df = neighborhood_df[['OBJECTID', 'NAME', 'geometry']]

# %%
for i, row in clean_df.iterrows():
    point = shapely.geometry.Point(row['longitude'], row['latitude'])
    for j, neigh in neigh_df.iterrows():
        if neigh['geometry'].contains(point):
            clean_df.at[i, 'neighborhood'] = neigh['NAME']

# %%
clean_df.to_csv('../data/properties_with_neighborhoods.csv', index=False)

# %%
for i, row in clean_df.iterrows():
    for j, city in city_geo_df.iterrows():
        if city['geometry'].contains(shapely.geometry.Point(row['longitude'], row['latitude'])):
            clean_df.at[i, 'city'] = city['name']

# %%
clean_df.to_csv('../data/properties_with_neighborhoods_and_cities.csv', index=False)

# %%
clean_df['neighborhood'] = clean_df['neighborhood'].str.lower()
clean_df['city'] = clean_df['city'].str.lower()
clean_df['address_city'] = clean_df['address_city'].str.lower()
clean_df['address_county'] = clean_df['address_county'].str.lower()
clean_df

# %%
df = pd.read_csv('../data/properties_with_neighborhoods_and_cities.csv')

# %%
df

# %%
df.rename(columns={'city': 'found_city'}, inplace=True)
df['address_city'] = df['address_city'].str.lower()
df['address_county'] = df['address_county'].str.lower()
df['neighborhood'] = df['neighborhood'].str.lower()
df['accepted_city'] = df['found_city'].fillna(df['address_city'])

subdf = df[df['accepted_city'] == 'atlanta']
subdf = subdf[subdf['neighborhood'].isnull()]
subdf['clusters'] = hdbscan.fit_predict(subdf[['longitude', 'latitude']])
subdf['neighborhood'] = subdf['clusters'].apply(lambda x: f"cluster_{x}")

for i, row in subdf.iterrows():
    df.at[i, 'neighborhood'] = row['neighborhood']

df['region_id'] = df.apply(lambda x: f"{x['neighborhood']}_{x['accepted_city']}", axis=1)

df

# %%
df[df['region_id'] == 'nan_atlanta']

# %%
df.to_csv('../data/my_props.csv', index=False)

# %%
df.drop(df[~df['region_id'].str.contains('nan_atlanta')].index, inplace=True)
df

# %%
from sklearn.cluster import HDBSCAN
hdbscan = HDBSCAN(min_cluster_size=100)
df['cluster'] = hdbscan.fit_predict(df[['longitude', 'latitude']])
df['neighborhood'] = df['cluster'].apply(lambda x: f'aux_{x}' if x != -1 else np.nan)

# %%
mydf = df.drop(df[df['cluster'] == -1].index)
mydf

# %%
# import knn
from sklearn.neighbors import KNeighborsClassifier
df = pd.read_csv('../data/my_props.csv')
# train classifier on all data not in cluster_-1_atlanta region
knn = KNeighborsClassifier(n_neighbors=1)
train = df[df['region_id'] != 'cluster_-1_atlanta']
knn.fit(train[['longitude', 'latitude']], train['region_id'])
predict = df[df['region_id'] == 'cluster_-1_atlanta']
predict['region_id'] = knn.predict(predict[['longitude', 'latitude']])
predict

for i, row in predict.iterrows():
    df.at[i, 'region_id'] = row['region_id']
df.to_csv('../data/my_props.csv', index=False)


# %%
# for city in df['accepted_city'].unique():
#     if city == 'atlanta':
#         continue
#     print(city)
#     print(df[df['accepted_city'] == city]['region_id'].unique())

ok_cities = df.groupby('accepted_city').count().sort_values('propertyId', ascending=False)[0:28].index.tolist()
df = df[df['accepted_city'].isin(ok_cities)]
df.to_csv('../data/my_props.csv', index=False)

# %%
from alpha_shapes import Alpha_Shaper
from polylabel import polylabel

df = pd.read_csv('../data/my_props.csv')

df['region_center'] = np.nan
df['region_shape'] = np.nan

region_ids = df['region_id'].unique()

for region_id in region_ids:
    subdf = df[df['region_id'] == region_id]
    coords = df.apply(lambda x: (x['longitude'], x['latitude']), axis=1).tolist()
    shaper = Alpha_Shaper(coords)
    shape = shaper.get_shape(2)
    try:
        shape_coords = [list(coord) for coord in shape.exterior.coords]
    except AttributeError:
        print(region_id)
        print(shape)
        continue
    center = polylabel([shape_coords])
    for i, row in subdf.iterrows():
        df.at[i, 'region_center'] = center
        df.at[i, 'region_shape'] = shape
df

# %%
df.to_pickle('../data/my_props.pkl')



# %%
df[~df['region_center'].isnull()]

# %%
import pandas as pd

# Load the first CSV file
df1 = pd.read_csv('../data/updated_data-3.csv', low_memory=False)

# Load the second CSV file
df2 = pd.read_csv("../data/zillow_all_offmarket-atlanta-with-walk-score4.csv", low_memory=False)

# Merge the DataFrames on the 'PropertyID' column
merged_df = pd.merge(df1, df2[['propertyId', 'PredictedSoldPrice']], on='propertyId', how='left')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('../data/merged_file_2.csv', index=False)


