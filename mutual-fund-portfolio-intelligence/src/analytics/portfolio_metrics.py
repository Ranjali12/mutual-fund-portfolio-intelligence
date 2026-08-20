def calculate_holding_metrics(
    units: float,
    purchase_price: float,
    current_nav: float,
) -> dict:
    """Calculate basic metrics for one mutual-fund holding."""

    investment_cost = units * purchase_price
    current_value = units * current_nav
    profit_loss = current_value - investment_cost

    return_percentage = (
        (profit_loss / investment_cost) * 100
        if investment_cost > 0
        else 0.0
    )

    return {
        "investment_cost": investment_cost,
        "current_value": current_value,
        "profit_loss": profit_loss,
        "return_percentage": return_percentage,
    }


def calculate_portfolio_allocation(holdings: list[dict]) -> dict:
    """Calculate total portfolio value and allocation for each holding."""

    total_value = sum(
        holding["current_value"]
        for holding in holdings
    )

    if total_value <= 0:
        raise ValueError("Total portfolio value must be greater than zero.")

    for holding in holdings:
        holding["allocation_percentage"] = (
            holding["current_value"] / total_value
        ) * 100

    return {
        "total_portfolio_value": total_value,
        "holdings": holdings,
    }


def assess_concentration(holdings: list[dict]) -> dict:
    """Assess concentration based on each holding's portfolio allocation."""

    for holding in holdings:
        allocation = holding["allocation_percentage"]

        if allocation > 50:
            level = "high"
        elif allocation >= 30:
            level = "moderate"
        else:
            level = "low"

        holding["concentration_level"] = level

    return {
        "holdings": holdings,
    }