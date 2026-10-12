# AgriDrought Maroc

A data pipeline that estimates short-term drought risk for 10 Moroccan regions. Every day it pulls recent rainfall, compares it with the historical norm for the same calendar window, and publishes a drought risk score per region.

The project covers the full path from code to deployment: a tested Python pipeline, Azure storage, infrastructure as code, and automated CI/CD and scheduling.

## What it does

For each region, the pipeline computes:

```
drought_risk_pct = (historical_avg_mm - current_mm) / historical_avg_mm * 100
```

- **Positive** means drier than normal (100 = no rain at all).
- **Negative** means wetter than normal.

Regions: Agadir, Marrakech, Casablanca, Tanger, Rabat, Fes, Ouarzazate, Tiznit, Taroudant, Errachidia.

Example output:

```
agadir: 100.0% below normal (0.0mm vs 2.02mm avg)
tanger: 44.8% below normal (5.5mm vs 9.96mm avg)
fes: 97.3% above normal (13.3mm vs 6.74mm avg)
```

## Architecture

```
Open-Meteo archive API
        |
        v
  ingest.py  ------>  bronze/   raw API responses, one file per day
                         |
                         v
                    compute.py  ------>  gold/   drought_index_<date>.json
                                            |
                                            v
                                        report.py   ranked regions
```

- **Bronze** holds the raw API responses, never overwritten:
  - `openmeteo/current/<date>.json`: the last 14 days of daily rainfall, ending 5 days before the run (the archive API lags real time).
  - `openmeteo/baseline/daily_2021_2025.json`: full daily rainfall for 2021-2025, fetched once and reused.
- **Gold** holds the computed index, one dated file per run, so history accumulates.
- The baseline average takes the same calendar window in each past year and skips any year with missing days, so a gap can never silently lower the average.

## Repository layout

```
regions.py            region names and coordinates
fetch.py              Open-Meteo requests (timeout, retry with backoff)
transform.py          rainfall totals, baseline average, risk score
storage.py            Azure Blob Storage helpers
ingest.py             extract + load into bronze
compute.py            bronze -> gold
report.py             prints regions ranked by drought risk
test_api.py           unit tests
requirements.txt      Python dependencies
infra/main.tf         Terraform configuration
.github/workflows/    ci.yml, cd.yml, ingest.yml
```

## Infrastructure (Terraform)

Defined in `infra/main.tf` and deployed to Azure (Spain Central):

- Resource group `rg-agridrought`
- Storage account `stagridrought` (Standard, LRS) with `bronze` and `gold` containers
- Remote state in a separate storage account (`rg-tfstate` / `sttfstateagridrought` / `tfstate`), so a local machine and GitHub Actions share the same state and lock it during runs

## CI/CD and scheduling (GitHub Actions)

| Workflow | Trigger | What it does |
|---|---|---|
| `ci.yml` | push / pull request to `main` | Installs dependencies and runs the tests |
| `cd.yml` | push to `main` | Runs `terraform apply` against Azure |
| `ingest.yml` | daily at 00:00 UTC, or manual | Runs `ingest.py` then `compute.py` |

Authentication from GitHub to Azure uses **OIDC federation**: a federated credential trusts runs from this repository's `main` branch, so no Azure password is stored anywhere. The pipeline's storage connection string is kept as the GitHub secret `AZURE_STORAGE_CONNECTION_STRING`.

## Tests

`pytest test_api.py -v` runs 5 tests:

- the fetch function against a mocked API response
- the rainfall totals per region
- the baseline average: normal case, a year with missing days being skipped, and an error when no usable data exists

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (it is gitignored):

```
AZURE_STORAGE_CONNECTION_STRING=<full connection string from the Azure Portal>
```

Then:

```bash
python3 ingest.py && python3 compute.py && python3 report.py
```

The first `ingest.py` run also builds the 2021-2025 baseline, which takes a minute or two. Later runs only fetch the current window.

To deploy the infrastructure: `az login --use-device-code`, then `cd infra && terraform init && terraform plan`.

## Limitations and next steps

- A percentage deficit is unstable for very dry regions, where a small average makes the score swing widely. A standardized index (such as SPI) would be more robust.
- Rainfall is the only signal so far. Soil moisture, temperature and reservoir levels would make the index more meaningful.
- Results are stored as dated JSON files. A database or warehouse layer would allow queries across days.
- Scheduled GitHub workflows are paused after 60 days without repository activity.

## Tech stack

Python, requests, azure-storage-blob, pytest, Terraform, Azure Blob Storage, GitHub Actions.
