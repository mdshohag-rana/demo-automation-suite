# Automation Demo

## Overview

This repository contains a Python-based UI automation project using `pytest` and `Playwright`. The suite is configured to execute browser tests against the `https://quotes.toscrape.com/` sample website.

Key features:
- `pytest` test discovery and execution
- `playwright` browser automation with Chromium
- video recording, tracing, and HTML screenshots on test execution
- `allure` integration for rich test reporting
- generated HTML report via `pytest-html`

## Repository Structure

- `tests/` - contains test cases written using Playwright Page objects and `pytest` fixtures
- `conftest.py` - shared fixtures for browser context, page handling, screenshots, video, and trace attachments
- `pytest.ini` - pytest configuration, browser settings, reporting options, and test discovery rules
- `requirements.txt` - Python dependencies required to run the automation suite
- `allure-results/` - generated Allure result files after test execution
- `test-results/` - generated HTML and JUnit XML reports
- `screenshots/`, `videos/`, `traces/` - saved artifacts for debugging and reporting

## Requirements

- Python 3.8+ (recommended)
- `pip` package manager
- Internet access to reach `https://quotes.toscrape.com/`

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install the required packages:

```powershell
pip install -r requirements.txt
```

3. Install Playwright browsers:

```powershell
python -m playwright install
```

## Running Tests

Run the full suite using:

```powershell
pytest
```

The current configuration in `pytest.ini` uses:
- Chromium browser
- `--headed` mode
- `--slowmo=200`
- screenshots, videos, and traces retained on failure
- HTML report output to `test-results/report.html`
- Allure results output to `allure-results`
- JUnit XML output to `report.xml`

### Run a specific test

```powershell
pytest tests/test_quotes.py -k "quotes_page_title"
```

### Run only smoke or regression tests

```powershell
pytest -m smoke
pytest -m regression
```

## Reporting

### HTML report

After execution, open the generated report file:

```powershell
start test-results\report.html
```

### Allure report

If Allure is installed, serve the results locally:

```powershell
allure serve allure-results
```

## Test Coverage and Artifacts

During each test run, the suite automatically collects:
- final screenshots in `screenshots/`
- HTML page source in `screenshots/`
- browser video recordings in `videos/`
- Playwright trace ZIP files in `traces/`
- Allure attachments for screenshots, page HTML, URLs, video, and trace archives

## Example Tests

The current suite includes basic validations for the Quotes to Scrape website:
- page URL and title checks
- quote visibility and content assertions
- top tag navigation validation
- negative login test for invalid credentials

## Notes

- `pytest.ini` is configured to run tests in headed mode. Remove `--headed` or modify `addopts` to run in headless mode.
- Screenshots and videos are captured even if tests pass, but `--screenshot=only-on-failure` and `--video=retain-on-failure` control retention behavior.
- The project uses `allure-pytest` for enhanced reporting and attachments.

## Troubleshooting

- If Chromium is not installed, rerun `python -m playwright install`.
- If tests fail due to network issues, verify internet access and the availability of `https://quotes.toscrape.com/`.
- If `allure` command is missing, install Allure or use the generated HTML report instead.
