from pathlib import Path

from src.analytics.data_quality import assess_data_quality
from src.analytics.portfolio_metrics import (
    assess_concentration,
    calculate_holding_metrics,
    calculate_portfolio_allocation,
)
from src.data.amfi_client import fetch_latest_nav
from src.data.fund_matcher import find_fund_matches
from src.models.input_loader import load_portfolio


def analyze_portfolio(
    portfolio_path: str | Path,
) -> dict:
    """Run deterministic analysis on an investor portfolio."""

    portfolio = load_portfolio(portfolio_path)
    nav_data = fetch_latest_nav()

    analyzed_holdings = []

    for holding in portfolio["holdings"]:
        matches = find_fund_matches(
            holding["fund_name"],
            nav_data,
        )

        if not matches:
            analyzed_holdings.append(
                {
                    **holding,
                    "status": "no_match",
                    "matches": [],
                }
            )
            continue

        if len(matches) > 1:
            analyzed_holdings.append(
                {
                    **holding,
                    "status": "multiple_matches",
                    "matches": matches,
                }
            )
            continue

        match = matches[0]

        current_nav = float(match["net_asset_value"])

        metrics = calculate_holding_metrics(
            units=float(holding["units"]),
            purchase_price=float(holding["purchase_price"]),
            current_nav=current_nav,
        )

        analyzed_holdings.append(
            {
                **holding,
                **metrics,
                "scheme_code": match["scheme_code"],
                "scheme_name": match["scheme_name"],
                "current_nav": current_nav,
                "nav_date": match["date"],
                "status": "matched",
            }
        )

    matched_holdings = [
        holding
        for holding in analyzed_holdings
        if holding["status"] == "matched"
    ]

    if not matched_holdings:
        return {
            "investor": portfolio["investor"],
            "holdings": analyzed_holdings,
            "data_quality_warnings": [],
            "status": "no_holdings_matched",
        }

    allocation_result = calculate_portfolio_allocation(
        matched_holdings
    )

    concentration_result = assess_concentration(
        allocation_result["holdings"]
    )

    data_quality_warnings = assess_data_quality(
        concentration_result["holdings"]
    )

    return {
        "investor": portfolio["investor"],
        "total_portfolio_value": allocation_result[
            "total_portfolio_value"
        ],
        "holdings": analyzed_holdings,
        "analyzed_holdings": concentration_result["holdings"],
        "data_quality_warnings": data_quality_warnings,
        "status": "success",
    }