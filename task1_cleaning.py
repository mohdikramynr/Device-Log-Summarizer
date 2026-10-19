import math


def clean_sensor_readings(values):
    """Convert mixed inputs to floats, drop invalid/negative values, cap at 500.0."""
    cleaned = []

    for value in values:
        try:
            number = float(value)
        except (ValueError, TypeError):
            continue

        # Skip NaN, infinity and negative values
        if not math.isfinite(number) or number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned


def run_tests():
    assert clean_sensor_readings([100, "250", None, -10, "abc", 600, 350]) == [100.0, 250.0, 500.0, 350.0]
    assert clean_sensor_readings([]) == []
    assert clean_sensor_readings([None, "hello", -20, -5]) == []
    print("All tests passed")


if __name__ == "__main__":
    run_tests()