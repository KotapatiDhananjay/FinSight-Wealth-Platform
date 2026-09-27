# FinSight Wealth Platform

## Portfolio Optimization Engine

FinSight Wealth Platform is a FinTech portfolio optimization project designed for wealth management and robo-advisory use cases.

The system accepts an investor's risk profile and investment capital, analyzes historical market data, and generates an optimized portfolio allocation using Modern Portfolio Theory concepts and quantitative optimization.

---

## Project Objectives

The project aims to:

- Analyze historical stock price data
- Calculate expected annual returns
- Calculate portfolio volatility
- Calculate covariance between assets
- Optimize portfolio asset allocation
- Calculate Sharpe ratio
- Calculate maximum drawdown
- Support multiple investor risk profiles
- Provide an interactive Streamlit dashboard
- Provide a FastAPI backend
- Provide automated tests
- Document the complete workflow in a Jupyter notebook

---

## Risk Profiles

The project supports four risk profiles from the provided FinSight dataset:

| Risk Profile | Investment Horizon | Expected Return | Maximum Equity | Maximum Drawdown |
|---|---:|---:|---:|---:|
| Conservative | 3 years | 7.5% | 40% | 2.5% |
| Moderate | 7 years | 9.0% | 70% | 10.0% |
| Aggressive | 15 years | 10.2% | 95% | 16.2% |
| Very Aggressive | 20 years | 11.0% | 110% | 20.0% |

---

## Dataset

### Portfolio Dataset

File:

```text
data/finsight_portfolio_data.csv