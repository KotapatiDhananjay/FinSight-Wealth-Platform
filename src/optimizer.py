import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .data_loader import load_portfolio_data, load_risk_profiles


# ============================================================
# LOAD DATA
# ============================================================

portfolio_df = load_portfolio_data()
risk_profiles = load_risk_profiles()


# ============================================================
# ASSETS
# ============================================================

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


# ============================================================
# PREPARE DATA
# ============================================================

portfolio_df["date"] = pd.to_datetime(portfolio_df["date"])

portfolio_df = portfolio_df.sort_values("date")

prices = portfolio_df[assets]

returns = prices.pct_change().dropna()


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

# Annual expected returns
expected_returns = returns.mean() * 252

# Annual covariance matrix
covariance_matrix = returns.cov() * 252


# ============================================================
# PORTFOLIO RETURN
# ============================================================

def portfolio_return(weights):
    return np.dot(weights, expected_returns)


# ============================================================
# PORTFOLIO VOLATILITY
# ============================================================

def portfolio_volatility(weights):
    return np.sqrt(
        weights.T @ covariance_matrix.values @ weights
    )


# ============================================================
# SHARPE RATIO
# ============================================================

def sharpe_ratio(weights, risk_free_rate=0.06):

    ret = portfolio_return(weights)

    risk = portfolio_volatility(weights)

    if risk <= 0:
        return 0

    return (ret - risk_free_rate) / risk


# ============================================================
# GET RISK PROFILE
# ============================================================

def get_profile(profile_name):

    profile_name = profile_name.lower()

    row = risk_profiles[
        risk_profiles["risk_appetite"].str.lower() == profile_name
    ]

    if row.empty:
        raise ValueError(
            f"Unknown risk profile: {profile_name}"
        )

    return row.iloc[0]


# ============================================================
# PORTFOLIO OPTIMIZATION
# ============================================================

def optimize_portfolio(profile_name):

    profile = get_profile(profile_name)

    target_return = (
        float(profile["expected_return_pct"]) / 100
    )

    max_drawdown = (
        float(profile["max_drawdown_pct"]) / 100
    )

    max_equity = min(
        float(profile["max_equity_pct"]) / 100,
        1.0
    )

    number_of_assets = len(assets)

    # Equal-weight starting point
    initial_weights = (
        np.ones(number_of_assets) / number_of_assets
    )

    # Each stock cannot exceed 40%
    bounds = [
        (0, 0.40)
        for _ in range(number_of_assets)
    ]

    # Portfolio weights must sum to 100%
    constraints = [
        {
            "type": "eq",
            "fun": lambda weights: np.sum(weights) - 1
        }
    ]

    # --------------------------------------------------------
    # Objective Function
    # --------------------------------------------------------

    def objective(weights):

        ret = portfolio_return(weights)

        risk = portfolio_volatility(weights)

        sharpe = sharpe_ratio(weights)

        return (
            -sharpe
            + 20 * max(0, target_return - ret) ** 2
            + 20 * max(0, risk - max_drawdown) ** 2
        )

    # --------------------------------------------------------
    # Optimization
    # --------------------------------------------------------

    result = minimize(
        objective,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={
            "maxiter": 2000,
            "ftol": 1e-9
        }
    )

    if not result.success:

        print(
            f"Optimization warning for {profile_name}:"
        )

        print(result.message)

    # --------------------------------------------------------
    # Clean Weights
    # --------------------------------------------------------

    weights = np.maximum(result.x, 0)

    if weights.sum() == 0:

        weights = initial_weights

    else:

        weights = weights / weights.sum()

    return weights


# ============================================================
# CALCULATE PORTFOLIO METRICS
# ============================================================

def calculate_metrics(weights):

    ret = portfolio_return(weights)

    risk = portfolio_volatility(weights)

    sharpe = sharpe_ratio(weights)

    return {
        "expected_return": ret,
        "volatility": risk,
        "sharpe_ratio": sharpe
    }


# ============================================================
# MAXIMUM DRAWDOWN
# ============================================================

def calculate_max_drawdown(weights):

    portfolio_daily_returns = returns.dot(weights)

    cumulative_returns = (
        1 + portfolio_daily_returns
    ).cumprod()

    running_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns / running_max
    ) - 1

    return abs(drawdown.min())


# ============================================================
# DISPLAY PORTFOLIO
# ============================================================

def display_portfolio(profile_name):

    weights = optimize_portfolio(profile_name)

    metrics = calculate_metrics(weights)

    max_drawdown = calculate_max_drawdown(weights)

    profile = get_profile(profile_name)

    print("\n")
    print("=" * 65)

    print(
        f"{profile_name.upper()} PORTFOLIO"
    )

    print("=" * 65)

    print("\nClient Profile:")

    print(
        "Investment Horizon :",
        profile["investment_horizon_yrs"],
        "years"
    )

    print(
        "Target Return      :",
        profile["expected_return_pct"],
        "%"
    )

    print(
        "Maximum Equity     :",
        profile["max_equity_pct"],
        "%"
    )

    print(
        "Maximum Drawdown   :",
        profile["max_drawdown_pct"],
        "%"
    )

    print("\nAsset Allocation:")

    for asset, weight in zip(
        assets,
        weights
    ):

        print(
            f"{asset:<15}"
            f"{weight * 100:>8.2f}%"
        )

    print("\nPortfolio Metrics:")

    print(
        "Expected Return :",
        f"{metrics['expected_return'] * 100:.2f}%"
    )

    print(
        "Volatility      :",
        f"{metrics['volatility'] * 100:.2f}%"
    )

    print(
        "Sharpe Ratio    :",
        f"{metrics['sharpe_ratio']:.2f}"
    )

    print(
        "Actual Max Drawdown :",
        f"{max_drawdown * 100:.2f}%"
    )


# ============================================================
# RUN ALL PROFILES
# ============================================================

if __name__ == "__main__":

    profiles = [
        "conservative",
        "moderate",
        "aggressive",
        "very_aggressive"
    ]

    for profile in profiles:

        display_portfolio(profile)