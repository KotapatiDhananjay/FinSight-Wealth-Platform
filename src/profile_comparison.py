import pandas as pd
import plotly.express as px

from optimizer import (
    optimize_portfolio,
    calculate_metrics
)


# Profiles required by the project
profiles = [
    "conservative",
    "moderate",
    "aggressive",
    "very_aggressive"
]


results = []


# ---------------------------------------------------------
# Calculate portfolio metrics for every profile
# ---------------------------------------------------------

for profile in profiles:

    weights = optimize_portfolio(profile)

    metrics = calculate_metrics(weights)

    results.append({

        "Risk Profile": profile.replace(
            "_",
            " "
        ).title(),

        "Expected Return": (
            metrics["expected_return"] * 100
        ),

        "Volatility": (
            metrics["volatility"] * 100
        ),

        "Sharpe Ratio": (
            metrics["sharpe_ratio"]
        )
    })


# ---------------------------------------------------------
# Create dataframe
# ---------------------------------------------------------

comparison = pd.DataFrame(results)


print("\n")
print("=" * 65)
print("RISK PROFILE COMPARISON")
print("=" * 65)

print(
    comparison.to_string(
        index=False
    )
)


# ---------------------------------------------------------
# Expected Return vs Risk Chart
# ---------------------------------------------------------

fig = px.scatter(

    comparison,

    x="Volatility",

    y="Expected Return",

    size="Sharpe Ratio",

    text="Risk Profile",

    title="Expected Return vs Portfolio Risk",

    labels={
        "Volatility":
            "Portfolio Risk / Volatility (%)",

        "Expected Return":
            "Expected Annual Return (%)"
    }
)


fig.update_traces(
    textposition="top center"
)


fig.show()