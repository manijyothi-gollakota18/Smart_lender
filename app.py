import os
import json
import numpy as np
import xgboost as xgb
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Paths for the saved XGBoost booster and metadata
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.json")
METADATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata.json")

bst = None
metadata = None

def load_model():
    global bst, metadata
    if os.path.exists(MODEL_PATH) and os.path.exists(METADATA_PATH):
        try:
            bst = xgb.Booster()
            bst.load_model(MODEL_PATH)
            with open(METADATA_PATH, "r") as f:
                metadata = json.load(f)
            print("Successfully loaded native XGBoost model and metadata.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Warning: model.json or metadata.json not found. Run train_model.py first.")

# Load model on startup
load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global bst, metadata
    if request.method == 'POST':
        # Ensure model and metadata are loaded; try reloading if None
        if bst is None or metadata is None:
            load_model()
            if bst is None or metadata is None:
                return "Error: Machine learning model is not trained/loaded.", 500
                
        try:
            # Retrieve values from POST form request
            gender = request.form.get('gender')
            married = request.form.get('married')
            dependents = request.form.get('dependents')
            education = request.form.get('education')
            self_employed = request.form.get('self_employed')
            applicant_income = float(request.form.get('applicant_income', 0))
            coapplicant_income = float(request.form.get('coapplicant_income', 0))
            loan_amount = float(request.form.get('loan_amount', 0))
            loan_term = float(request.form.get('loan_term', 360))
            credit_history = float(request.form.get('credit_history', 1.0))
            property_area = request.form.get('property_area')

            # Build dict for display back on the results page
            input_data = {
                'gender': gender,
                'married': married,
                'dependents': dependents,
                'education': education,
                'self_employed': self_employed,
                'applicant_income': applicant_income,
                'coapplicant_income': coapplicant_income,
                'loan_amount': loan_amount,
                'loan_term': loan_term,
                'credit_history': str(credit_history),
                'property_area': property_area
            }

            # Map the categories to numerical matches used during training
            mappings = metadata['mappings']
            
            gender_num = mappings['Gender'].get(gender, 1)
            married_num = mappings['Married'].get(married, 1)
            dependents_num = int(dependents.replace('+', '')) if dependents else 0
            education_num = mappings['Education'].get(education, 1)
            self_employed_num = mappings['Self_Employed'].get(self_employed, 0)
            property_area_num = mappings['Property_Area'].get(property_area, 1)

            # Build prediction features list in the exact order expected by the model
            feature_values = [
                gender_num,
                married_num,
                dependents_num,
                education_num,
                self_employed_num,
                applicant_income,
                coapplicant_income,
                loan_amount,
                loan_term,
                credit_history,
                property_area_num
            ]

            # Construct DMatrix directly from 2D array representation
            dmat = xgb.DMatrix([feature_values], feature_names=metadata['feature_names'])
            
            # Predict probability of approval (binary model outputs probability of class 1)
            prob = float(bst.predict(dmat)[0])
            
            # Prediction outcome: class 1 is Y (eligible), class 0 is N (declined)
            eligible = bool(prob >= 0.5)
            confidence = prob if eligible else (1.0 - prob)

            return render_template('result.html', eligible=eligible, confidence=confidence, input_data=input_data)

        except Exception as e:
            return f"An error occurred during prediction: {e}", 400

    # GET request: render the empty form page
    return render_template('predict.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
