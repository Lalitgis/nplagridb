# nplagridb (Coming Soon...)

**A lightweight Python package template for organizing, validating, analyzing, and visualizing multi-year Nepal agriculture and livestock datasets stored as CSV files.**

`nplagridb` is designed for researchers, students, analysts, public-sector teams, and data maintainers who work with Nepal's crop and livestock records across years, districts, provinces, commodities, indicators, and units. It provides a clean package structure for shipping CSV-backed datasets with reusable Python utilities, while keeping the raw data transparent and easy to update.

The package follows a tidy-data approach: each row should represent one observation, and each column should represent one variable. This makes the dataset easier to filter, summarize, plot, validate, and combine with other administrative or geospatial data.

## What This Package Provides

- Load all crop CSV files, all livestock CSV files, or both categories together.
- Automatically add useful provenance columns such as `category` and `source_file`.
- Normalize column names into consistent lowercase `snake_case`.
- Produce summary statistics by year, district, province, item, indicator, category, or any available column.
- Create simple trend plots for quick exploration and reporting.
- Validate whether expected columns are present before analysis.
- Package raw data, metadata, and Python utilities in a reproducible project layout.

## Why nplagridb?

Agriculture and livestock data are often distributed as separate spreadsheets, annual tables, district reports, or manually maintained CSV files. Over time, column names may drift, units may vary, and files may become difficult to compare across years.

`nplagridb` gives you a practical foundation for managing that complexity. It does not hide the raw files. Instead, it keeps them versioned, readable, and documented while adding a Python interface for common analytical workflows.

Use it as:

- a starter package for a Nepal agriculture and livestock data project,
- a local research database backed by CSV files,
- a teaching example for tidy agricultural data,
- a reproducible data release template,
- or a foundation for a future PyPI package with external data hosting.

## Folder Layout

```text
nplagridb/
  pyproject.toml
  README.md
  src/
    nplagridb/
      __init__.py
      dataset.py
      plotting.py
      validation.py
      data/
        raw/
          crops/
            sample_crops.csv
          livestock/
            sample_livestock.csv
        metadata/
          columns.csv
```

Replace the sample CSV files with your real data, or keep the samples and add your files beside them.

## Recommended CSV Structure

For the smoothest experience, store data in tidy format with one row per observation:

```csv
year,province,district,item,indicator,value,unit
2020,Bagmati,Kathmandu,Rice,Production,12000,metric_ton
2020,Bagmati,Kathmandu,Rice,Area,3500,hectare
```

For livestock records:

```csv
year,province,district,item,indicator,value,unit
2020,Lumbini,Rupandehi,Cattle,Population,25000,head
2020,Lumbini,Rupandehi,Milk,Production,4500,metric_ton
```

Recommended core columns:

| Column | Description | Example |
|---|---|---|
| `year` | Observation year | `2020` |
| `province` | Province name | `Bagmati` |
| `district` | District name | `Kathmandu` |
| `item` | Crop, livestock type, or product | `Rice`, `Cattle`, `Milk` |
| `indicator` | Measured variable | `Production`, `Area`, `Population` |
| `value` | Numeric measurement | `12000` |
| `unit` | Measurement unit | `metric_ton`, `hectare`, `head` |

The loader standardizes column names automatically. For example:

| Original column name | Normalized column name |
|---|---|
| `Year` | `year` |
| `District Name` | `district_name` |
| `Production (MT)` | `production_mt` |
| `Crop Area (Ha)` | `crop_area_ha` |

## Installation

From the project folder:

```bash
python -m pip install -e .
```

This installs the package in editable mode, which is useful while you are adding data files or improving the loader.

## Basic Usage

```python
import nplagridb as nal

crops = nal.load_crops()
livestock = nal.load_livestock()
all_data = nal.load_dataset()

print(all_data.head())
print(nal.summary(all_data, group_by=["year", "category"]))
```

## Loading Data

Load only crop files:

```python
import nplagridb as nal

crops = nal.load_crops()
print(crops.shape)
```

Load only livestock files:

```python
import nplagridb as nal

livestock = nal.load_livestock()
print(livestock.shape)
```

Load both categories:

```python
import nplagridb as nal

data = nal.load_dataset()
print(data[["year", "district", "item", "indicator", "value", "category"]].head())
```

Each loaded row includes:

- `category`: identifies whether the row came from crop or livestock data.
- `source_file`: records the original CSV filename.

These columns make it easier to trace results back to their source files.

## Summary Statistics

Summarize by year and category:

```python
import nplagridb as nal

data = nal.load_dataset()
yearly = nal.summary(data, group_by=["year", "category"])
print(yearly)
```

