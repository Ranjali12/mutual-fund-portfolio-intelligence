import pandas as pd

from src.data.fund_matcher import find_fund_matches


def test_partial_fund_match():
    nav_data = pd.DataFrame(
        [
            {
                "scheme_code": "1001",
                "scheme_name": "HDFC Flexi Cap Fund - Direct Plan - Growth",
                "net_asset_value": 250.50,
                "date": "2026-08-18",
            },
            {
                "scheme_code": "1002",
                "scheme_name": "HDFC Balanced Advantage Fund - Direct Plan - Growth",
                "net_asset_value": 500.25,
                "date": "2026-08-18",
            },
        ]
    )

    matches = find_fund_matches(
        "HDFC Flexi Cap",
        nav_data,
    )

    assert len(matches) == 1
    assert (
        matches[0]["scheme_name"]
        == "HDFC Flexi Cap Fund - Direct Plan - Growth"
    )


def test_no_fund_match():
    nav_data = pd.DataFrame(
        [
            {
                "scheme_code": "1001",
                "scheme_name": "HDFC Flexi Cap Fund - Direct Plan - Growth",
                "net_asset_value": 250.50,
                "date": "2026-08-18",
            }
        ]
    )

    matches = find_fund_matches(
        "Completely Unknown Fund",
        nav_data,
    )

    assert matches == []