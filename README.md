Personal Finance Anomaly Detector & Budget Variance Engine 🚀

An end-to-end data analytics pipeline designed to detect unusual spending patterns, financial outliers, and budget breaches in transactional datasets. This system leverages dual-layer statistical validation (**Z-Score** & **Interquartile Range - IQR**), maintains a relational storage schema using **SQL**, and provides dynamic, interactive dashboards for auditing.

🎯 Project Overview :
In real-world financial systems, identifying fraudulent activities, system glitches, or sudden overspending manually is highly inefficient. This project automates the entire analytical workflow:
1. Data Ingestion & Simulation: Simulates realistic transactional data while embedding complex statistical anomalies.
2. Mathematical Analysis: Employs a hybrid model (Z-Score + IQR) to identify mathematical anomalies grouped by domain-specific categories.
3. Database Standardization: Synchronizes raw and processed logs into structured RDBMS schemas using optimized SQL queries.
4. Interactive BI Layer: Triggers responsive data visualizations mapping actual expenses against operational budgets.

💻 Tech Stack & Tools Used
- Language: Python 3.x
- Data Manipulation: Pandas, NumPy
- Relational Database: SQLite3 / SQL Syntax
- Data Visualization: Plotly Express
- File Management: OpenPyXL (Excel Logging)
- Environment: VS Code, Git, GitHub

📊 Core Architecture & Logic

1. Statistical Anomaly Detection Core
To ensure absolute accuracy, the system avoids static hardcoded thresholds and uses dynamic mathematics:
- Z-Score Filter: Measures how many standard deviations a transaction lies away from the category mean. Flags items where $|Z| > 3$.
  $$\text{Z} = \frac{X - \mu}{\sigma}$$
- IQR (Interquartile Range) Fences: Divides data into percentiles ($Q1$, $Q2$, $Q3$). It sets strict mathematical boundaries:
  $$\text{Upper Fence} = Q3 + (1.5 \times \text{IQR})$$
  Any transaction exceeding this fence is instantly isolated. Highly resilient to heavy skewness.

2. SQL RDBMS Architecture
Processed outputs are structured and migrated into three core relational tables inside `finance.db`:-
 `all_transactions`: Complete raw transaction ledger.
- `detected_anomalies`: Isolated outlier points flagged by the algorithms for audit reviews.
- `monthly_budget_report`: Roll-up aggregations mapping total monthly spending against predefined targets to evaluate financial health.

 📁 Repository Structure
```bash
├── generate_data.py       
├── anomaly_detector.py    
├── sql_db_sync.py         
├── requirements.txt       
└── README.md              
