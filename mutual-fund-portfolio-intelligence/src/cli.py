import json
from pathlib import Path

from src.analytics.portfolio_analyzer import analyze_portfolio
from src.intelligence.insight_generator import generate_insights


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO_PATH = PROJECT_ROOT / "data" / "investor_portfolio.json"


def print_portfolio_summary(analysis: dict) -> None:
    """Print a concise summary of the verified portfolio analysis."""

    holdings = analysis.get("analyzed_holdings", [])

    total_value = analysis.get("total_portfolio_value", 0.0)

    total_invested = sum(
        holding.get("investment_cost", 0.0)
        for holding in holdings
    )

    total_profit_loss = sum(
        holding.get("profit_loss", 0.0)
        for holding in holdings
    )

    print("\n" + "=" * 40)
    print("PORTFOLIO SUMMARY")
    print("=" * 40)

    print(f"\nTotal value:     ₹{total_value:,.2f}")
    print(f"Total invested:  ₹{total_invested:,.2f}")
    print(f"Overall P/L:     ₹{total_profit_loss:,.2f}")

    print("\nHoldings")

    for holding in holdings:
        fund_name = holding.get("scheme_name", holding["fund_name"])
        allocation = holding.get("allocation_percentage", 0.0)
        current_value = holding.get("current_value", 0.0)

        print(f"\n{fund_name}")
        print(f"  Current value: ₹{current_value:,.2f}")
        print(f"  Allocation:    {allocation:.2f}%")
        print(f"  Status:        {holding.get('status', 'unknown')}")

    warnings = analysis.get("data_quality_warnings", [])

    print(
        f"\nData quality warnings: {len(warnings)}"
    )

    for warning in warnings:
        print(
            f"  - {warning.get('message', 'Review required.')}"
        )


def main() -> None:
    """Run the Mutual Fund Portfolio Intelligence CLI."""

    print("\nMutual Fund Portfolio Intelligence")
    print("=" * 40)

    print("\nAnalyzing portfolio...")

    analysis = analyze_portfolio(PORTFOLIO_PATH)

    if analysis["status"] != "success":
        print("\nAnalysis could not be completed.")
        print(json.dumps(analysis, indent=2, default=str))
        return

    print_portfolio_summary(analysis)

    print("\nGenerating personalised insights...")

    try:
        insights = generate_insights(analysis)
    except (RuntimeError, ValueError) as exc:
        print(f"\nUnable to generate Gemini insights: {exc}")
        print(
            "\nThe deterministic portfolio analysis "
            "completed successfully."
        )
        return

    print("\n" + "=" * 40)
    print("PORTFOLIO INSIGHTS")
    print("=" * 40)

    print(
        f"\n{insights.get('overall_assessment', '')}"
    )

    for index, insight in enumerate(
        insights.get("insights", []),
        start=1,
    ):
        print(f"\n{index}. [{insight['priority'].upper()}]")
        print(f"Type: {insight['type']}")
        print(f"Finding: {insight['finding']}")
        print(f"Why it matters: {insight['why_it_matters']}")
        print(f"Evidence: {', '.join(insight['evidence'])}")
        print(f"Action: {insight['action']}")


if __name__ == "__main__":
    main()