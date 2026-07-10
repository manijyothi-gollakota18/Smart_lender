import urllib.request
import urllib.parse
import sys

def verify_app():
    base_url = "http://127.0.0.1:5000"
    print("--- Starting Programmatic Verification of Smart Lender App ---")

    # 1. Verify Home Page
    try:
        response = urllib.request.urlopen(base_url)
        html = response.read().decode('utf-8')
        assert response.status == 200
        assert "SMART LENDER" in html
        print("[PASS] Home Page verified successfully (HTTP 200)")
    except Exception as e:
        print(f"[FAIL] Home Page verification failed: {e}")
        sys.exit(1)

    # 2. Verify Insights Page
    try:
        response = urllib.request.urlopen(f"{base_url}/insights")
        html = response.read().decode('utf-8')
        assert response.status == 200
        assert "Model Performance Leaderboard" in html
        assert "count_plot.png" in html
        assert "dist_plot.png" in html
        assert "bar_chart.png" in html
        print("[PASS] Insights Page verified successfully (HTTP 200)")
    except Exception as e:
        print(f"[FAIL] Insights Page verification failed: {e}")
        sys.exit(1)

    # 3. Verify Scenario 1: Low-Risk Applicant (Approved)
    try:
        scenario_1_data = urllib.parse.urlencode({
            'gender': 'Male',
            'married': 'Yes',
            'dependents': '2',
            'education': 'Graduate',
            'self_employed': 'No',
            'property_area': 'Semiurban',
            'applicant_income': '7500',
            'coapplicant_income': '2500',
            'loan_amount': '150',
            'loan_term': '360',
            'credit_history': '1.0'
        }).encode('utf-8')
        
        req = urllib.request.Request(f"{base_url}/predict", data=scenario_1_data)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        
        assert response.status == 200
        assert "LOAN ELIGIBLE" in html
        assert "LOAN DECLINED" not in html
        print("[PASS] Scenario 1 (Low-Risk Fast-Track) verified: Predicts LOAN ELIGIBLE")
    except Exception as e:
        print(f"[FAIL] Scenario 1 verification failed: {e}")
        sys.exit(1)

    # 4. Verify Scenario 2: High-Risk Applicant (Declined)
    try:
        scenario_2_data = urllib.parse.urlencode({
            'gender': 'Female',
            'married': 'No',
            'dependents': '0',
            'education': 'Not Graduate',
            'self_employed': 'Yes',
            'property_area': 'Rural',
            'applicant_income': '2200',
            'coapplicant_income': '0',
            'loan_amount': '300',
            'loan_term': '180',
            'credit_history': '0.0'
        }).encode('utf-8')
        
        req = urllib.request.Request(f"{base_url}/predict", data=scenario_2_data)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        
        assert response.status == 200
        assert "LOAN DECLINED" in html
        assert "LOAN ELIGIBLE" not in html
        print("[PASS] Scenario 2 (High-Risk Detection) verified: Predicts LOAN DECLINED")
    except Exception as e:
        print(f"[FAIL] Scenario 2 verification failed: {e}")
        sys.exit(1)

    print("\n[SUCCESS] All verification tests passed successfully!")

if __name__ == "__main__":
    verify_app()
