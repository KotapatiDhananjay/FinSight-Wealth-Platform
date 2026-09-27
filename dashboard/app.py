import sys
import os

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from src.optimizer import (
    assets,
    optimize_portfolio,
    calculate_metrics,
    calculate_max_drawdown,
    get_profile
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinSight Wealth Platform",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        color: #666;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        border: 1px solid #e5e7eb;
    }

    .disclaimer {
        font-size: 13px;
        color: #666;
        padding: 15px;
        border-radius: 8px;
        background-color: #f8f8f8;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">💰 FinSight Wealth Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'MPT-based AI/ML Portfolio Optimization Platform'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Investment Configuration")

st.sidebar.markdown(
    "Enter your investment details below."
)


capital = st.sidebar.number_input(
    "Investment Capital (₹)",
    min_value=1000.0,
    max_value=100000000.0,
    value=100000.0,
    step=10000.0
)


risk_profile = st.sidebar.selectbox(
    "Risk Profile",
    [
        "conservative",
        "moderate",
        "aggressive",
        "very_aggressive"
    ],
    format_func=lambda x: x.replace(
        "_",
        " "
    ).title()
)


optimize_button = st.sidebar.button(
    "🚀 Optimize Portfolio",
    type="primary",
    use_container_width=True
)


st.sidebar.divider()

st.sidebar.info(
    "The optimizer uses historical market data "
    "and Modern Portfolio Theory to calculate "
    "an estimated asset allocation."
)


# ============================================================
# PROFILE INFORMATION
# ============================================================

profile = get_profile(
    risk_profile
)


st.markdown(
    '<div class="section-title">Risk Profile</div>',
    unsafe_allow_html=True
)


profile_col1, profile_col2, profile_col3, profile_col4 = (
    st.columns(4)
)


with profile_col1:

    st.metric(
        "Risk Profile",
        risk_profile.replace(
            "_",
            " "
        ).title()
    )


with profile_col2:

    st.metric(
        "Investment Horizon",
        f"{profile['investment_horizon_yrs']} Years"
    )


with profile_col3:

    st.metric(
        "Target Return",
        f"{profile['expected_return_pct']}%"
    )


with profile_col4:

    st.metric(
        "Maximum Drawdown",
        f"{profile['max_drawdown_pct']}%"
    )


st.divider()


# ============================================================
# DEFAULT MESSAGE
# ============================================================

if not optimize_button:

    st.info(
        "👈 Enter your investment capital, "
        "select a risk profile and click "
        "'Optimize Portfolio' to generate "
        "your portfolio."
    )


# ============================================================
# OPTIMIZE PORTFOLIO
# ============================================================

if optimize_button:

    # --------------------------------------------------------
    # Calculate optimized weights
    # --------------------------------------------------------

    weights = optimize_portfolio(
        risk_profile
    )


    # --------------------------------------------------------
    # Calculate portfolio metrics
    # --------------------------------------------------------

    metrics = calculate_metrics(
        weights
    )


    # --------------------------------------------------------
    # Calculate actual historical drawdown
    # --------------------------------------------------------

    actual_drawdown = calculate_max_drawdown(
        weights
    )


    # ========================================================
    # CREATE PORTFOLIO DATAFRAME
    # ========================================================

    portfolio = pd.DataFrame(
        {
            "Asset": assets,
            "Weight": weights
        }
    )


    portfolio["Allocation (%)"] = (
        portfolio["Weight"] * 100
    )


    portfolio["Investment (₹)"] = (
        portfolio["Weight"] * capital
    )


    # Remove extremely small allocations
    portfolio = portfolio[
        portfolio["Allocation (%)"] > 0.01
    ]


    # Sort largest allocation first
    portfolio = portfolio.sort_values(
        "Allocation (%)",
        ascending=False
    )


    # ========================================================
    # PORTFOLIO METRICS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Optimized Portfolio'
        '</div>',
        unsafe_allow_html=True
    )


    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )


    with metric1:

        st.metric(
            "Investment",
            f"₹{capital:,.0f}"
        )


    with metric2:

        st.metric(
            "Expected Return",
            f"{metrics['expected_return'] * 100:.2f}%"
        )


    with metric3:

        st.metric(
            "Portfolio Risk",
            f"{metrics['volatility'] * 100:.2f}%"
        )


    with metric4:

        st.metric(
            "Sharpe Ratio",
            f"{metrics['sharpe_ratio']:.2f}"
        )


    st.divider()


    # ========================================================
    # ALLOCATION CHARTS
    # ========================================================

    chart_col1, chart_col2 = st.columns(2)


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with chart_col1:

        st.subheader(
            "📊 Asset Allocation"
        )


        pie_chart = px.pie(
            portfolio,
            names="Asset",
            values="Allocation (%)",
            hole=0.45,
            title="Portfolio Allocation"
        )


        pie_chart.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )


        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with chart_col2:

        st.subheader(
            "💰 Capital Allocation"
        )


        bar_chart = px.bar(
            portfolio,
            x="Asset",
            y="Investment (₹)",
            title="Investment Amount by Asset",
            text="Investment (₹)"
        )


        bar_chart.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )


        bar_chart.update_layout(
            yaxis_title="Investment (₹)",
            xaxis_title="Asset"
        )


        st.plotly_chart(
            bar_chart,
            use_container_width=True
        )


    # ========================================================
    # RECOMMENDED ALLOCATION TABLE
    # ========================================================

    st.subheader(
        "📋 Recommended Allocation"
    )


    display_df = portfolio[
        [
            "Asset",
            "Allocation (%)",
            "Investment (₹)"
        ]
    ].copy()


    display_df["Allocation (%)"] = (
        display_df["Allocation (%)"]
        .round(2)
    )


    display_df["Investment (₹)"] = (
        display_df["Investment (₹)"]
        .round(2)
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # RETURN ESTIMATE
    # ========================================================

    st.subheader(
        "📈 Return Estimate"
    )


    expected_profit = (
        capital
        * metrics["expected_return"]
    )


    estimated_value = (
        capital
        + expected_profit
    )


    return_col1, return_col2, return_col3 = (
        st.columns(3)
    )


    with return_col1:

        st.metric(
            "Estimated Annual Return",
            f"₹{expected_profit:,.2f}"
        )


    with return_col2:

        st.metric(
            "Estimated Portfolio Value",
            f"₹{estimated_value:,.2f}"
        )


    with return_col3:

        st.metric(
            "Historical Max Drawdown",
            f"{actual_drawdown * 100:.2f}%"
        )


    st.divider()


# ============================================================
# RISK PROFILE COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Expected Return vs Risk'
    '</div>',
    unsafe_allow_html=True
)


