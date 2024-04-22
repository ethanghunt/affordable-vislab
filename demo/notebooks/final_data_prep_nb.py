# %%
import pandas as pd
import numpy as np
import json

# %%
df = pd.read_csv('../data/merged_file_2.csv')

# %%
for col in df.columns:
  print(col)

apls = df['Average Price Level'].dropna()
deciles = np.percentile(apls, np.arange(0, 100, 10))
quartiles = np.percentile(apls, np.arange(0, 100, 25))

# assign price decile to each row
df['Price Quartile'] = np.digitize(df['Average Price Level'], quartiles)

df['Price Decile'] = np.digitize(df['Average Price Level'], deciles)
df['Price Decile']

# %%
region_stats = []

for group in df.groupby('region_id'):
  region_id = group[0]
  region_df = group[1]
  apl = region_df['Average Price Level'].dropna().mean()
  ddr = region_df['Doordash Restaurants above 4.5 and 1-2 $'].dropna().mean()
  sold_price = region_df['PredictedSoldPrice'].dropna().median()
  school_ratings = region_df['schools_rating_1'].dropna().mean()

  region_stats.append({
    'region_id': region_id,
    'Average Price Level': float(apl),
    'Doordash Rating': float(ddr),
    'Sold Price': float(sold_price),
    'HAI': float(19168394.5/sold_price) if not np.isnan(sold_price) and sold_price != 0 else np.nan,
    'School Ratings': float(school_ratings) if not np.isnan(school_ratings) else np.nan
  })

sps = [region_stat['Sold Price'] for region_stat in region_stats]
apls = [region_stat['Average Price Level'] for region_stat in region_stats]
ddrs = [region_stat['Doordash Rating'] for region_stat in region_stats]
schrs = [region_stat['School Ratings'] for region_stat in region_stats]

sps = [sp for sp in sps if not np.isnan(sp)]
apls = [apl for apl in apls if not np.isnan(apl)]
ddrs = [ddr for ddr in ddrs if not np.isnan(ddr)]
schrs = [schr for schr in schrs if not np.isnan(schr)]

sp_quartiles = np.percentile(sps, np.arange(0, 100, 25))
ddr_quartiles = np.percentile(ddrs, np.arange(0, 100, 25))
apls_quartiles = np.percentile(apls, np.arange(0, 100, 25))
schrs_quartiles = np.percentile(schrs, np.arange(0, 100, 25))

for region_stat in region_stats:
  region_stat['Sold Price Quartile'] = int(np.digitize(region_stat['Sold Price'], sp_quartiles)) if not np.isnan(region_stat['Sold Price']) else np.nan
  region_stat['Doordash Rating Quartile'] = int(np.digitize(region_stat['Doordash Rating'], ddr_quartiles)) if not np.isnan(region_stat['Doordash Rating']) else np.nan
  region_stat['Average Price Level Quartile'] = int(np.digitize(region_stat['Average Price Level'], apls_quartiles)) if not np.isnan(region_stat['Average Price Level']) else np.nan
  region_stat['School Ratings Quartile'] = int(np.digitize(region_stat['School Ratings'], schrs_quartiles)) if not np.isnan(region_stat['School Ratings']) else np.nan
  
with open('../data/region_stats.json', 'w') as f:
  json.dump(region_stats, f)

# %%
sp_quartiles

# %%
df[df['region_id'] == 'nan_sandy springs']['Average Price Level']

# %%
apl_map = {r['region_id']: int(r['Price Decile']) for r in region_prices}

# save apl_map to json
with open('../data/apl_map.json', 'w') as f:
  json.dump(apl_map, f)

# %%
def decile_to_color(decile):
  base_rgb = (146, 60, 58)
  rgb = [int(x - (decile - 5) * 10) for x in base_rgb]
  return 'rgb' + str(tuple(rgb))
decile_to_color(1)


