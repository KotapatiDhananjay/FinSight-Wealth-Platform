from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.optimizer import (
    assets,
    optimize_portfolio,
    calculate_metrics,
    calculate_max_drawdown,
    get_profile
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="FinSight Portfolio Optimization API",
    description="Portfolio optimization API for the FinSight Wealth Platform",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class PortfolioRequest(BaseModel):
    risk_profile: str
    capital: float


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "FinSight Portfolio Optimization API",
        "status": "running"
    }


# ============================================================
# AVAILABLE RISK PROFILES
# ============================================================

@app.get("/profiles")
def get_profiles():

    return {
        "profiles": [
            "conservative",
            "moderate",
            "aggressive",
            "very_aggressive"
        ]
    }


# ============================================================
# PROFILE INFORMATION
# ============================================================

@app.get("/profiles/{profile_name}")
def profile_information(profile_name: str):

    try:

        profile = get_profile(profile_name)

        return {
            "profile_id": int(profile["profile_id"]),
            "risk_appetite": str(profile["risk_appetite"]),
            "investment_horizon_yrs": int(
                profile["investment_horizon_yrs"]
            ),
            "max_equity_pct": float(
                profile["max_equity_pct"]
            ),
            "expected_return_pct": float(
                profile["expected_return_pct"]
            ),
            "max_drawdown_pct": float(
                profile["max_drawdown_pct"]
            )
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# PORTFOLIO OPTIMIZATION
# ============================================================

@app.post("/optimize")
def optimize(request: PortfolioRequest):

    # --------------------------------------------------------
    # Validate Capital
    # --------------------------------------------------------

    if request.capital <= 0:

        raise HTTPException(
            status_code=400,
            detail="Capital must be greater than zero."
        )

    # --------------------------------------------------------
    # Validate Risk Profile
    # --------------------------------------------------------

    try:

        profile = get_profile(
            request.risk_profile
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    # --------------------------------------------------------
    # Optimize Portfolio
    # --------------------------------------------------------

    try:

        weights = optimize_portfolio(
            request.risk_profile
        )

        metrics = calculate_metrics(
            weights
        )

        max_drawdown = calculate_max_drawdown(
            weights
        )

        # ----------------------------------------------------
        # Asset Allocation
        # ----------------------------------------------------

        allocation = {}

        for asset, weight in zip(
            assets,
            weights
        ):

            allocation[asset] = {
                "percentage": round(
                    float(weight * 100),
                    2
                ),
                "amount": round(
                    float(weight * request.capital),
                    2
                )
            }

        # ----------------------------------------------------
        # API Response
        # ----------------------------------------------------

        return {

            "risk_profile": str(
                profile["risk_appetite"]
            ),

            "capital": float(
                request.capital
            ),

            "investment_horizon_years": int(
                profile["investment_horizon_yrs"]
            ),

            "target_return_percent": float(
                profile["expected_return_pct"]
            ),

            "maximum_equity_percent": float(
                profile["max_equity_pct"]
            ),

            "maximum_drawdown_target_percent": float(
                profile["max_drawdown_pct"]
            ),

            "allocation": allocation,

            "portfolio_metrics": {

                "expected_return_percent": round(
                    float(
                        metrics["expected_return"] * 100
                    ),
                    2
                ),

                "volatility_percent": round(
                    float(
                        metrics["volatility"] * 100
                    ),
                    2
                ),

                "sharpe_ratio": round(
                    float(
                        metrics["sharpe_ratio"]
                    ),
                    2
                ),

                "maximum_drawdown_percent": round(
                    float(
                        max_drawdown * 100
                    ),
                    2
                )
            }
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Portfolio optimization failed: {str(error)}"
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "FinSight Portfolio Optimization API"
    }