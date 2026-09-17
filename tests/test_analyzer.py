import pandas as pd

from anomaly_lab.analyzer import analyze_dataframe


def test_report_contains_expected_metrics():
    df = pd.DataFrame(
        {
            "amount": [100, 110, 120, 5000],
            "items": [1, 1, 2, 20],
            "channel": ["a", "a", "b", "b"],
        }
    )

    result = analyze_dataframe(df, contamination=0.25)

    assert result.report["rows"] == 4
    assert result.report["columns"] == 3
    assert result.report["numeric_columns"] == ["amount", "items"]
    assert result.report["anomaly_count"] == 1
    assert "is_anomaly" in result.analyzed.columns


def test_empty_dataframe_is_rejected():
    df = pd.DataFrame()

    try:
        analyze_dataframe(df)
    except ValueError as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError")
