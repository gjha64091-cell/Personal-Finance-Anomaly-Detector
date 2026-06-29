import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# 1. Setup Parameters
n_records = 520
categories = ['Food', 'Travel', 'Shopping', 'Bills']
start_date = datetime(2026, 1, 1)

# Normal distributions for each category (Mean, Std Dev)
cat_dist = {
    'Food': (500, 150),       # Normal daily/weekly food expense
    'Travel': (1200, 400),    # Normal travel/fuel cost
    'Shopping': (2000, 600),  # Clothes, electronics, etc.
    'Bills': (4000, 500)      # Rent, electricity, utilities
}

data = []

# 2. Generate Normal Transactions
for i in range(n_records):
    date = start_date + timedelta(days=random.randint(0, 90))
    category = random.choice(categories)
    mean, std = cat_dist[category]
    amount = round(np.random.normal(mean, std), 2)
    # Ensure amount is strictly positive
    amount = max(amount, 100.0)
    
    data.append([f"TXN_{1000+i}", date.strftime('%Y-%m-%d'), category, amount])

# 3. Inject 15+ Specific Anomalies (Jaise resume me mention kiya hai)
anomalous_entries = [
    # Food me bohot bada amount (e.g., high-end party)
    ("TXN_2001", "2026-01-15", "Food", 8500.00),
    ("TXN_2002", "2026-02-18", "Food", 9200.00),
    ("TXN_2003", "2026-03-05", "Food", 7800.00),
    # Travel me abnormal spike (e.g., flight tickets booking)
    ("TXN_2004", "2026-01-22", "Travel", 25000.00),
    ("TXN_2005", "2026-02-10", "Travel", 18500.00),
    ("TXN_2006", "2026-03-12", "Travel", 22000.00),
    # Shopping me huge luxury purchases
    ("TXN_2007", "2026-01-05", "Shopping", 65000.00),
    ("TXN_2008", "2026-01-28", "Shopping", 48000.00),
    ("TXN_2009", "2026-02-14", "Shopping", 55000.00),
    ("TXN_2010", "2026-03-25", "Shopping", 72000.00),
    # Bills double/triple charging
    ("TXN_2011", "2026-01-02", "Bills", 18000.00),
    ("TXN_2012", "2026-02-02", "Bills", 19500.00),
    ("TXN_2013", "2026-03-02", "Bills", 21000.00),
    # Mix random outliers
    ("TXN_2014", "2026-02-20", "Shopping", 35000.00),
    ("TXN_2015", "2026-03-18", "Food", 6000.00),
    ("TXN_2016", "2026-03-29", "Travel", 15000.00)
]

# Merge normal and anomalous data
df = pd.DataFrame(data, columns=['Transaction_ID', 'Date', 'Category', 'Amount'])
df_anom = pd.DataFrame(anomalous_entries, columns=['Transaction_ID', 'Date', 'Category', 'Amount'])
df_final = pd.concat([df, df_anom], ignore_index=True).sort_values(by='Date')

# Save to CSV
df_final.to_csv('transactions.csv', index=False)
print("Success: 500+ transactions with 16 anomalies saved to 'transactions.csv'!")