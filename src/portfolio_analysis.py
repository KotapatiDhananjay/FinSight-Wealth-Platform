import pandas as pd
import numpy as np

from data_loader import load_portfolio_data


# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

df = load_portfolio_data()

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date
df = df.sort_values("date")


# --------------------------------------------------
# 2. SELECT ASSETS
# --------------------------------------------------

assets = [
    "RELIANCE",
    "TCS",
    "HDFCBANK",
    "INFY",
    "ICICIBANK",
    "WIPRO",
    "BAJFINANCE",
    "HCLTECH"
]

market = "market_nifty50"


# --------------------------------------------------
# 3. CALCULATE DAILY RETURNS
# --------------------------------------------------

returns = df[assets].pct_change()

print("\n" + "=" * 60)
print("DAILY RETURNS")
print("=" * 60)

print(returns.head())


# --------------------------------------------------
# 4. REMOVE FIRST EMPTY ROW
# --------------------------------------------------

returns = returns.dropna()


# --------------------------------------------------
# 5. CALCULATE ANNUALIZED EXPECTED RETURN
# --------------------------------------------------

expected_returns = returns.mean() * 252


print("\n" + "=" * 60)
print("EXPECTED ANNUAL RETURN")
print("=" * 60)

for asset in assets:
    print(
        f"{asset:<15} "
        f"{expected_returns[asset] * 100:.2f}%"
    )


# --------------------------------------------------
# 6. CALCULATE ANNUALIZED VOLATILITY
# --------------------------------------------------

volatility = returns.std() * np.sqrt(252)


print("\n" + "=" * 60)
print("ANNUALIZED VOLATILITY")
print("=" * 60)

for asset in assets:
    print(
        f"{asset:<15} "
        f"{volatility[asset] * 100:.2f}%"
    )


# --------------------------------------------------
# 7. CALCULATE COVARIANCE MATRIX
# --------------------------------------------------

covariance_matrix = returns.cov() * 252


print("\n" + "=" * 60)
print("COVARIANCE MATRIX")
print("=" * 60)

print(covariance_matrix.round(4))


# --------------------------------------------------
# 8. CALCULATE CORRELATION MATRIX
# --------------------------------------------------

correlation_matrix = returns.corr()


print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

print(correlation_matrix.round(2))


# --------------------------------------------------
# 9. CREATE SUMMARY TABLE
# --------------------------------------------------

summary = pd.DataFrame({
    "Expected Return": expected_returns,
    "Volatility": volatility
})


print("\n" + "=" * 60)
print("ASSET PERFORMANCE SUMMARY")
print("=" * 60)

print(summary)


# --------------------------------------------------
# 10. SAVE RESULTS
# --------------------------------------------------

summary.to_csv(
    "data/asset_performance_summary.csv"
)

covariance_matrix.to_csv(
    "data/covariance_matrix.csv"
)

correlation_matrix.to_csv(
    "data/correlation_matrix.csv"
)


print("\nAnalysis files saved successfully!")