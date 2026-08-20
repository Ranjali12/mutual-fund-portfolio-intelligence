import difflib
import re

import pandas as pd


OUTPUT_COLUMNS = [
    "scheme_code",
    "scheme_name",
    "net_asset_value",
    "date",
]


def _normalize_name(name: str) -> str:
    """Normalize a fund name for comparison."""

    name = str(name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def _has_variant(
    scheme_name: str,
    variant: str,
) -> bool:
    """Check whether a scheme contains a requested variant."""

    normalized = _normalize_name(scheme_name)

    if variant == "direct":
        return "direct" in normalized

    if variant == "growth":
        return "growth" in normalized

    if variant == "idcw":
        return "idcw" in normalized

    if variant == "regular":
        return "regular" in normalized

    return False


def find_fund_matches(
    fund_name: str,
    nav_data: pd.DataFrame,
    limit: int = 5,
) -> list[dict]:
    """Find likely AMFI scheme matches for a user-provided fund name."""

    if not fund_name.strip():
        return []

    query = _normalize_name(fund_name)

    normalized_names = nav_data["scheme_name"].fillna("").map(
        _normalize_name
    )

    # 1. Exact normalized match.
    exact_matches = nav_data[
        normalized_names == query
    ]

    if not exact_matches.empty:
        return exact_matches[
            OUTPUT_COLUMNS
        ].head(limit).to_dict(orient="records")

    # 2. Find the fund family using the meaningful words.
    query_words = set(query.split())

    generic_words = {
        "fund",
        "plan",
        "option",
        "direct",
        "regular",
        "growth",
        "idcw",
        "monthly",
        "quarterly",
    }

    family_words = query_words - generic_words

    def contains_family(scheme_name: str) -> bool:
        scheme_words = set(
            _normalize_name(scheme_name).split()
        )
        return family_words.issubset(scheme_words)

    family_matches = nav_data[
        nav_data["scheme_name"].fillna("").map(
            contains_family
        )
    ]

    if not family_matches.empty:
        # 3. Prefer requested plan type.
        requested_variants = []

        if "direct" in query_words:
            requested_variants.append("direct")

        if "growth" in query_words:
            requested_variants.append("growth")

        if "idcw" in query_words:
            requested_variants.append("idcw")

        if "regular" in query_words:
            requested_variants.append("regular")

        variant_matches = family_matches

        for variant in requested_variants:
            variant_matches = variant_matches[
                variant_matches["scheme_name"].map(
                    lambda name: _has_variant(
                        name,
                        variant,
                    )
                )
            ]

        if len(variant_matches) == 1:
            return variant_matches[
                OUTPUT_COLUMNS
            ].to_dict(orient="records")

        if not variant_matches.empty:
            return variant_matches[
                OUTPUT_COLUMNS
            ].head(limit).to_dict(orient="records")

        return family_matches[
            OUTPUT_COLUMNS
        ].head(limit).to_dict(orient="records")

    # 4. Conservative fuzzy matching.
    unique_names = normalized_names.unique()

    fuzzy_names = difflib.get_close_matches(
        query,
        unique_names,
        n=limit,
        cutoff=0.75,
    )

    if not fuzzy_names:
        return []

    matches = nav_data[
        normalized_names.isin(fuzzy_names)
    ].head(limit)

    return matches[
        OUTPUT_COLUMNS
    ].to_dict(orient="records")