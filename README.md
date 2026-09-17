# Anomaly Lab

A compact data-quality and anomaly-detection toolkit for CSV datasets.

The CLI produces a reproducible report with missing-value statistics, duplicate counts, descriptive statistics, and Isolation Forest anomaly labels.

## Features

- CSV ingestion
- Automatic numeric-column detection
- Missing-value report
- Duplicate detection
- Isolation Forest anomaly detection
- Exported CSV with anomaly labels
- JSON summary report
- CLI interface
- Unit tests
- GitHub Actions CI

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python -m anomaly_lab.cli \
  --input data/sample_transactions.csv \
  --output output
```

Generated files:

```text
output/
  analyzed.csv
  report.json
```

## Example report

```json
{
  "rows": 20,
  "columns": 4,
  "duplicate_rows": 1,
  "numeric_columns": ["amount", "items"],
  "anomaly_count": 2
}
```

## How anomaly detection works

`IsolationForest` isolates unusual points using randomized decision trees. Rows that are easier to isolate are more likely to be anomalies.

This repository uses anomaly detection as a **signal**, not as an automatic decision-maker. Domain review is still required.

## Project structure

```text
anomaly_lab/
  analyzer.py
  cli.py
data/
  sample_transactions.csv
tests/
  test_analyzer.py
```

## Roadmap

- [ ] HTML report
- [ ] Configurable feature selection
- [ ] Time-series anomaly mode
- [ ] Visualization dashboard
- [ ] Schema validation

## License

MIT
