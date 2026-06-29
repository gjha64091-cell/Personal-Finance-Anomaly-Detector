import sqlite3
import pandas as pd

# 1. Connect to SQLite Database (Ek local finance.db file ban jayegi)
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# 2. CSV files ko clean dataframes mein load karo
df_all = pd.read_csv('transactions.csv')
df_anomalies = pd.read_csv('flagged_anomalies.csv')
df_budget = pd.read_csv('budget_report.csv')

# 3. In dataframes ko SQL Tables mein convert karo
df_all.to_sql('all_transactions', conn, if_exists='replace', index=False)
df_anomalies.to_sql('detected_anomalies', conn, if_exists='replace', index=False)
df_budget.to_sql('monthly_budget_report', conn, if_exists='replace', index=False)

print("⚡ Successfully created 3 relational tables in SQL Database (finance.db)!")

# 4. Verification Query: Ek custom SQL query run karke verify karte hain
print("\n--- Running SQL Query: Top 5 Highest Flagged Anomalies ---")
query = """
    SELECT Transaction_ID, Date, Category, Amount, round(Z_Score, 2) as Z_Score 
    FROM detected_anomalies 
    ORDER BY Amount DESC 
    LIMIT 5;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Close connection
conn.close()