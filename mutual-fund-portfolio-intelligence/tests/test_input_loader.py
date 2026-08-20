import json

import pytest

from src.models.input_loader import load_portfolio


def test_load_valid_portfolio(tmp_path):
    portfolio = {
        "investor": {
            "risk_profile": "moderate",
            "investment_horizon_years": 5,
            "primary_goal": "wealth_creation",
        },
        "holdings": [
            {
                "fund_name": "HDFC Flexi Cap Fund",
                "units": 50,
                "purchase_price": 200.0,
            }
        ],
    }

    file_path = tmp_path / "portfolio.json"
    file_path.write_text(
        json.dumps(portfolio),
        encoding="utf-8",
    )

    result = load_portfolio(file_path)

    assert result["investor"]["risk_profile"] == "moderate"
    assert len(result["holdings"]) == 1
    assert result["holdings"][0]["units"] == 50


def test_missing_holdings(tmp_path):
    portfolio = {
        "investor": {
            "risk_profile": "moderate",
            "investment_horizon_years": 5,
            "primary_goal": "wealth_creation",
        }
    }

    file_path = tmp_path / "portfolio.json"
    file_path.write_text(
        json.dumps(portfolio),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing 'holdings' section"):
        load_portfolio(file_path)


def test_invalid_units(tmp_path):
    portfolio = {
        "investor": {
            "risk_profile": "moderate",
            "investment_horizon_years": 5,
            "primary_goal": "wealth_creation",
        },
        "holdings": [
            {
                "fund_name": "HDFC Flexi Cap Fund",
                "units": -10,
                "purchase_price": 200.0,
            }
        ],
    }

    file_path = tmp_path / "portfolio.json"
    file_path.write_text(
        json.dumps(portfolio),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="units must be greater than zero"):
        load_portfolio(file_path)