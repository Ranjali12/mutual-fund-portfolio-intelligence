import json
from pathlib import Path


def load_portfolio(path: str | Path) -> dict:
    """Load and validate the investor portfolio JSON."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Portfolio file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        portfolio = json.load(file)

    if "investor" not in portfolio:
        raise ValueError("Missing 'investor' section.")

    if "holdings" not in portfolio:
        raise ValueError("Missing 'holdings' section.")

    if not isinstance(portfolio["holdings"], list):
        raise ValueError("'holdings' must be a list.")

    if not portfolio["holdings"]:
        raise ValueError("Portfolio must contain at least one holding.")

    for index, holding in enumerate(portfolio["holdings"]):
        required_fields = {
            "fund_name",
            "units",
            "purchase_price",
        }

        missing_fields = required_fields - holding.keys()

        if missing_fields:
            raise ValueError(
                f"Holding {index + 1} is missing: "
                f"{', '.join(sorted(missing_fields))}"
            )

        if holding["units"] <= 0:
            raise ValueError(
                f"Holding {index + 1}: units must be greater than zero."
            )

        if holding["purchase_price"] <= 0:
            raise ValueError(
                f"Holding {index + 1}: purchase_price must be greater than zero."
            )

    return portfolio