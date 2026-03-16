import duckdb

CSV = "data/processed/combined_crime_data_2023_2025.csv"
OUT = "data/processed/combined_crime_data_2023_2025.parquet"

duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV}'))
    TO '{OUT}' (FORMAT PARQUET)
""")

print("Done!")