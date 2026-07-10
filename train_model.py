import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_and_save_model():
    # Load dataset
    data_path = os.path.join("data", "train.csv")
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}. Please run download_data.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Drop Loan_ID as it is not a feature
    if 'Loan_ID' in df.columns:
        df = df.drop(columns=['Loan_ID'])

    print("Initial Data Shape:", df.shape)

    # Define columns
    numerical_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
    categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Credit_History', 'Property_Area']
    target_col = 'Loan_Status'

    # 1. Handling Missing Values
    # Impute numerical columns using mean
    for col in numerical_cols:
        if col in df.columns:
            mean_val = df[col].mean()
            df[col] = df[col].fillna(mean_val)
            print(f"Imputed numerical '{col}' missing values with mean: {mean_val:.2f}")

    # Impute categorical columns using mode
    imputation_defaults = {}
    for col in categorical_cols:
        if col in df.columns:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            imputation_defaults[col] = mode_val
            print(f"Imputed categorical '{col}' missing values with mode: {mode_val}")

    # Save imputation defaults for web app reference (if needed, though form guarantees input)
    # We can store them in a dictionary
    
    # 2. Encoding Categorical Variables
    # We use mapping to ensure consistency between training and prediction
    mapping = {
        'Gender': {'Male': 1, 'Female': 0},
        'Married': {'Yes': 1, 'No': 0},
        'Dependents': {'0': 0, '1': 1, '2': 2, '3+': 3},
        'Education': {'Graduate': 1, 'Not Graduate': 0},
        'Self_Employed': {'Yes': 1, 'No': 0},
        'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2},
        'Loan_Status': {'Y': 1, 'N': 0}
    }

    # Map Dependents that might be numbers or strings
    df['Dependents'] = df['Dependents'].astype(str).str.replace('+', '', regex=False)
    df['Dependents'] = pd.to_numeric(df['Dependents'], errors='coerce').fillna(0).astype(int)

    # Map other categorical features
    for col, map_dict in mapping.items():
        if col in df.columns and col != 'Dependents':
            df[col] = df[col].map(map_dict)

    # Ensure Credit_History is integer/float
    df['Credit_History'] = df['Credit_History'].astype(float)

    # Check for any remaining NaNs
    if df.isnull().sum().sum() > 0:
        print("Warning: Remaining NaNs found in dataframe:")
        print(df.isnull().sum())
        df = df.dropna()

    # Split features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    print("\nFeature Columns:", X.columns.tolist())
    print("Processed Dataset Preview:")
    print(X.head())

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print(f"\nTrain shape: {X_train.shape}, Test shape: {X_test.shape}")

    # Initialize models
    models = {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.08,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
    }

    results = {}
    best_model_name = None
    best_test_acc = 0.0

    print("\n--- Model Training & Evaluation ---")
    for name, model in models.items():
        model.fit(X_train, y_train)
        
        train_preds = model.predict(X_train)
        test_preds = model.predict(X_test)
        
        train_acc = accuracy_score(y_train, train_preds)
        test_acc = accuracy_score(y_test, test_preds)
        
        results[name] = {
            "train_accuracy": train_acc,
            "test_accuracy": test_acc,
            "model_object": model
        }
        
        print(f"\n{name} Classifier:")
        print(f"  Training Accuracy: {train_acc * 100:.2f}%")
        print(f"  Testing Accuracy:  {test_acc * 100:.2f}%")
        
        # We save XGBoost specifically, but let's check which is best
        if name == "XGBoost":
            best_model_name = name

    # Serializing the XGBoost model as requested (XGBoost is the best-performing model mentioned)
    best_model = results["XGBoost"]["model_object"]
    
    # Save the model and feature names to a pickle file
    model_data = {
        "model": best_model,
        "feature_names": X.columns.tolist(),
        "mappings": mapping
    }
    
    model_path = "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model_data, f)
        
    print(f"\nSaved XGBoost model metadata to '{model_path}' successfully!")

if __name__ == "__main__":
    train_and_save_model()
