import nplagridb as nal


def test_load_dataset_has_categories():
    data = nal.load_dataset()

    assert {"crops", "livestock"} == set(data["category"])
    assert "source_file" in data.columns


def test_summary_returns_grouped_statistics():
    data = nal.load_dataset()
    result = nal.summary(data, group_by=["year", "category"])

    assert {"year", "category", "count", "mean", "min", "max", "sum"}.issubset(result.columns)


def test_validate_columns_reports_missing_columns():
    data = nal.load_dataset()
    report = nal.validate_columns(data, required=["year", "district", "not_a_column"])

    assert report["valid"] is False
    assert report["missing"] == ["not_a_column"]
