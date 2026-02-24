"""
Combine and clean Vancouver crime data CSVs for 2023-2025.

Replicates the data loading and cleaning logic from the EDA notebook
(notebooks/VancouverCrimeAnalysis.ipynb) and outputs a single cleaned CSV.

Usage:
    python scripts/combine_csv.py
"""

import os
import pandas as pd


def main():
    # --- Paths -----------------------------------------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    output_path = os.path.join(processed_dir, "combined_crime_data_2023_2025.csv")

    # --- 1. Load CSVs for 2023-2025 --------------------------------------
    years = [2023, 2024, 2025]
    dfs = []
    for year in years:
        path = os.path.join(raw_dir, f"crimedata_csv_AllNeighbourhoods_{year}.csv")
        df_year = pd.read_csv(path)
        dfs.append(df_year)
        print(f"Loaded {year}: {df_year.shape[0]:,} rows")

    df = pd.concat(dfs, ignore_index=True)
    print(f"\nCombined dataset: {df.shape[0]:,} rows, {df.shape[1]} columns")

    # --- 2. Data Cleaning -------------------------------------------------
    missing_neighbourhood = df["NEIGHBOURHOOD"].isna().sum()
    empty_neighbourhood = (df["NEIGHBOURHOOD"] == "").sum()
    print(f"\nMissing NEIGHBOURHOOD values: {missing_neighbourhood}")
    print(f"Empty-string NEIGHBOURHOOD values: {empty_neighbourhood}")

    df = df[df["NEIGHBOURHOOD"].notna() & (df["NEIGHBOURHOOD"] != "")].copy()
    print(f"After cleaning: {df.shape[0]:,} rows")

    # --- 3. Create DATE column --------------------------------------------
    df["DATE"] = pd.to_datetime(
        df[["YEAR", "MONTH", "DAY"]].rename(
            columns={"YEAR": "year", "MONTH": "month", "DAY": "day"}
        ),
        errors="coerce",
    )
    print(f"Date range: {df['DATE'].min()} to {df['DATE'].max()}")

    # --- 4. Summary -------------------------------------------------------
    print(f"\nYears present: {sorted(df['YEAR'].unique())}")
    print(f"Neighbourhoods: {df['NEIGHBOURHOOD'].nunique()}")
    print("\nCrime types:")
    for ct in sorted(df["TYPE"].unique()):
        print(f"  - {ct}")

    # --- 5. Save ----------------------------------------------------------
    df.to_csv(output_path, index=False)
    print(f"\nSaved combined CSV to: {output_path}")
    print(f"Final shape: {df.shape[0]:,} rows, {df.shape[1]} columns")


if __name__ == "__main__":
    main()
