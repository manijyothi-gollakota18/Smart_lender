import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Load the saved model and feature mappings
MODEL_PATH = "model.pkl"
model_data = None

def load_model():
    global model_data
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                model_data = pickle.load(f)
            print("Successfully loaded model from model.pkl")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print(f"Warning: model.pkl not found. Please run train_model.py first.")

# Load model on startup
load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global model_data
    if request.method == 'POST':
        # Ensure model is loaded; try reloading if None
        if model_data is None:
            load_model()
            if model_data is None:
                return "Error: Machine learning model is not trained/loaded. Please run training script first.", 500
                
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

            # Map the categories to matches used during training
            mappings = model_data['mappings']
            
            gender_num = mappings['Gender'].get(gender, 1)
            married_num = mappings['Married'].get(married, 1)
            dependents_num = int(dependents.replace('+', '')) if dependents else 0
            education_num = mappings['Education'].get(education, 1)
            self_employed_num = mappings['Self_Employed'].get(self_employed, 0)
            property_area_num = mappings['Property_Area'].get(property_area, 1)

            # Build prediction dataframe with exact matching feature names and ordering
            features_dict = {
                'Gender': [gender_num],
                'Married': [married_num],
                'Dependents': [dependents_num],
                'Education': [education_num],
                'Self_Employed': [self_employed_num],
                'ApplicantIncome': [applicant_income],
                'CoapplicantIncome': [coapplicant_income],
                'LoanAmount': [loan_amount],
                'Loan_Amount_Term': [loan_term],
                'Credit_History': [credit_history],
                'Property_Area': [property_area_num]
            }
            
            features_df = pd.DataFrame(features_dict)
            
            # Predict
            model = model_data['model']
            prediction = model.predict(features_df)[0]
            
            # Get probability scores
            try:
                probabilities = model.predict_proba(features_df)[0]
                confidence = float(probabilities[prediction])
            except Exception:
                confidence = 1.0

            # Prediction outcome: 1 is eligible (Y), 0 is ineligible (N)
            eligible = bool(prediction == 1)

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
