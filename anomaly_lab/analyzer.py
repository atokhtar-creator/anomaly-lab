from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
from sklearn.ensemble import IsolationForest


@dataclass
class AnalysisResult:
    analyzed: pd.DataFrame
    report: dict


def analyze_dataframe(
    df: pd.DataFrame,
    contamination: float = 0.1,
    random_state: int = 42,
) -> AnalysisResult:
    if df.empty:
        raise ValueError("Input dataframe is empty.")

    work = df.copy()
    numeric_columns = work.select_dtypes(include="number").columns.tolist()
    missing = work.isna().sum().to_dict()
    duplicate_rows = int(work.duplicated().sum())

    anomaly_count = 0
    work["is_anomaly"] = False

    if numeric_columns:
        features = work[numeric_columns].copy()
        features = features.fillna(features.median(numeric_only=True)).fillna(0)
        model = IsolationForest(contamination=contamination, random_state=random_state)
        labels = model.fit_predict(features)
        work["is_anomaly"] = labels == -1
        anomaly_count = int(work["is_anomaly"].sum())

    report = {
        "rows": int(len(work)),
        "columns": int(len(df.columns)),
        "duplicate_rows": duplicate_rows,
        "numeric_columns": numeric_columns,
        "missing_values": {k: int(v) for k, v in missing.items()},
        "anomaly_count": anomaly_count,
    }

    return AnalysisResult(analyzed=work, report=report)
