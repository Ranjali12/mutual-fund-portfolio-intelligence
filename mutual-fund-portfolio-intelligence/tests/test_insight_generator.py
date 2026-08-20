import json

from src.intelligence import insight_generator


def test_generate_insights(monkeypatch):
    analysis = {
        "investor": {
            "risk_profile": "moderate",
            "investment_horizon_years": 5,
            "primary_goal": "wealth_creation",
        },
        "total_portfolio_value": 100_000,
        "analyzed_holdings": [
            {
                "fund_name": "Test Fund",
                "current_value": 60_000,
                "allocation_percentage": 60.0,
                "concentration_level": "high",
                "profit_loss": 5_000,
                "return_percentage": 10.0,
            }
        ],
    }

    expected_response = {
        "overall_assessment": "Portfolio has concentration risk.",
        "insights": [
            {
                "priority": "high",
                "type": "concentration",
                "finding": "One fund represents 60% of the portfolio.",
                "why_it_matters": "This creates concentration risk.",
                "evidence": ["allocation_percentage: 60.0"],
                "action": "Review portfolio diversification.",
            }
        ],
    }

    class MockResponse:
        text = json.dumps(expected_response)

    class MockModels:
        def generate_content(
            self,
            model,
            contents,
            config=None,
        ):
            return MockResponse()

    class MockClient:
        models = MockModels()

    monkeypatch.setattr(
        insight_generator.genai,
        "Client",
        lambda api_key: MockClient(),
    )

    monkeypatch.setenv(
        "GEMINI_API_KEY",
        "test-key",
    )

    result = insight_generator.generate_insights(analysis)

    assert result == expected_response
    assert result["insights"][0]["priority"] == "high"
    assert result["insights"][0]["type"] == "concentration"