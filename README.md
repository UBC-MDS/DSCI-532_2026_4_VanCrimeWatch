# VanCrimeWatch Dashboard Project

VanCrimeWatch is an interactive dashboard, providing a geospatial analysis of crime hotspots across different neighborhoods in Vancouver. Its goal is focused on assisting new business owners visualize which areas are more prone to specific types of crimes, enabling them to make adequate risk assessments when deciding where to open their businesses. They will be able to use this tool to make comparisons across neighborhoods, filter by crime types and also observe crime patterns from the last 3 years (2023-2025), to make more informed, business decisions. More generally, this dashboard acts as a tool serving anyone interested in understanding local crime patterns. Using Python and Shiny, the dashboard effectively communicates data-driven insights on complex crime patterns in the Vancouver area.

## Set up & Run Dashboard App

**1) First, clone the repository:**

```bash
git clone https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch.git
cd DSCI_532_2026_4_VanCrimeWatch
```

**2) To ensure you can run the dashboard locally, activate the conda environment:**

```bash
conda env create -f environment.yml
conda activate vancrimewatch
```

**3) Run the Dashboard app with the following:**

```bash
shiny run src/app.py --reload
```

**4) Access the dashboard through the link displayed in your terminal:**

```bash
http://127.0.0.1:8000
```

## Dataset

The dataset used is pulled from publicly available data from [Vancouver Police Department](https://geodash.vpd.ca/opendata/).

## Contributors

- Sarisha Dash
- Jennifer Tsang
- Prabuddha Tamhane
- Nour Shawky