Summarize by district and item:

```python
district_items = nal.summary(data, group_by=["district", "item"])
print(district_items)
```

Summarize by any column available in your dataset:

```python
province_summary = nal.summary(data, group_by=["province"])
print(province_summary)
```

## Plotting Trends

Create a simple trend plot:

```python
import matplotlib.pyplot as plt
import nplagridb as nal

data = nal.load_dataset()

nal.plot_trend(
    data,
    year_col="year",
    value_col="value",
    group_col="category",
    title="Nepal Agriculture and Livestock Trend",
)

plt.show()
```

Example use cases:

- compare crop and livestock values across years,
- inspect production trends for a selected commodity,
- check whether district-level records have unexpected gaps,
- create quick exploratory visuals before deeper analysis.

## Data Validation

Validate that required columns are present:

```python
import nplagridb as nal

data = nal.load_dataset()

report = nal.validate_columns(
    data,
    required=["year", "district", "item", "value"],
)

print(report)
```

Validation is especially helpful when new CSV files are added by different contributors or copied from external reports with inconsistent headers.

## Metadata

Maintain a data dictionary in:

```text
src/nplagridb/data/metadata/columns.csv
```

A useful metadata table may include:

```csv
column,description,example,required,notes
year,Observation year,2020,yes,Use Gregorian calendar year unless documented otherwise
province,Province name,Bagmati,recommended,Use consistent spelling
district,District name,Kathmandu,yes,Use official district names where possible
item,Crop/livestock/product name,Rice,yes,Keep names stable across files
indicator,Measured variable,Production,yes,Examples: Production Area Population Yield
value,Numeric value,12000,yes,Avoid commas inside numeric values
unit,Measurement unit,metric_ton,recommended,Use controlled unit labels
```

## Dataset Management Guidelines

- Keep raw CSVs unchanged in `src/nplagridb/data/raw/`.
- Store crop files in `data/raw/crops/`.
- Store livestock files in `data/raw/livestock/`.
- Use stable, descriptive filenames such as `crops_2010_2024.csv` or `livestock_district_2005_2024.csv`.
- Maintain a data dictionary in `data/metadata/columns.csv`.
- Track source, license, collection method, and update date in this README or a separate metadata file.
- Prefer tidy rows: `year`, `province`, `district`, `item`, `indicator`, `value`, `unit`.
- Avoid changing old raw files after release. Add corrected or versioned files when data changes.
- Add tests whenever you change column conventions, loader behavior, or validation rules.
- Increase the package version when included data changes.
- For large datasets, publish the code package separately and host the data through a documented downloader.

## Suggested Data Quality Checks

Before publishing or sharing a dataset, consider checking:

- Are all expected years present?
- Are district and province names spelled consistently?
- Are numeric columns stored as numbers rather than text?
- Are units documented and consistent within each indicator?
- Are duplicate rows intentional?
- Are missing values represented consistently?
- Can each source file be traced to an original report or data provider?

## Building a Distributable Package

Install build tools:

```bash
python -m pip install build twine
```

Build the package:

```bash
python -m build
```

This creates distribution files inside:

```text
dist/
```

You can share the `.whl` file privately, upload to TestPyPI for testing, or publish to PyPI when the package is ready.

## Versioning

Use semantic versioning where possible:

- Patch version changes, such as `0.1.1`, for small documentation fixes or metadata corrections.
- Minor version changes, such as `0.2.0`, for new data files or new helper functions.
- Major version changes, such as `1.0.0`, for stable public releases or breaking changes.

Because this package may include data, document both code changes and data changes in release notes.

## Citation

If you use this package or its dataset in research, reports, dashboards, or derived data products, cite it as:

```text
nplagridb maintainers. nplagridb: Nepal Agriculture and Livestock Dataset, version 0.1.0, 2026.
```

Suggested BibTeX entry:

```bibtex
@misc{nplagridb2026,
  title = {nplagridb: Nepal Agriculture and Livestock Dataset},
  author = {{Lalit BC}},
  year = {2026},
  version = {0.1.0},
  note = {Python package and CSV dataset}
}
```

## License

Add the appropriate license for both:

- the package code, and
- the included dataset.

Code and data may require different licenses. If the data comes from government reports, surveys, publications, or institutional sources, document the original source and usage terms clearly.

## Project Status

`nplagridb` is a package template and early-stage data management structure. It is ready to be adapted with real Nepal agriculture and livestock CSV files, expanded metadata, additional validation rules, and tests.

Contributions that improve data documentation, loader reliability, validation coverage, and analytical examples are welcome.
