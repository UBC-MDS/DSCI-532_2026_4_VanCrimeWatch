# VanCrimeWatch Dashboard

> Interactive geospatial dashboard for visualizing crime patterns across Vancouver neighbourhoods.

[**Live App (Stable)**](https://jentsang-vancrimewatch.share.connect.posit.cloud/) | [**Preview (Dev)**](https://jentsang-vancrimewatch-dev.share.connect.posit.cloud/)


## Motivation

Choosing a location for a new business requires understanding local safety conditions. VanCrimeWatch helps new business owners and community members visualize which areas in Vancouver are more prone to specific types of crimes, enabling informed risk assessments for business placement decisions.

Using publicly available data from the Vancouver Police Department (2023--2025), the dashboard provides:

- **Interactive Map** -- Geospatial view of crime hotspots across Vancouver neighbourhoods.
- **Crime Timeline** -- Monthly, weekly, and hourly trend analysis with per-year comparisons.
- **Crime Type Breakdown** -- Distribution of crime categories across selected filters.
- **Neighbourhood & Crime Type Filters** -- Drill down into specific areas and offence types.
- **Year Selection** -- Compare crime patterns across 2023, 2024, and 2025.


## Demo

![Dashboard Demo](img/m3_demo.gif)

## Using the AI explorer

The AI Explorer tab allows you to query the Vancouver crime dataset using plain English. Instead of manually adjusting filters, you can choose that tab and instead type questions like:

### Example: How a prospective business owner might use the AI Explorer tab

Say you are considering opening a bakery and want to compare crime activity across a few Vancouver neighbourhoods. Initially, you know that the bakeries are popular in the downtown area. Here is how you might use the AI Explorer to guide your decision:

1. **Start broad** — ask *"Show me the crime density in downtown area in 2025"* to get an overview of crime types in your area of interest. The map will pan to the area of interest, the donut chart will update to show the distribution of crime types from that area, and the timeline will update to reflect crime patterns within that neighborhood from the year 2025.
2. **Narrow down and start comparing** — follow up with *"Show me theft from vehicle and break and enter commercial in Kitsilano and West End in 2024 and 2025"* to compare business-relevant crime types across neighbourhoods side by side.
3. **Download the data** — once you have a filtered view, click **Download Filtered CSV** to save the results for your own analysis.

### Tips for querying

- Use filter-style queries to update the dashboard outputs: *"Show me [crime type] in [neighbourhood] in [year]"*
- The AI understands informal names — "downtown" maps to "Central Business District", "vandalism" maps to "Mischief", and "car theft" maps to "Theft of Vehicle"
- For queries like *"Which neighbourhood has the most theft?"*, the result will appear only as text in the chat
- If your query returns no matching records (e.g. *"Show me homicides in Kitsilano in 2025"*), the charts will display a message indicating no data was found for that combination

> **Note:** The AI may still misinterpret queries, depending on the language used. This is a work in progress features that we hope to update with more detailed instructions. You can also use the main **Dashboard** tab to extract extract neighborhood names, crime types and years available.

## Installation & Local Development

### 1. Clone the repository

```bash
git clone https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch.git
cd DSCI_532_2026_4_VanCrimeWatch
```

### 2. Create and activate the conda environment

```bash
conda env create -f environment.yml
conda activate vancrimewatch
```

### 3. Set up your Anthropic API key

The AI Explorer tab requires an [Anthropic](https://console.anthropic.com) API key. Make sure to set one up if you wish to use the querychat tool locally.

Create a `.env` file in the root of the repository:
```bash
touch .env
```

Add your API key to the file:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Set up your MongoDB URI

The Chat History tab requires a [MongoDB Cloud](https://cloud.mongodb.com/) Cluster and URI key to connect pymongo to a mongodb cloud cluster. Make sure to set one up if you wish to use the history tool locally.

Once you have set up a cluster, and the `.env` file is created in the above step:

Add your API key to the `.env` file:
```
PYMONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/?appName=<cluster>
```

### 5. Run the dashboard

```bash
shiny run src/app.py --reload
```

### 6. Open in your browser

```
http://127.0.0.1:8000
```

## Testing

This dashboard includes both unit tests (Pytest) for the core data-filtering logic and Playwright UI tests for the dashboard interface. 

To run the entire test suite locally:

1. Ensure your conda environment is activated 
```bash
conda activate vancrimewatch
```

2. Ensure the Playwright browsers are installed 
```bash
playwright install
```

To run all tests from the root directory:
```bash
pytest tests/
```

## Contributing

Interested in contributing? Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started, our code of conduct, and the process for submitting pull requests.

## Dataset

The dataset is sourced from publicly available data provided by the [Vancouver Police Department](https://geodash.vpd.ca/opendata/), covering crime incidents from 2023 to 2025.

## License

Licensed under the terms of the [MIT License](LICENSE).

## Contributors

- Sarisha Das
- Jennifer Tsang
- Prabuddha Tamhane
- Nour Shawky
