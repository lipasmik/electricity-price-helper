# Electricity Price Helper

A small Python program for monitoring future electricity prices using the Pörssisähkö API (https://porssisahko.net/api).

The project demonstrates a lightweight automation and testing approach, including:

- Configurable price thresholds
- Filtering future electricity prices
- Unit testing with pytest
- API validation using Playwright
- Automated test execution with GitHub Actions

## Features

The application can:

- Fetch latest electricity prices from the Pörssisähkö API
- Display future hours below a configurable price limit
- Display future hours above a configurable price limit
- Format output in a user-friendly way

Example output:

```text
Good time to heat the sauna:
30.05 22:00 - 23:00, 4.2 c/kWh

High electricity prices expected:
31.05 08:00 - 09:00, 12.5 c/kWh
```

## Project Structure

```text
src/
  price_helper.py

tests/
  test_price_helper.py
  test_e2e_price_flow.py

.github/workflows/
  tests.yml
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright runtime:

```bash
python -m playwright install
```

## Running the Application

Run with default thresholds:

```bash
python src/price_helper.py
```

Custom thresholds can be provided via command-line arguments:

```bash
python src/price_helper.py --under 5 --over 10
```

Arguments:

- `--under`
  Show future hours below this price threshold

- `--over`
  Show future hours above this price threshold

## Running Tests

Run all tests:

```bash
pytest -v
```

Generate HTML test reports:

```bash
pytest -v --html=reports/test-report.html --self-contained-html
```

The tests include:

- Unit tests for filtering and formatting logic
- Boundary value tests
- Playwright API tests against the live endpoint

## Continuous Integration

Tests are automatically executed using GitHub Actions on every push and pull request.

The CI pipeline:

- Runs unit tests and E2E tests separately
- Generates HTML test reports
- Uploads reports as build artifacts

## Future Improvements

Possible future enhancements could include:

- Scheduled execution using GitHub Actions
- Email notifications for price alerts
- Docker containerization
