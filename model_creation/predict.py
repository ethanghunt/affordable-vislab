import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split

# Load your training dataset
train_data = pd.read_csv("zillow_sold_atlantas4.csv", low_memory=False)

# Handle mixed data types and missing values
numeric_cols = train_data.select_dtypes(include=[np.number])
non_numeric_cols = train_data.select_dtypes(exclude=[np.number])
train_data[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
train_data[non_numeric_cols.columns] = non_numeric_cols.fillna('Unknown')  

# Define the top 15 variables
top_variables = ['newConstruction', 'propertyTaxRate', 'bathroomCount', 'levels', 'bedroomCount', 
                 'taxes_year_1', 'hasFireplace', 'Average Price Level', 'taxes_year_2', 'schools_distance_2',
                 'schools_type_2', 'schools_rating_2', 'parkingCapacity', 'schools_rating_1', 'schools_type_1']

# Convert columns that should be numeric but are object due to mixed types
for col in ['propertyTaxRate', 'Average Price Level']:
    train_data[col] = pd.to_numeric(train_data[col], errors='coerce')

# Fill NaN values again for newly converted numeric columns if any NaNs were introduced
train_data.fillna(train_data.mean(), inplace=True)

# Split the data into features (X) and target variable (y)
X_train = train_data[top_variables]
y_train = train_data["soldPrice"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Train your OLS model using the training set
X_train = sm.add_constant(X_train) 
ols_model = sm.OLS(y_train, X_train).fit()

# Evaluate the model using the testing set
X_test = sm.add_constant(X_test) 
predictions = ols_model.predict(X_test)

# Assess the performance of the model (e.g., calculate R-squared)
r_squared = ols_model.rsquared
print(f"R-squared for the model: {r_squared}")

# Load dataset
df_417 = pd.read_csv("all_data.csv")
df_417.fillna(train_data.mean(), inplace=True)  # Impute using the training data's mean values

# Convert 'propertyTaxRate' column to numeric, replacing non-numeric values with NaN
df_417['propertyTaxRate'] = pd.to_numeric(df_417['propertyTaxRate'], errors='coerce')

# Impute missing values in 'propertyTaxRate' column with the mean
mean_property_tax_rate = df_417['propertyTaxRate'].mean()
df_417['propertyTaxRate'].fillna(mean_property_tax_rate, inplace=True)

# Extract features from the 417 dataset
X_417 = df_417[top_variables] 

# Add the constant term for OLS prediction
X_417 = sm.add_constant(X_417)

# Predict outcomes using the trained model
predictions_417 = ols_model.predict(X_417)
predictions_417 = np.maximum(predictions_417, 0)  # Ensure no negative predictions

# Add the predictions as a new column to the 417 dataset DataFrame
df_417["PredictedSoldPrice"] = predictions_417

# Save the updated DataFrame with predictions to a new CSV file
df_417.to_csv("predicted_values.csv", index=False)
