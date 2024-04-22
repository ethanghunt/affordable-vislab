import pandas as pd

# Load the first dataset zillow_all_active_atlantas4 zillow_sold_atlantas3  zillow_all_offmarket-atlanta-with-walk-score4
property_data = pd.read_csv("zillow_all_offmarket-atlanta-with-walk-score3.csv", low_memory=False)

# Load the second dataset, ensure you have the right file path
income_data = pd.read_csv("final_joined_dataset.csv", low_memory=False)

# Merge the datasets on 'region_id'
merged_data = pd.merge(property_data, income_data, on='region_id', how='left')

# Check the first few rows to confirm merge was successful
print(merged_data.head())

# Save the merged dataframe to a new CSV file if needed
merged_data.to_csv("zillow_all_offmarket-atlanta-with-walk-score4.csv", index=False)
