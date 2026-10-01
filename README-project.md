# SpecFinder India

A student prototype for finding and comparing laptops by exact hardware requirements. The initial release focuses on laptops; PC components can be added later.

## Features

- Filter by laptop type, brand, GPU, processor family, minimum RAM, minimum storage, and maximum price.
- Sort matching laptops by price, RAM, storage, or rating.
- View a comparison table and a price chart.

## Run on macOS

From this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-project.txt
streamlit run app.py
```

## Dataset

Download the public India-focused laptop dataset from [abhinavflac/laptops-specs-dataset](https://github.com/abhinavflac/laptops-specs-dataset) and place `laptops_cleaned.csv` at `data/processed/laptops_cleaned.csv`.

The included dataset source folder is kept out of Git by `.gitignore`. Preserve the original data and attribution. The source README describes the dataset as CC0, while the repository's `LICENSE` file says MIT; check with the author if you need to redistribute the dataset itself.

## Known limitations

- Dataset contains 992 listings from the source's December 2025 India collection, not a complete catalogue of every laptop or PC part.
- The CSV has no store name or product-page URL. The app compares listed prices from the dataset and does not show live cross-store offers.
- RTX 3070 Ti is not present in the included gaming laptop rows. Select a GPU available in the filter for the demo.
- Ratings are shown as the source's 0–100 score.

## Project area for evaluation

Web Scraping / data analysis. The dataset source reports collecting product listings from Indian e-commerce websites. This student prototype focuses on cleaning structured fields and building a useful specification search interface.
