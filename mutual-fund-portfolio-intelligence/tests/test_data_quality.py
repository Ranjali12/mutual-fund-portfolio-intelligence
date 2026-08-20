from src.analytics.data_quality import assess_data_quality


def test_flags_unusually_large_return():
    holdings = [
        {
            "fund_name": "HDFC Flexi Cap Fund",
            "return_percentage": 1040.89,
        }
    ]

    warnings = assess_data_quality(holdings)

    assert len(warnings) == 1
    assert warnings[0]["type"] == "unusually_large_return"
    assert warnings[0]["return_percentage"] == 1040.89


def test_normal_return_has_no_warning():
    holdings = [
        {
            "fund_name": "Test Fund",
            "return_percentage": 25.0,
        }
    ]

    warnings = assess_data_quality(holdings)

    assert warnings == []