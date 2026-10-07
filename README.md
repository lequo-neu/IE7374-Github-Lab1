# IE7374 Lab 1 — GitHub Actions CI/CD Pipeline

## Overview

This lab implements a CI/CD pipeline using GitHub Actions that automatically
runs a four-stage quality gate on every push to the main branch: a dependency
security audit, static code analysis, automated testing with coverage reporting,
and artifact upload. Every stage must pass before the next one starts, which
means a pull request carrying a known vulnerability or a failing test can never
reach the repository without being flagged first.

The source module lives in src/calculator.py and replaces the original generic
arithmetic functions with supply-chain calculations for drug shortage duration
forecasting, which is the domain context for the PharmTrack Sentinel project.

## Changes Made to the Lab

**Source logic (src/calculator.py)**

All four functions were replaced with domain-specific supply-chain calculations.
fun1 computes safety stock as daily usage multiplied by lead time in days.
fun2 computes surplus inventory by subtracting safety stock from current stock
on hand, which returns a negative value when stock falls below the safety
threshold. fun3 computes total units needed over a forecast horizon, such as
a D50 or D80 shortage duration window. fun4 produces a composite urgency score
by summing the three values above.

**CI/CD pipeline (pytest_action.yml)**

Two stages were added that directly modify pipeline behavior.

The first new stage runs flake8 across the src/ and test/ directories. This
enforces a consistent code style and catches syntax issues early. If flake8
finds any violation, the pipeline stops and does not proceed to testing.

The second new stage runs pytest with coverage flags using pytest-cov, producing
a JUnit XML report and a line-by-line coverage XML report. Both files are
uploaded as GitHub Actions artifacts so they are available for download after
each run.

## Advanced Extension — Automated Dependency Security Audit

**Why this was chosen**

A CI/CD pipeline that only tests functionality gives a false sense of safety.
Code can pass every test and still ship a critical vulnerability if one of its
dependencies has a known exploit. In real-world ML engineering, models and
pipelines often rely on scientific libraries with complex dependency trees, and
a single outdated package can expose the entire system. Integrating security
scanning directly into the pipeline forces the team to confront vulnerabilities
at the moment they are introduced, rather than discovering them months later in
a security review.

Pip-audit was chosen specifically because it is the official tool recommended
by the Python Packaging Authority (PyPA) for this purpose. It queries two
authoritative databases: the Python Vulnerability Database (PyVD), which is
maintained by the Python security team, and the GitHub Advisory Database, which
tracks CVEs across the broader open source ecosystem. Unlike manual dependency
reviews, pip-audit runs in under five seconds and produces a machine-readable
report that integrates cleanly into a GitHub Actions step.

**How it works**

The audit step runs immediately after pip install and before any code analysis.
This ordering is intentional: there is no point linting or testing code if the
environment it runs in is already compromised. The command scans every package
listed in requirements.txt, resolves their transitive dependencies, and checks
each resolved version against the vulnerability databases.

If a vulnerability is found, pip-audit prints a table with four columns: the
package name, the installed version, the CVE or advisory identifier, and the
version that fixes the issue. The pipeline exits with a non-zero status code,
which causes GitHub Actions to mark the run as failed and block any subsequent
steps from executing. The fix is either to upgrade the affected package to the
recommended version or, in rare cases where no fix exists yet, to explicitly
accept the finding with a documented justification.

If no vulnerabilities are found, the output is a clean table with a No
vulnerabilities found message and the pipeline continues normally.

**What it produces**

Every pipeline run now produces an implicit security certificate: if the run
passed, the dependencies were clean at that point in time. This gives reviewers
and future team members confidence that the codebase was not knowingly shipping
with exploitable packages. In a team setting, this also removes the burden of
manual dependency reviews from code reviews entirely.

## Prerequisites

The following must be available on your machine before running locally.

Python 3.14 or later. Download from https://www.python.org/downloads and
verify with: python3 --version

Git. Download from https://git-scm.com and verify with: git --version

## Environment Setup

Clone the repository.

```
git clone https://github.com/lequo-neu/IE7374-Github-Lab1.git
cd IE7374-Github-Lab1
```

Create and activate a virtual environment.

```
python3 -m venv lab_01
source lab_01/bin/activate
```

Install all dependencies including pip-audit, pytest-cov, and flake8.

```
pip install -r requirements.txt
```

## Running the Code Locally

Run the security audit first to check for known CVEs in your installed packages.

```
pip-audit -r requirements.txt --format=columns
```

No output means no known vulnerabilities. A table output means vulnerabilities
were found and must be addressed before the pipeline will pass.

Run the linter to check code style.

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

After running pip-audit, you will see one of two things. If all packages are
clean, the output will be a table with a No vulnerabilities found message. If
a vulnerability exists, you will see the package name, the CVE or advisory ID,
the installed version, and the recommended fix version. The pipeline fails in
that case until the package is upgraded or the finding is explicitly accepted.

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

On GitHub, the Actions tab will show the pipeline running through four named
stages: Audit dependencies, Lint with flake8, Run tests with coverage, and
Upload test and coverage results. The Artifacts section at the bottom of each
run contains pytest-report.xml and coverage.xml available for download.

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
It sets up Python 3.14, installs dependencies, runs pip-audit to scan for
known CVEs, runs flake8 for linting, runs pytest with coverage and uploads
both a JUnit XML report and a coverage XML report as artifacts.

The unittest_action.yml workflow triggers on every push to main and runs the
standard library unittest suite as a second independent verification layer.
