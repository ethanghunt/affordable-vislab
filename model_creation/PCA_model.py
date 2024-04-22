import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, RidgeCV, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Load and preprocess the data
df = pd.read_csv("zillow_sold_atlantas4.csv", low_memory=False)
df['soldDate'] = pd.to_datetime(df['soldDate'])

# Extract more features from 'soldDate'
df['month'] = df['soldDate'].dt.month
df['day'] = df['soldDate'].dt.day
df['year'] = df['soldDate'].dt.year

# Drop the original 'soldDate' column
df.drop('soldDate', axis=1, inplace=True)

# Sorting by year if it's a time series analysis
df.sort_values(by='year', inplace=True)

# Drop columns with less than 60% data
df = df.dropna(thresh=0.6*len(df), axis=1)

# Identify categorical and numerical columns
categorical_columns = df.select_dtypes(include=['object']).columns
numerical_columns = df.select_dtypes(exclude=['object']).columns

# One-hot encode categorical data
encoder = OneHotEncoder(drop='first')
encoded_categorical = encoder.fit_transform(df[categorical_columns])

# Assuming 'soldPrice' is the target variable and exists in df
if 'soldPrice' in df.columns and not df['soldPrice'].isnull().values.any():
    encoded_categorical_df = pd.DataFrame(encoded_categorical.toarray(), 
                                          columns=encoder.get_feature_names_out(categorical_columns))

    # Combine encoded categorical and numerical columns
    df_encoded = pd.concat([encoded_categorical_df, df[numerical_columns]], axis=1)

    # Define features and target
    X = df_encoded.drop('soldPrice', axis=1)
    y = df_encoded['soldPrice']

    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, shuffle=False)

    # Define the model pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),  # Standardize the features
        ("pca", PCA(n_components=0.95)),  # Retain 95% of variance
        ("regression", LinearRegression())  # Linear regression model
    ])

    # Fit the pipeline
    pipeline.fit(X_train, y_train)

    # Make predictions and evaluate the model
    predictions = pipeline.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)

    print("PCA Linear Regression R^2:", r2)
    print("PCA Linear Regression MSE:", mse)
else:
    print("Error: 'soldPrice' column is either missing or contains null values.")