document.addEventListener('DOMContentLoaded', () => {
    // Prediction Form Loader overlay
    const predictionForm = document.getElementById('prediction-form');
    const loaderWrapper = document.getElementById('loader-wrapper');

    if (predictionForm && loaderWrapper) {
        predictionForm.addEventListener('submit', (e) => {
            // Show loader
            loaderWrapper.style.display = 'flex';
        });
    }

    // Dynamic color updates or validation triggers (if any)
    const applicantIncomeInput = document.getElementById('applicant_income');
    const coapplicantIncomeInput = document.getElementById('coapplicant_income');
    const totalIncomeDisplay = document.getElementById('total-income-display');

    if (applicantIncomeInput && coapplicantIncomeInput && totalIncomeDisplay) {
        const calculateTotalIncome = () => {
            const appIncome = parseFloat(applicantIncomeInput.value) || 0;
            const coappIncome = parseFloat(coapplicantIncomeInput.value) || 0;
            totalIncomeDisplay.textContent = `Total Monthly Income: $${(appIncome + coappIncome).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        };

        applicantIncomeInput.addEventListener('input', calculateTotalIncome);
        coapplicantIncomeInput.addEventListener('input', calculateTotalIncome);
    }
});
