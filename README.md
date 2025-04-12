🌍 Problem: Understanding Economic Trends Across Countries

Macroeconomic indicators like GDP, CPI (inflation), unemployment, and interest rates are vital for understanding a country’s economic health. However, this data is often scattered across different sources, varies in format, and is not easy to analyze or compare across countries.

In particular, policymakers, investors, and researchers often need to:
	•	Analyze how key indicators evolve over time
	•	Compare economic trends across countries
	•	Identify correlations between indicators (e.g., inflation vs interest rate, or unemployment vs GDP)
	•	Gain insights that could signal economic risk or growth opportunities

💡 Solution: A Reproducible Data Platform for Global Macroeconomic Insights

This project builds an end-to-end data pipeline that ingests publicly available macroeconomic data from the World Bank API, transforms and aggregates it using dbt, stores it in BigQuery, and visualizes it through a dynamic, filterable Looker Studio dashboard.

Key features:
	•	Scheduled data ingestion using Airflow, fetching multiple macro indicators for many countries
	•	Cleaned and modeled data with dbt, including calculations for YoY changes and derived metrics
	•	Partitioned and clustered BigQuery tables to ensure efficient querying
	•	A dashboard with country and year filters, showing:
	•	GDP growth over time
	•	CPI trends compared to GDP
	•	Correlation between inflation and unemployment
	•	(Optional) Stock market trends from yfinance

🛠️ Tech Stack
	•	Airflow (Docker) for orchestration
	•	Python for API ingestion scripts
	•	Terraform for provisioning GCP resources
	•	BigQuery as the data warehouse
	•	dbt for data transformations and metrics
	•	Looker Studio for visualization

This platform enables automated, reproducible macroeconomic analysis, helping users explore country-level trends with data that updates automatically and scales globally.
