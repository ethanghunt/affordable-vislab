import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load and preprocess the data
df = pd.read_csv("zillow_sold_atlantas4.csv", low_memory=False)
df['soldDate'] = pd.to_datetime(df['soldDate'])

df['month'] = df['soldDate'].dt.month
df['day'] = df['soldDate'].dt.day
df['year'] = df['soldDate'].dt.year

df.drop('soldDate', axis=1, inplace=True)

df.sort_values(by='year', inplace=True)  # Sorting by year 
df = df.dropna(thresh=0.6*len(df), axis=1)  # Drop columns with less than 60% data
df = pd.get_dummies(df, drop_first=True)  # Convert categorical to dummy variables

# Define features and target
X = df.drop('soldPrice', axis=1)  
y = df['soldPrice']

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, shuffle=False)

# Model fitting
lasso = LassoCV(cv=TimeSeriesSplit(n_splits=5))
ridge = RidgeCV(cv=TimeSeriesSplit(n_splits=5))
rf = RandomForestRegressor(n_estimators=100)

lasso.fit(X_train, y_train)
ridge.fit(X_train, y_train)
rf.fit(X_train, y_train)

# Output feature names for clarity in the output
feature_names = X.columns

# Feature importances from Random Forest
importances_rf = rf.feature_importances_
important_features_rf = feature_names[importances_rf > np.mean(importances_rf)]
print(f"Important features by Random Forest: {important_features_rf.tolist()}")

# Coefficients from LASSO and Ridge
coefficients_lasso = lasso.coef_
important_features_lasso = feature_names[coefficients_lasso != 0]
print(f"Important features by LASSO: {important_features_lasso.tolist()}")

coefficients_ridge = ridge.coef_
threshold_ridge = np.quantile(np.abs(coefficients_ridge), 0.75)
important_features_ridge = feature_names[np.abs(coefficients_ridge) > threshold_ridge]
print(f"Important features by Ridge: {important_features_ridge.tolist()}")

# Print R^2 and MSE for each model
print("Lasso R^2:", r2_score(y_test, lasso.predict(X_test)))
print("Ridge R^2:", r2_score(y_test, ridge.predict(X_test)))
print("Random Forest R^2:", r2_score(y_test, rf.predict(X_test)))
print("Lasso MSE:", mean_squared_error(y_test, lasso.predict(X_test)))
print("Ridge MSE:", mean_squared_error(y_test, ridge.predict(X_test)))
print("Random Forest MSE:", mean_squared_error(y_test, rf.predict(X_test)))
