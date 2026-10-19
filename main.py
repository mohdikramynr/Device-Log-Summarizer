import argparse
import csv
import json
import math
import sys
from collections import defaultdict

VALID_STATUSES = {"ACTIVE", "WARNING", "ERROR"}


def parse_temperature(raw):
    """Return temperature as float, or None if missing/invalid."""
    try:
        value = float(str(raw).strip())
    except (TypeError, ValueError):
        return None

    if not math.isfinite(value):
        return None

    return value


def read_records(path):
    """Read the CSV and return (rows, skipped_count). Raises on file problems."""
    rows = []
    skipped = 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"device_id", "status", "temperature"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV must contain columns: {', '.join(sorted(required))}"
            )
        for line_no, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            if not device_id or status not in VALID_STATUSES:
                print(f"Warning: skipping line {line_no} (bad device_id/status)",
                      file=sys.stderr)
                skipped += 1
                continue
            rows.append(
                {
                    "device_id": device_id,
                    "status": status,
                    "temperature": parse_temperature(row.get("temperature")),
                }
            )
    return rows, skipped


def aggregate(rows):
    """Group by device_id and compute total records, mean temp, error count."""
    groups = defaultdict(list)
    for row in rows:
        groups[row["device_id"]].append(row)

    results = []
    for device_id, records in sorted(groups.items()):
        temps = [r["temperature"] for r in records if r["temperature"] is not None]
        if not temps:
            print(f"Warning: {device_id} has no valid temperature, skipped",
                  file=sys.stderr)
            continue
        results.append(
            {
                "device_id": device_id,
                "total_records": len(records),
                "avg_temperature": round(sum(temps) / len(temps), 2),
                "error_count": sum(1 for r in records if r["status"] == "ERROR"),
            }
        )
    return results


def filter_devices(results, max_avg_temp):
    """Keep only devices whose average temperature is <= max_avg_temp."""
    return [r for r in results if r["avg_temperature"] <= max_avg_temp]


def print_table(results):
    header = f"{'Device':<10}{'Records':>10}{'Avg Temp':>12}{'Errors':>10}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['device_id']:<10}{r['total_records']:>10}"
              f"{r['avg_temperature']:>12.2f}{r['error_count']:>10}")
    if not results:
        print("(no devices to show)")


def main():
    parser = argparse.ArgumentParser(description="Device Log Summarizer")
    parser.add_argument("csv_path", help="Path to device_telemetry.csv")
    parser.add_argument("-o", "--output", default="summary.json",
                        help="Output JSON file (default: summary.json)")
    parser.add_argument("--max-avg-temp", type=float, default=80.0,
                        help="Drop devices with average temperature above this")
    args = parser.parse_args()

    try:
        rows, skipped = read_records(args.csv_path)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_path}", file=sys.stderr)
        return 1
    except (ValueError, csv.Error, UnicodeDecodeError) as exc:
        print(f"Error: could not read CSV: {exc}", file=sys.stderr)
        return 1

    results = filter_devices(aggregate(rows), args.max_avg_temp)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print_table(results)
    print(f"\nSaved {len(results)} device(s) to {args.output} "
          f"({skipped} bad row(s) skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())