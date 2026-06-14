"""Plotting helpers for the dataset."""

from __future__ import annotations

from typing import Any

import pandas as pd


def plot_trend(
    data: pd.DataFrame,
    year_col: str = "year",
    value_col: str = "value",
    group_col: str | None = None,
    title: str | None = None,
    ax: Any | None = None,
) -> Any:
    """Plot values over time, optionally split by one grouping column."""

    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "plot_trend requires matplotlib. Install it with: python -m pip install matplotlib"
        ) from exc

    for column in [year_col, value_col]:
        if column not in data.columns:
            raise KeyError(f"Column not found: {column}")

    ax = ax or plt.subplots(figsize=(9, 5))[1]
    plot_data = data.copy()
    plot_data[year_col] = pd.to_numeric(plot_data[year_col], errors="coerce")
    plot_data[value_col] = pd.to_numeric(plot_data[value_col], errors="coerce")
    plot_data = plot_data.dropna(subset=[year_col, value_col])

    if group_col:
        if group_col not in plot_data.columns:
            raise KeyError(f"Column not found: {group_col}")
        grouped = plot_data.groupby([year_col, group_col], dropna=False)[value_col].sum().reset_index()
        for label, group in grouped.groupby(group_col):
            ax.plot(group[year_col], group[value_col], marker="o", label=str(label))
        ax.legend(title=group_col)
    else:
        grouped = plot_data.groupby(year_col, dropna=False)[value_col].sum().reset_index()
        ax.plot(grouped[year_col], grouped[value_col], marker="o")

    ax.set_xlabel(year_col.replace("_", " ").title())
    ax.set_ylabel(value_col.replace("_", " ").title())
    ax.set_title(title or "Dataset Trend")
    ax.grid(True, alpha=0.25)
    return ax
