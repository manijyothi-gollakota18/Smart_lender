import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns

def generate_eda_plots():
    # Load dataset
    data_path = os.path.join("data", "train.csv")
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}. Please run download_data.py first.")
        return

    df = pd.read_csv(data_path)
    print("Dataset Loaded. Columns:", df.columns.tolist())

    # Create output directory
    output_dir = os.path.join("static", "plots")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Set aesthetic style
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 12,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16
    })

    # 1. Count Plot: Credit History vs Loan Status
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=df, x='Credit_History', hue='Loan_Status', palette='Set2')
    plt.title('Loan Approval Status by Credit History', pad=15)
    plt.xlabel('Credit History (1.0 = Good, 0.0 = Bad)')
    plt.ylabel('Applicant Count')
    plt.legend(title='Loan Approved', labels=['No (N)', 'Yes (Y)'])
    plt.tight_layout()
    plot_path1 = os.path.join(output_dir, "count_plot.png")
    plt.savefig(plot_path1, dpi=150)
    plt.close()
    print(f"Saved: {plot_path1}")

    # 2. Distribution Plot: Applicant Income Distribution
    plt.figure(figsize=(8, 6))
    # Drop NaNs for income plotting
    sns.histplot(data=df.dropna(subset=['ApplicantIncome']), x='ApplicantIncome', kde=True, color='#6366f1', bins=40)
    plt.title('Distribution of Applicant Income', pad=15)
    plt.xlabel('Applicant Income ($)')
    plt.ylabel('Frequency')
    plt.xlim(0, 40000)  # Restrict x-axis slightly for better visibility (remove outliers visually)
    plt.tight_layout()
    plot_path2 = os.path.join(output_dir, "dist_plot.png")
    plt.savefig(plot_path2, dpi=150)
    plt.close()
    print(f"Saved: {plot_path2}")

    # 3. Bar Chart: Loan Amount vs Education Grouped by Loan Status
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df.dropna(subset=['LoanAmount', 'Education', 'Loan_Status']), 
                x='Education', y='LoanAmount', hue='Loan_Status', palette='Pastel1', errorbar=None)
    plt.title('Average Loan Amount by Education & Loan Status', pad=15)
    plt.xlabel('Education Level')
    plt.ylabel('Average Loan Amount (in thousands)')
    plt.legend(title='Loan Approved', labels=['No (N)', 'Yes (Y)'])
    plt.tight_layout()
    plot_path3 = os.path.join(output_dir, "bar_chart.png")
    plt.savefig(plot_path3, dpi=150)
    plt.close()
    print(f"Saved: {plot_path3}")

if __name__ == "__main__":
    generate_eda_plots()
