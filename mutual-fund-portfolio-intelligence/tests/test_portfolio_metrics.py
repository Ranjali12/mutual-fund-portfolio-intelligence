from src.analytics.portfolio_metrics import (
    calculate_holding_metrics,
    calculate_portfolio_allocation,
    assess_concentration,
)


def test_calculate_holding_metrics():
    result = calculate_holding_metrics(
        units=100,
        purchase_price=200,
        current_nav=250,
    )

    assert result["investment_cost"] == 20_000
    assert result["current_value"] == 25_000
    assert result["profit_loss"] == 5_000
    assert result["return_percentage"] == 25.0


def test_calculate_portfolio_allocation():
    holdings = [
        {"fund_name": "Fund A", "current_value": 60_000},
        {"fund_name": "Fund B", "current_value": 25_000},
        {"fund_name": "Fund C", "current_value": 15_000},
    ]

    result = calculate_portfolio_allocation(holdings)

    assert result["total_portfolio_value"] == 100_000
    assert result["holdings"][0]["allocation_percentage"] == 60.0
    assert result["holdings"][1]["allocation_percentage"] == 25.0
    assert result["holdings"][2]["allocation_percentage"] == 15.0


def test_assess_concentration():
    holdings = [
        {
            "fund_name": "Fund A",
            "current_value": 60_000,
            "allocation_percentage": 60.0,
        },
        {
            "fund_name": "Fund B",
            "current_value": 25_000,
            "allocation_percentage": 25.0,
        },
        {
            "fund_name": "Fund C",
            "current_value": 15_000,
            "allocation_percentage": 15.0,
        },
    ]

    result = assess_concentration(holdings)

    assert result["holdings"][0]["concentration_level"] == "high"
    assert result["holdings"][1]["concentration_level"] == "low"
    assert result["holdings"][2]["concentration_level"] == "low"