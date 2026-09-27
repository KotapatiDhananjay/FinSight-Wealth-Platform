import sys
from pathlib import Path

import numpy as np


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT OPTIMIZER
# ============================================================

from src.optimizer import (
    assets,
    optimize_portfolio,
    calculate_metrics,
    calculate_max_drawdown,
    get_profile
)


# ============================================================
# TEST RISK PROFILES
# ============================================================

def test_risk_profiles_exist():

    profiles = [
        "conservative",
        "moderate",
        "aggressive",
        "very_aggressive"
    ]

    for profile in profiles:

        result = get_profile(profile)

        assert result is not None

        assert (
            str(result["risk_appetite"]).lower()
            == profile
        )


# ============================================================
# TEST PROFILE VALUES
# ============================================================

def test_aggressive_profile():

    profile = get_profile("aggressive")

    assert float(
        profile["expected_return_pct"]
    ) == 10.2

    assert int(
        profile["investment_horizon_yrs"]
    ) == 15


# ============================================================
# TEST OPTIMIZATION
# ============================================================

def test_optimize_portfolio():

    weights = optimize_portfolio(
        "aggressive"
    )

    assert len(weights) == len(assets)

    assert np.all(
        weights >= 0
    )

    assert np.isclose(
        weights.sum(),
        1.0
    )


# ============================================================
# TEST INDIVIDUAL ASSET LIMIT
# ============================================================

def test_asset_weight_limit():

    weights = optimize_portfolio(
        "aggressive"
    )

    assert np.all(
        weights <= 0.40 + 1e-6
    )


# ============================================================
# TEST PORTFOLIO METRICS
# ============================================================

def test_portfolio_metrics():

    weights = optimize_portfolio(
        "aggressive"
    )

    metrics = calculate_metrics(
        weights
    )

    assert "expected_return" in metrics

    assert "volatility" in metrics

    assert "sharpe_ratio" in metrics

    assert np.isfinite(
        metrics["expected_return"]
    )

    assert np.isfinite(
        metrics["volatility"]
    )

    assert np.isfinite(
        metrics["sharpe_ratio"]
    )


# ============================================================
# TEST MAXIMUM DRAWDOWN
# ============================================================

def test_maximum_drawdown():

    weights = optimize_portfolio(
        "aggressive"
    )

    max_drawdown = calculate_max_drawdown(
        weights
    )

    assert max_drawdown >= 0

    assert max_drawdown <= 1


# ============================================================
# TEST ALL PROFILES
# ============================================================

def test_all_profiles():

    profiles = [
        "conservative",
        "moderate",
        "aggressive",
        "very_aggressive"
    ]

    for profile in profiles:

        weights = optimize_portfolio(
            profile
        )

        assert len(weights) == len(assets)

        assert np.isclose(
            weights.sum(),
            1.0
        )

        metrics = calculate_metrics(
            weights
        )

        assert metrics[
            "volatility"
        ] >= 0