"""Dataset loading and summary utilities."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
import re
from typing import Iterable, Literal

import pandas as pd

Category = Literal["crops", "livestock"]


PACKAGE_DATA_ROOT = resources.files("nplagridb").joinpath("data", "raw")


def _normalize_column(name: object) -> str:
    text = str(name).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _read_csv(path: Path, category: Category, normalize_columns: bool = True) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if normalize_columns:
        frame = frame.rename(columns={col: _normalize_column(col) for col in frame.columns})
    frame["category"] = category
    frame["source_file"] = path.name
    return frame


def available_files(category: Category | None = None) -> list[str]:
    """Return packaged CSV files.

    Parameters
    ----------
    category:
        Optional category name: ``"crops"`` or ``"livestock"``.
    """

    categories: Iterable[Category] = [category] if category else ["crops", "livestock"]
    files: list[str] = []
    for item in categories:
        category_root = PACKAGE_DATA_ROOT.joinpath(item)
        files.extend(str(path) for path in category_root.iterdir() if path.name.endswith(".csv"))
    return sorted(files)


def load_category(
    category: Category,
    data_dir: str | Path | None = None,
    normalize_columns: bool = True,
) -> pd.DataFrame:
    """Load all CSV files for one dataset category.

    ``data_dir`` can point to an external folder with ``crops`` and ``livestock``
    subfolders. If omitted, packaged CSVs are used.
    """

    root = Path(data_dir) if data_dir else PACKAGE_DATA_ROOT
    category_root = root / category
    paths = sorted(category_root.glob("*.csv"))

    if not paths:
        raise FileNotFoundError(f"No CSV files found in {category_root}")

    frames = [_read_csv(path, category, normalize_columns) for path in paths]
    return pd.concat(frames, ignore_index=True, sort=False)


def load_crops(data_dir: str | Path | None = None, normalize_columns: bool = True) -> pd.DataFrame:
    """Load crop CSV files."""

    return load_category("crops", data_dir=data_dir, normalize_columns=normalize_columns)


def load_livestock(data_dir: str | Path | None = None, normalize_columns: bool = True) -> pd.DataFrame:
    """Load livestock CSV files."""

    return load_category("livestock", data_dir=data_dir, normalize_columns=normalize_columns)


def load_dataset(data_dir: str | Path | None = None, normalize_columns: bool = True) -> pd.DataFrame:
    """Load crop and livestock CSV files into one DataFrame."""

    frames = [
        load_crops(data_dir=data_dir, normalize_columns=normalize_columns),
        load_livestock(data_dir=data_dir, normalize_columns=normalize_columns),
    ]
    return pd.concat(frames, ignore_index=True, sort=False)


def summary(
    data: pd.DataFrame,
    group_by: str | list[str] | None = None,
    value_col: str = "value",
) -> pd.DataFrame:
    """Return summary statistics for numeric data.

    If ``group_by`` is omitted, the function tries useful default columns that
    are present in the dataset: ``year``, ``category``, ``province``, ``district``,
    ``item``, and ``indicator``.
    """

    if value_col not in data.columns:
        numeric_cols = data.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            raise ValueError("No numeric columns found for summary statistics.")
        value_col = numeric_cols[0]

    if group_by is None:
        defaults = ["year", "category", "province", "district", "item", "indicator"]
        group_columns = [col for col in defaults if col in data.columns]
    elif isinstance(group_by, str):
        group_columns = [group_by]
    else:
        group_columns = list(group_by)

    missing = [col for col in group_columns if col not in data.columns]
    if missing:
        raise KeyError(f"Missing group_by columns: {missing}")

    if not group_columns:
        return data[value_col].describe().to_frame().T

    return (
        data.groupby(group_columns, dropna=False)[value_col]
        .agg(["count", "mean", "min", "max", "sum"])
        .reset_index()
    )
