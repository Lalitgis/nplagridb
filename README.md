# nplagridb

Python package template for a multi-year Nepal agriculture and livestock dataset stored as CSV files.

## What this package gives you

- Load all crop CSVs, livestock CSVs, or both categories together.
- Add a `category` and `source_file` column automatically.
- Standardize column names for easier analysis.
- Produce summary statistics by year, district, province, item, or any available column.
- Create simple trend plots.
- Validate whether expected columns are present.

## Folder layout

```text
nplagridb/
  pyproject.toml
  src/
    nplagridb/
      data/
        raw/
          crops/
            sample_crops.csv
          livestock/
            sample_livestock.csv
        metadata/
          columns.csv
      dataset.py
      plotting.py
      validation.py
```

Replace the sample CSVs with your real files, or keep the samples and add your files beside them.

## Recommended CSV structure

Use one row per observation. A tidy structure is easiest to package and analyze:

```csv
year,province,district,item,indicator,value,unit
2020,Bagmati,Kathmandu,Rice,Production,12000,metric_ton
2020,Bagmati,Kathmandu,Rice,Area,3500,hectare
```

For livestock:

```csv
year,province,district,item,indicator,value,unit
2020,Lumbini,Rupandehi,Cattle,Population,25000,head
2020,Lumbini,Rupandehi,Milk,Production,4500,metric_ton
```

If your existing CSVs use names such as `Year`, `District Name`, or `Production (MT)`, the loader normalizes them to lowercase snake_case names such as `year`, `district_name`, and `production_mt`.

## Install locally

From this folder:

```bash
python -m pip install -e .
```

## Basic usage

```python
import nplagridb as nal

crops = nal.load_crops()
livestock = nal.load_livestock()
all_data = nal.load_dataset()

print(all_data.head())
print(nal.summary(all_data, group_by=["year", "category"]))
```

## Plot a trend

```python
import matplotlib.pyplot as plt
import nplagridb as nal

data = nal.load_dataset()
nal.plot_trend(
    data,
    year_col="year",
    value_col="value",
    group_col="category",
    title="Nepal agriculture and livestock trend",
)
plt.show()
```

## Validate your data

```python
import nplagridb as nal

data = nal.load_dataset()
report = nal.validate_columns(data, required=["year", "district", "item", "value"])
print(report)
```

## Building a distributable package

Install build tools:

```bash
python -m pip install build twine
```

Build:

```bash
python -m build
```

This creates files inside `dist/`. You can share the `.whl` file privately or publish to PyPI/TestPyPI later.

## Dataset management reference

1. Keep raw CSVs unchanged in `src/nplagridb/data/raw/`.
2. Store crop files in `data/raw/crops/` and livestock files in `data/raw/livestock/`.
3. Use stable, descriptive filenames, for example `crops_2010_2024.csv` or `livestock_district_2005_2024.csv`.
4. Maintain a data dictionary in `data/metadata/columns.csv`.
5. Track source, license, collection method, and update date in your README.
6. Prefer tidy rows: `year`, `province`, `district`, `item`, `indicator`, `value`, `unit`.
7. Avoid changing old raw files. Add new versioned files when data is corrected.
8. Add tests whenever you change column conventions or loader behavior.
9. Increase the package version when you update included data.
10. For large datasets, publish code on PyPI and host data separately with a downloader.

## Citation template

```text
nplagridb maintainers. nplagridb: Nepal Agriculture and Livestock Dataset, version 0.1.0, 2026.
```
