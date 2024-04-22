import pandas as pd
import numpy as np
import joblib

# Load the trained Ridge model
ridge_model = joblib.load('ridge_model.pkl')

# Load the starting test CSV
starting_test_csv_path = "full_dataset.csv"
df_test = pd.read_csv(starting_test_csv_path)

# Load imputer and encoder from disk
imputer = joblib.load('imputer.pkl')
encoder = joblib.load('encoder.pkl')

# Select top 15 features based on Ridge model
feature_names = df_test.drop(columns=['soldPrice']).columns.tolist()
ridge_model_estimator = ridge_model.named_steps['model']  
ridge_coefs_abs = np.abs(ridge_model_estimator.coef_)
feature_coefs = list(zip(feature_names, ridge_coefs_abs))
top_features = [feature for feature, coef in sorted(feature_coefs, key=lambda x: x[1], reverse=True)[:15]]

df_test_selected_features = df_test[top_features]

numeric_imputed = imputer.transform(df_test_selected_features.select_dtypes(include=np.number))

categorical_cols = df_test_selected_features.select_dtypes(exclude=[np.number]).astype(str)
categorical_encoded = encoder.transform(categorical_cols)

X_test = np.concatenate([numeric_imputed, categorical_encoded.toarray()], axis=1)

y_pred_ridge = ridge_model.predict(X_test)

df_test['Ridge_Predictions'] = y_pred_ridge

# Save the predictions to a new CSV file
output_file_path = "All_Predictions_Ridge.csv"
df_test.to_csv(output_file_path, index=False)

print("Predictions saved to:", output_file_path)
