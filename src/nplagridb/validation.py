"""Validation helpers for dataset columns."""

from __future__ import annotations

import pandas as pd


def validate_columns(data: pd.DataFrame, required: list[str]) -> dict[str, object]:
    """Check whether a DataFrame contains required columns."""

    available = list(data.columns)
    missing = [column for column in required if column not in data.columns]
    return {
        "valid": not missing,
        "required": required,
        "available": available,
        "missing": missing,
    }
