from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "processed" / "laptops_cleaned.csv"

st.set_page_config(page_title="SpecFinder India", page_icon="💻", layout="wide")
st.title("💻 SpecFinder India")
st.caption("Find laptops by the specifications that matter to you.")

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["price", "ram_gb", "storage_gb", "gpu_vram_gb", "display_size_inch"]:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

if not DATA_PATH.exists():
    st.error(f"Dataset not found at {DATA_PATH}. Download the project dataset and place it in data/processed/.")
    st.stop()

df = load_data(DATA_PATH)

with st.sidebar:
    st.header("Find your laptop")
    categories = sorted(df["device_category"].dropna().unique())
    category = st.selectbox("Type", ["Any"] + categories)
    brands = sorted(df["brand"].dropna().astype(str).str.title().unique())
    brand = st.selectbox("Brand", ["Any"] + brands)
    gpu_models = sorted(df["gpu_model"].dropna().astype(str).unique())
    gpu = st.selectbox("Graphics (GPU)", ["Any"] + gpu_models)
    cpu_series = sorted(df["cpu_series"].dropna().astype(str).unique())
    cpu = st.selectbox("Processor family", ["Any"] + cpu_series)
    min_ram = st.selectbox("Minimum RAM", [0, 8, 16, 32, 64], index=0, format_func=lambda v: "Any" if v == 0 else f"{v} GB")
    min_storage = st.selectbox("Minimum storage", [0, 256, 512, 1024, 2048], index=0, format_func=lambda v: "Any" if v == 0 else (f"{v // 1024} TB" if v >= 1024 else f"{v} GB"))
    max_price = st.number_input("Maximum price (₹)", min_value=0, max_value=1_000_000, value=200_000, step=10_000)
    query = st.text_input("Model name contains", placeholder="e.g. Legion, Victus")
    sort_by = st.selectbox("Sort results", ["Lowest price", "Highest RAM", "Largest storage", "Highest rating"])

results = df.copy()
if category != "Any":
    results = results[results["device_category"] == category]
if brand != "Any":
    results = results[results["brand"].astype(str).str.casefold() == brand.casefold()]
if gpu != "Any":
    results = results[results["gpu_model"].astype(str) == gpu]
if cpu != "Any":
    results = results[results["cpu_series"].astype(str) == cpu]
if min_ram:
    results = results[results["ram_gb"] >= min_ram]
if min_storage:
    results = results[results["storage_gb"] >= min_storage]
if max_price:
    results = results[results["price"] <= max_price]
if query.strip():
    results = results[results["model"].astype(str).str.contains(query.strip(), case=False, na=False)]

sort_map = {
    "Lowest price": ("price", True),
    "Highest RAM": ("ram_gb", False),
    "Largest storage": ("storage_gb", False),
    "Highest rating": ("rating", False),
}
column, ascending = sort_map[sort_by]
results = results.sort_values(column, ascending=ascending, na_position="last")

m1, m2, m3 = st.columns(3)
m1.metric("Matching laptops", f"{len(results):,}")
m2.metric("Lowest listed price", f"₹{results['price'].min():,.0f}" if not results.empty else "—")
m3.metric("Highest listed price", f"₹{results['price'].max():,.0f}" if not results.empty else "—")

st.subheader("Matching laptops")
if results.empty:
    st.info("No laptops match all these filters. Try widening your budget or relaxing one specification.")
else:
    show_cols = ["brand", "model", "price", "cpu_series", "cpu_model", "gpu_model", "gpu_vram_gb", "ram_gb", "storage_gb", "display_size_inch", "rating"]
    show_cols = [c for c in show_cols if c in results.columns]
    display = results[show_cols].rename(columns={
        "brand": "Brand", "model": "Model", "price": "Price (₹)", "cpu_series": "CPU", "cpu_model": "CPU model",
        "gpu_model": "GPU", "gpu_vram_gb": "GPU VRAM (GB)", "ram_gb": "RAM (GB)", "storage_gb": "Storage (GB)",
        "display_size_inch": "Screen (in)", "rating": "Rating (0–100)"
    })
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.bar_chart(results.head(15).set_index("model")["price"], y_label="Price (₹)")

with st.expander("About this dataset and its limits"):
    st.write("This prototype uses a public India-focused laptop dataset. Its CSV has specifications and listed prices, but no retailer names or product-page URLs. Prices therefore compare dataset records, not live offers across stores. The current data also has no RTX 3070 Ti entries; choose a GPU that appears in the filter list for your demo.")
    st.markdown("Dataset source: [abhinavflac/laptops-specs-dataset](https://github.com/abhinavflac/laptops-specs-dataset)")
