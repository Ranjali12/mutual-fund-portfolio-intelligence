import pandas as pd
import requests


AMFI_NAV_URL = "https://www.amfiindia.com/spages/NAVAll.txt"

COLUMNS = [
    "scheme_code",
    "isin_div_payout_growth",
    "isin_div_reinvestment",
    "scheme_name",
    "net_asset_value",
    "date",
]


def fetch_latest_nav() -> pd.DataFrame:
    """Fetch and parse latest mutual-fund NAV data from AMFI."""

    response = requests.get(
        AMFI_NAV_URL,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    response.raise_for_status()

    rows = []

    for line in response.text.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = [part.strip() for part in line.split(";")]

        # Keep only actual scheme records.
        # Category headings and AMC names do not have 6 fields.
        if len(parts) != 6:
            continue

        rows.append(parts)

    df = pd.DataFrame(rows, columns=COLUMNS)

    df["net_asset_value"] = pd.to_numeric(
        df["net_asset_value"],
        errors="coerce",
    )

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%b-%Y",
        errors="coerce",
    )

    return df


if __name__ == "__main__":
    df = fetch_latest_nav()

    print(df.head())
    print(f"\nRows fetched: {len(df)}")
    print("\nColumns:")
    print(df.columns.tolist())