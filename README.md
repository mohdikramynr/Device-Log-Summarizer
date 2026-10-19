# Device Log Summarizer

A small Python project I built for the TestRight Nanosystems assignment.
It reads device temperature data from a CSV file, works out a few numbers
for each device, and draws a chart of the results.

## What it does
- Reads device_id, status and temperature from the CSV
- For every device it finds the total records, the average temperature and
  how many records are ERROR
- Leaves out devices whose average temperature is above 80
- Saves the result in summary.json, prints a table, and saves a bar chart
  as chart.png
- Shows a clear message if the file is missing or a row has bad data,
  instead of crashing

## Files
- task1_cleaning.py : cleans a list of sensor readings (Section 1)
- main.py : the CSV summarizer (Section 2)
- plot_chart.py : makes the chart (Section 3)
- device_telemetry.csv : sample data I made for testing
- PROMPT_LOG.md : how I used AI while working on this

## How to run
    python -m pip install matplotlib
    python task1_cleaning.py
    python main.py device_telemetry.csv
    python plot_chart.py summary.json

## Note
The original CSV was not shared with the assignment, so I created a small
sample file with the same three columns to test everything.