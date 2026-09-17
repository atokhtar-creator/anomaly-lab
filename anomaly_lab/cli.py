from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from anomaly_lab.analyzer import analyze_dataframe


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze CSV data quality and detect anomalies.")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument(
        "--contamination",
        type=float,
        default=0.1,
        help="Expected anomaly fraction for IsolationForest",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if not 0 < args.contamination <= 0.5:
        raise SystemExit("--contamination must be in the range (0, 0.5].")

    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_path)
    result = analyze_dataframe(df, contamination=args.contamination)
    result.analyzed.to_csv(output_dir / "analyzed.csv", index=False)
    (output_dir / "report.json").write_text(json.dumps(result.report, indent=2), encoding="utf-8")
    print(json.dumps(result.report, indent=2))


if __name__ == "__main__":
    main()
