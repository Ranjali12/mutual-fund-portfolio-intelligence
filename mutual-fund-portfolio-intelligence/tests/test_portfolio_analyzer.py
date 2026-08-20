import json

import pandas as pd

from src.analytics import portfolio_analyzer


def test_analyze_portfolio_success(tmp_path, monkeypatch):
    portfolio = {
        "investor": {
            "risk_profile": "moderate",
            "investment_horizon_years": 5,
            "primary_goal": "wealth_creation",
        },
        "holdings": [
            {
                "fund_name": "Test Flexi Cap Fund",
                "units": 100,
                "purchase_price": 200.0,
            }
        ],
    }

    portfolio_file = tmp_path / "portfolio.json"
    portfolio_file.write_text(
        json.dumps(portfolio),
        encoding="utf-8",
    )

    nav_data = pd.DataFrame(
        [
            {
                "scheme_code": "1001",
                "scheme_name": "Test Flexi Cap Fund",
                "net_asset_value": 250.0,
                "date": "18-Aug-2026",
            }
        ]
    )

    monkeypatch.setattr(
        portfolio_analyzer,
        "fetch_latest_nav",
        lambda: nav_data,
    )

    result = portfolio_analyzer.analyze_portfolio(
        portfolio_file
    )

    assert result["status"] == "success"
    assert result["total_portfolio_value"] == 25_000

    holding = result["analyzed_holdings"][0]

    assert holding["current_nav"] == 250.0
    assert holding["investment_cost"] == 20_000
    assert holding["current_value"] == 25_000
    assert holding["profit_loss"] == 5_000
    assert holding["return_percentage"] == 25.0
    assert holding["allocation_percentage"] == 100.0
    assert holding["concentration_level"] == "high"


def test_analyze_portfolio_no_match(tmp_path, monkeypatch):
    portfolio = {
        "investor": {
            "risk_profile": "moderate",
            "investment_horizon_years": 5,
            "primary_goal": "wealth_creation",
        },
        "holdings": [
            {
                "fund_name": "Unknown Fund",
                "units": 100,
                "purchase_price": 200.0,
            }
        ],
    }

    portfolio_file = tmp_path / "portfolio.json"
    portfolio_file.write_text(
        json.dumps(portfolio),
        encoding="utf-8",
    )

    nav_data = pd.DataFrame(
        [
            {
                "scheme_code": "1001",
                "scheme_name": "Test Flexi Cap Fund",
                "net_asset_value": 250.0,
                "date": "18-Aug-2026",
            }
        ]
    )

    monkeypatch.setattr(
        portfolio_analyzer,
        "fetch_latest_nav",
        lambda: nav_data,
    )

    result = portfolio_analyzer.analyze_portfolio(
        portfolio_file
    )

    assert result["status"] == "no_holdings_matched"
    assert result["holdings"][0]["status"] == "no_match"