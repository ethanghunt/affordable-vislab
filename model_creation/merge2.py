import pandas as pd

# Load existing data with property details
property_data = pd.read_csv(
    "zillow_all_active_atlantas2.csv",
    low_memory=False
)
# Load the data containing region specifics like parks count, restaurants count, etc.
additional_data = pd.read_csv("places_count_with_address_4_2.csv")
# Merge the dataframes on 'region_id'
merged_data = pd.merge(property_data, additional_data, on='region_id', how='left')

merged_data.to_csv("zillow_all_active_atlantas3", index=False)
