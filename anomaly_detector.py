import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as io

# 1. Load data
df = pd.read_csv('transactions.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.strftime('%Y-%m')

print(f"Total Transactions Loaded: {len(df)}")

# --- METHOD 1: Z-SCORE (Applied Globally or per Category) ---
# Formula: Z = (X - Mean) / StdDev. Agar Z > 3, toh wo anomaly hai.
df['Z_Score'] = df.groupby('Category')['Amount'].transform(lambda x: (x - x.mean()) / x.std())
df['Is_Anomaly_Z'] = df['Z_Score'].abs() > 3

# --- METHOD 2: IQR (Interquartile Range) ---
# Q1 (25th percentile), Q3 (75th percentile). IQR = Q3 - Q1.
# Upper Bound = Q3 + 1.5 * IQR. Agar Amount > Upper Bound, toh anomaly hai.
def detect_iqr_outliers(group):
    q1 = group['Amount'].quantile(0.25)
    q3 = group['Amount'].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + (1.5 * iqr)
    return group['Amount'] > upper_bound

df['Is_Anomaly_IQR'] = df.groupby('Category', group_keys=False).apply(detect_iqr_outliers)

# Combine results (Flagged by either Z-score OR IQR)
df['Final_Anomaly'] = df['Is_Anomaly_Z'] | df['Is_Anomaly_IQR']

total_anomalies = df['Final_Anomaly'].sum()
print(f"Total Anomalies Flagged: {total_anomalies}")

# --- BUDGET VS ACTUAL REPORTING SYSTEM ---
# Let's define a monthly budget for each category
monthly_budgets = {
    'Food': 15000,
    'Travel': 20000,
    'Shopping': 25000,
    'Bills': 15000
}

# Group actual expenses by Month and Category
budget_df = df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
budget_df['Budget'] = budget_df['Category'].map(monthly_budgets)
budget_df['Variance'] = budget_df['Amount'] - budget_df['Budget']
budget_df['Budget_Exceeded'] = budget_df['Variance'] > 0

# Save data reports to CSV
df[df['Final_Anomaly'] == True].to_csv('flagged_anomalies.csv', index=False)
budget_df.to_csv('budget_report.csv', index=False)

# --- VISUALIZATION 1: Scatter Plot for Anomalies ---
fig_scatter = px.scatter(
    df, 
    x='Date', 
    y='Amount', 
    color='Final_Anomaly',
    color_discrete_map={True: 'red', False: 'blue'},
    hover_data=['Transaction_ID', 'Category', 'Amount'],
    title='Personal Finance Anomaly Detection (Visual Alerts)'
)
fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
fig_scatter.show()

# --- VISUALIZATION 2: Budget vs Actuals ---
fig_budget = px.bar(
    budget_df, 
    x='Month', 
    y='Amount', 
    color='Category', 
    barmode='group',
    text=budget_df['Variance'].apply(lambda x: f"Var: {round(x)}" if x > 0 else ""),
    title='Monthly Budget vs Actual Spending Patterns'
)
# Add target budget lines or reference markers if needed
fig_budget.show()