comparison_profiles = [
    "conservative",
    "moderate",
    "aggressive",
    "very_aggressive"
]


comparison_results = []


for profile_name in comparison_profiles:

    profile_weights = optimize_portfolio(
        profile_name
    )


    profile_metrics = calculate_metrics(
        profile_weights
    )


    comparison_results.append(
        {
            "Risk Profile":
                profile_name.replace(
                    "_",
                    " "
                ).title(),

            "Expected Return":
                profile_metrics[
                    "expected_return"
                ] * 100,

            "Risk":
                profile_metrics[
                    "volatility"
                ] * 100,

            "Sharpe Ratio":
                profile_metrics[
                    "sharpe_ratio"
                ]
        }
    )


comparison_df = pd.DataFrame(
    comparison_results
)


# ============================================================
# SCATTER CHART
# ============================================================

risk_chart = px.scatter(

    comparison_df,

    x="Risk",

    y="Expected Return",

    size="Sharpe Ratio",

    text="Risk Profile",

    title="Expected Annual Return vs Portfolio Risk",

    labels={
        "Risk":
            "Portfolio Risk / Volatility (%)",

        "Expected Return":
            "Expected Annual Return (%)",

        "Sharpe Ratio":
            "Sharpe Ratio"
    }
)


risk_chart.update_traces(
    textposition="top center"
)


risk_chart.update_layout(
    height=500
)


st.plotly_chart(
    risk_chart,
    use_container_width=True
)


# ============================================================
# PROFILE COMPARISON TABLE
# ============================================================

st.subheader(
    "Risk Profile Comparison"
)


comparison_display = comparison_df.copy()


comparison_display[
    "Expected Return"
] = comparison_display[
    "Expected Return"
].round(2)


comparison_display[
    "Risk"
] = comparison_display[
    "Risk"
].round(2)


comparison_display[
    "Sharpe Ratio"
] = comparison_display[
    "Sharpe Ratio"
].round(2)


st.dataframe(
    comparison_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()


st.markdown(
    """
    <div class="disclaimer">

    <b>Important:</b> This application is an educational
    and research demonstration. Portfolio returns are
    estimated using historical market data and Modern
    Portfolio Theory. Historical performance does not
    guarantee future returns. The application does not
    constitute personalized financial or investment advice.

    </div>
    """,
    unsafe_allow_html=True
)