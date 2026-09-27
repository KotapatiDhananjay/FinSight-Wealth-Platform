import pandas as pd

from data_loader import load_portfolio_data, load_risk_profiles


# Load datasets
portfolio_df = load_portfolio_data()
risk_df = load_risk_profiles()


print("\n" + "=" * 60)
print("PORTFOLIO DATA ANALYSIS")
print("=" * 60)

# Basic information
print("\nDataset Shape:")
print(portfolio_df.shape)

print("\nColumn Information:")
print(portfolio_df.info())

print("\nMissing Values:")
print(portfolio_df.isnull().sum())

print("\nDuplicate Rows:")
print(portfolio_df.duplicated().sum())


print("\n" + "=" * 60)
print("RISK PROFILE ANALYSIS")
print("=" * 60)

print("\nRisk Profiles:")
print(risk_df)

print("\nRisk Profile Names:")
print(risk_df["risk_appetite"].tolist())


print("\n" + "=" * 60)
print("NUMERICAL SUMMARY")
print("=" * 60)

print(portfolio_df.describe())