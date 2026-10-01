# Partschecker — SpecFinder India

A Python and Streamlit prototype for finding Indian laptops by exact hardware specifications and comparing their listed prices. The first version focuses on laptops; PC components can be added later.

## Run on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-project.txt
streamlit run app.py
```

Place `laptops_cleaned.csv` at `data/processed/laptops_cleaned.csv` before launching.

## Data source and limits

The project uses the [public Indian laptop specifications dataset](https://github.com/abhinavflac/laptops-specs-dataset). The dataset has specs and prices but no retailer names or product URLs, so this prototype cannot provide live cross-store offers. The included sample has no RTX 3070 Ti listings.

Dataset files are not included in this repository. Download the CSV from the source above.
