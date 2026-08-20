def assess_data_quality(holdings: list[dict]) -> list[dict]:
    """Identify potentially suspicious or incomplete portfolio data."""

    warnings = []

    for holding in holdings:
        return_percentage = holding.get("return_percentage")

        if return_percentage is None:
            continue

        if abs(return_percentage) >= 500:
            warnings.append(
                {
                    "type": "unusually_large_return",
                    "fund_name": holding.get("fund_name"),
                    "return_percentage": return_percentage,
                    "message": (
                        "The calculated return is unusually large. "
                        "Verify the recorded units and purchase price "
                        "before relying on this figure."
                    ),
                }
            )

    return warnings