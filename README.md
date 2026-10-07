# IE7374 Lab 1 — GitHub Actions CI/CD Pipeline

## Overview

This lab implements a CI/CD pipeline using GitHub Actions that automatically
runs code quality checks and unit tests on every push to the main branch.
The pipeline covers two core stages: static code analysis with flake8 and
automated testing with coverage reporting using pytest-cov.

The source module lives in src/calculator.py and replaces the original generic
arithmetic functions with supply-chain calculations for drug shortage duration
forecasting, which is the domain context for the PharmTrack Sentinel project.

## Changes Made to the Lab

Two categories of changes were made: changes to the source logic and changes
to the CI/CD pipeline itself.

**Source logic (src/calculator.py)**

All four functions were replaced with domain-specific supply-chain calculations.
fun1 computes safety stock as daily usage multiplied by lead time in days.
fun2 computes surplus inventory by subtracting safety stock from current stock
on hand, which can return a negative value when stock falls below the safety
threshold. fun3 computes total units needed over a forecast horizon, such as
a D50 or D80 shortage duration window. fun4 produces a composite urgency score
by summing the three values above, which can be used to prioritize which drug
shortages require immediate action.

**CI/CD pipeline (pytest_action.yml)**

Two new stages were added that directly modify how the pipeline operates.

The first new stage runs flake8 across the src/ and test/ directories before
any tests execute. This enforces a consistent code style and catches syntax
issues early in the pipeline. The max-line-length is set to 100 and E203/W503
are ignored to allow standard Python formatting. If flake8 finds any violation,
the pipeline stops immediately and does not proceed to the test stage.

The second new stage runs pytest with coverage flags using pytest-cov. It
produces a JUnit XML report for GitHub to parse and a line-by-line XML coverage
report showing which lines of src/calculator.py were exercised by the tests.
Both files are uploaded as GitHub Actions artifacts so they are available for
download after each run. This makes the pipeline provide measurable evidence
of test quality, not just a pass/fail signal.

## Prerequisites

The following must be available on your machine before running locally.

Python 3.14 or later. Download from https://www.python.org/downloads and
verify with: python3 --version

Git. Download from https://git-scm.com and verify with: git --version

## Environment Setup

Clone the repository and navigate into it.

```
git clone https://github.com/lequo-neu/IE7374-Github-Lab1.git
cd IE7374-Github-Lab1
```

Create and activate a virtual environment.

```
python3 -m venv lab_01
source lab_01/bin/activate
```

Install all dependencies. The versions that matter are pytest 8.x,
pytest-cov 5.x, and flake8 7.x. These will be pulled automatically from PyPI.

```
pip install -r requirements.txt
```

Verify the installations before running anything.

```
pytest --version
flake8 --version
```

## Running the Code Locally

Run the linter first. No output means no violations.

```
flake8 src/ test/ --max-line-length=100 --ignore=E203,W503
```

Run pytest with coverage.

```
pytest test/test_pytest.py --cov=src --cov-report=term-missing -v
```

Run the unittest suite separately.

```
python -m unittest test.test_unittest -v
```

## What a Successful Run Looks Like

After running flake8, you should see no output at all and the terminal should
return to the prompt immediately. Any printed output means there is a violation
that must be fixed before the pipeline will pass.

After running pytest, you should see output similar to this.

```
test/test_pytest.py::test_fun1 PASSED
test/test_pytest.py::test_fun2 PASSED
test/test_pytest.py::test_fun3 PASSED
test/test_pytest.py::test_fun4 PASSED

Name                 Stmts   Miss  Cover   Missing
src/calculator.py       16      0   100%

4 passed in 0.XXs
```

After running unittest, you should see this.

```
test_fun1 ... ok
test_fun2 ... ok
test_fun3 ... ok
test_fun4 ... ok

Ran 4 tests in 0.000s
OK
```

On GitHub, after any push to main, navigate to the Actions tab. Both the
"Testing with Pytest" and "Python Unittests" workflows should show a green
checkmark. Inside the pytest workflow run, expand the "Run tests with coverage"
step to see the coverage table inline. The Artifacts section at the bottom of
the run page will contain pytest-report.xml and coverage.xml available for
download.

## Project Structure

```
IE7374-Github-Lab1/
    .github/
        workflows/
            pytest_action.yml
            unittest_action.yml
    src/
        __init__.py
        calculator.py
    test/
        __init__.py
        test_pytest.py
        test_unittest.py
    .gitignore
    README.md
    requirements.txt
```

## CI/CD Pipeline Summary

The pytest_action.yml workflow triggers on every push and pull request to main.
It sets up Python 3.14, installs dependencies, runs flake8 for linting, runs
pytest with coverage and generates both a JUnit XML report and a coverage XML
report, then uploads both as artifacts.

The unittest_action.yml workflow triggers on every push to main and runs the
standard library unittest suite as a second independent verification layer.
