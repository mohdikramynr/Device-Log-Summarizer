import argparse
import json
import math
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def load_summary(path):
    """Load and validate device summary data from a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of devices.")

    if not data:
        raise ValueError("No device data found in the JSON file.")

    required_fields = {
        "device_id",
        "avg_temperature",
    }

    for index, device in enumerate(data):
        if not isinstance(device, dict):
            raise ValueError(f"Invalid device data at index {index}.")

        if not required_fields.issubset(device):
            raise ValueError(
                f"Missing required fields at index {index}."
            )

        if not isinstance(device["device_id"], str):
            raise ValueError(
                f"Invalid device ID at index {index}."
            )

        try:
            temperature = float(device["avg_temperature"])
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid temperature at index {index}."
            ) from None

        if not math.isfinite(temperature) or temperature < 0:
            raise ValueError(
                f"Temperature must be finite and non-negative at index {index}."
            )

        device["avg_temperature"] = temperature

    return data


def plot(data, output):
    """Create and save a bar chart of average device temperatures."""
    device_ids = [device["device_id"] for device in data]
    temperatures = [
        device["avg_temperature"] for device in data
    ]

    figure_width = max(7, len(device_ids) * 1.2)

    fig, ax = plt.subplots(figsize=(figure_width, 5))

    bars = ax.bar(
        device_ids,
        temperatures,
        color="#1f77b4",
        edgecolor="black",
        linewidth=0.5,
    )

    ax.set_title(
        "Average Temperature per Device",
        fontsize=14,
        pad=15,
    )
    ax.set_xlabel("Device ID", fontsize=11)
    ax.set_ylabel("Average Temperature (°C)", fontsize=11)

    # Keep the chart readable, even when all temperatures are zero.
    max_temperature = max(temperatures)
    upper_limit = max(1, max_temperature * 1.15)
    ax.set_ylim(0, upper_limit)

    # Display temperature values above the bars.
    ax.bar_label(
        bars,
        labels=[f"{temperature:.2f}" for temperature in temperatures],
        padding=3,
        fontsize=9,
    )

    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    plt.setp(
        ax.get_xticklabels(),
        rotation=45,
        ha="right",
    )

    fig.tight_layout()

    try:
        fig.savefig(output, dpi=150, bbox_inches="tight")
    finally:
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Plot average temperature per device."
    )

    parser.add_argument(
        "json_path",
        help="Path to the summary JSON file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="chart.png",
        help="Output image filename (default: chart.png).",
    )

    args = parser.parse_args()

    try:
        data = load_summary(args.json_path)
        plot(data, args.output)

    except FileNotFoundError:
        print(
            f"Error: File not found: {args.json_path}",
            file=sys.stderr,
        )
        return 1

    except PermissionError:
        print(
            "Error: Permission denied while reading or saving a file.",
            file=sys.stderr,
        )
        return 1

    except (ValueError, KeyError, json.JSONDecodeError) as error:
        print(
            f"Error: Invalid summary data: {error}",
            file=sys.stderr,
        )
        return 1

    except OSError as error:
        print(
            f"Error: Could not save the chart: {error}",
            file=sys.stderr,
        )
        return 1

    print(f"Chart saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())