# PROMPT_LOG.md

## Section 1: Sensor Data Cleaning
Written by me without AI. I used AI only afterwards for formatting
(docstring, assert-based tests).

## Section 2: Device Telemetry Summarizer
I used Claude to build the CSV summarizer (reading the CSV, grouping by
device, average temperature, ERROR count, filtering devices above 80,
JSON export, summary table, error handling). I ran it on a sample CSV
and fixed a missing `import math` after replacing `parse_temperature`
with an `isfinite` check.

## Section 3: Temperature Chart

### Initial prompt
Write a matplotlib script that loads summary.json and plots a bar chart
of average temperature per device.

### Bug in the first attempt
The first version produced a bare chart: no title, no axis labels, no
value labels on the bars, and no handling for a missing or empty JSON file.

### Follow-up prompt
Add a title, axis labels, value labels on bars, rotate x labels so they
don't overlap, use tight_layout, and show a clear error for a missing or
empty JSON file.

### Result
chart.png generated and checked manually.