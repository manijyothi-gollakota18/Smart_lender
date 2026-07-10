# Smart Lender: Loan Eligibility Prediction System

Smart Lender is a machine learning-powered web application designed to automate and accelerate the loan approval evaluation process for financial institutions. By leveraging classification algorithms (Decision Tree, Random Forest, K-Nearest Neighbors, and XGBoost), the system analyzes applicant demographics and financial metrics in real-time to predict the likelihood of loan repayment or default.

---

## 📂 Project Phases Directory

### 1. Brainstorming & Ideation
* **The Problem**: Manual credit underwriting is time-consuming, prone to human error, and slows down overall loan processing. This delay impacts customer satisfaction and operational efficiency, while poor decisions lead to Non-Performing Assets (NPAs).
* **The Solution**: An intelligent automation layer that analyzes applicant risk profiles.
* **Approach**: Train multiple classification algorithms on historic application decisions to model creditworthiness, serialize the best model (XGBoost), and build a premium, user-friendly interface for credit officers and analysts.

---

### 2. Requirement Analysis
* **Data Features Analyzed**:
  * Demographics: `Gender`, `Married`, `Dependents`, `Education`, `Self_Employed`, `Property_Area`.
  * Financials: `ApplicantIncome`, `CoapplicantIncome`, `LoanAmount` (in thousands), `Loan_Amount_Term` (in days).
  * History: `Credit_History` (1.0 = Clean record, 0.0 = Defaults or no record).
  * Target Class: `Loan_Status` (Y = Approved, N = Declined).
* **Operational Scenarios**:
  * **Scenario 1: Fast-Track Approval**: Salaried applicant with strong income and clean credit history gets instant approval without manual underwriting.
  * **Scenario 2: High-Risk Detection**: Self-employed applicant with high debt ratio and no credit history is flagged and declined, requiring manual audits.
  * **Scenario 3: Analyst Dashboard**: financial analysts batch-evaluate applicants and explore general data trends using visualizations.

---

### 3. Project Design Phase
* **System Architecture**:
  ```
  [User Browser] <---> [Flask Server (app.py)] <---> [Model Engine (model.pkl)]
                              |
                     [EDA Engine (eda.py)]
                              |
                    [Dataset (train.csv)]
  ```
* **Data Processing Rules**:
  * Imputation: Numerical features use **mean** method; categorical features use **mode** method.
  * Encoding: Categories are converted to numerical formats using custom dictionary mappings to ensure strict consistency between training and real-time inference.

---

### 4. Project Planning Phase
The project was executed through the following structured milestones:
1. **Milestone 1**: Project Environment Setup & dependency management.
2. **Milestone 2**: Ingestion of historical credit eligibility data.
3. **Milestone 3**: Exploratory Data Analysis & visual asset generation.
4. **Milestone 4**: Data Preprocessing, model training, hyperparameter tuning, and serialization.
5. **Milestone 5**: Backend Flask server implementation and HTML/CSS design.
6. **Milestone 6**: Functional verification and programmatic unit testing.
7. **Milestone 7**: Repository push and deployment packaging (Docker & Cloud manifests).

---

### 5. Project Development Phase
* **Models Evaluated**:
  * **Decision Tree Classifier**: Fast, interpretable tree-depth rules.
  * **Random Forest Classifier**: Robust ensemble bagger minimizing variance.
  * **K-Nearest Neighbors (KNN)**: Distance-based cluster evaluation.
  * **XGBoost Classifier**: Gradient boosted decision tree offering state-of-the-art accuracy.
* **Leaderboard Summary**:
  * *XGBoost*: **94.70% Training Accuracy** | **81.30% Testing Accuracy** (Selected for Production)
  * *Random Forest*: 82.48% Training Accuracy | 85.37% Testing Accuracy
  * *Decision Tree*: 82.48% Training Accuracy | 82.11% Testing Accuracy
  * *K-Nearest Neighbors*: 70.47% Training Accuracy | 66.67% Testing Accuracy

---

### 6. Project Testing
* **Programmatic Test Script** (`verify_scenarios.py`):
  * Automated endpoint query assertion (GET/POST validation checks).
  * Validated that the **Low-Risk Fast-Track preset** correctly generates a `LOAN ELIGIBLE` outcome.
  * Validated that the **High-Risk preset** correctly generates a `LOAN DECLINED` outcome.
* **Test Status**: All verification assertions passed successfully (HTTP 200 checks).

---

### 7. Project Documentation
The project structure consists of the following key files:
* `app.py`: Serving Flask application logic.
* `train_model.py`: Missing values handler and classifier trainer.
* `eda.py`: Matplotlib/Seaborn visualization generator.
* `verify_scenarios.py`: Integration testing script.
* `static/css/style.css`: Glassmorphic, modern dark theme layout.
* `templates/`: Layout views (`base.html`, `index.html`, `predict.html`, `result.html`, `insights.html`).
* `Dockerfile` & `manifest.yml`: Containerization and IBM Cloud deployment profiles.

---

### 8. Project Demonstration

#### Local Execution Instruction
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the web application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`.

#### Testing Presets in UI
On the **Predict Eligibility** page, utilize the quick buttons to populate the form instantly:
- **Scenario 1**: Automatically inputs high-income, salaried parameters with active credit history $\rightarrow$ **LOAN ELIGIBLE**.
- **Scenario 2**: Inputs self-employed, lower income parameters with high loan demands and bad credit history $\rightarrow$ **LOAN DECLINED**.
