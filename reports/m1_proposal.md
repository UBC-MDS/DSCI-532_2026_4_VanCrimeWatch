## Motivation and Purpose 

Our role: Data Analysts at the Vancouver Police Department
Target Audience: Prospective business owners and entrepreneurs who are hoping to open a business in the Vancouver area.

The process of opening a business involves many important decision making steps, with choice of location being a major one. Understanding neighborhood activity is critical not only for identifying whether the business will attract their target customer demographic, but also, to determine the safety risks that could impact employees, customers and business operations. To do this, business owners often have to conduct risk assessments by sifting through a large dataset of past incident reports, which is very time consuming and resource-intensive. Instead, it becomes much more efficient for them to visualize and examine this information in one place. Therefore, to address this challenge, we propose building an interactive dashboard illustrating crime patterns across Vancouver neighborhoods. The dashboard will show the city's crime hotspots, alongside informative temporal trends of crime activity from the past 3 years (2023-2025). In addition to this, business owners will be able to view the distribution of business-relevant crime types through filterable charts, giving them the ability to conduct side by side neighbourhood comparisons on the types of crime they view to be more important than others. This tool will allow them to efficiently account for safety risks specific to their business needs, and make more more informed data-driven location decisions.

## Description of the Data

We will be visualizing a dataset of approximately **100,000** reported crime incidents over the years **2023-2025** in Vancouver, of various types across various geographical locations and times. There are around 33,000 cases reported each year (with 2026 containing the most recent and thus less data). Each record represents a single incident.

Each row has the following:

* **Incident type** (`TYPE`) - the category of crime (e.g., *Break and Enter Commercial*).
* **Time** (`YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`) - the exact date and time the incident is recorded.
* **Location** (`HUNDRED_BLOCK`, `NEIGHBOURHOOD`) - the block-level street location and the associated neighbourhood. Many block locations are censored. 
* **Geographic coordinates** (`X`, `Y`) - spatial coordinates (latitiude and longitude)

The neighbourhood can directly inform the user about the general location of the crime, and paired with latitude-longitudes can be used to locate them on a map. 

The type of crimes can be classified into business-related, individual or other.

Also additional derived variables, such as day of week trends, time-of-day trends, and aggregated counts, can be created created to facilitate trend analysis and comparisons between neighbourhoods.

>**Note:**
>
> The data is taken from the publically available police records management system (PRIME) hosted on the official [Vancouver Police Department website](https://vpd.ca/crime-statistics/) and reflects reported offences at the time of extraction. Due to ongoing investigations and report refinements, the following things should be noted:
> - Some records are reported late, get updated, or reclassified as new information becomes available (e.g., an assault later determined to be a robbery)
> - Statistics may also lag by 2–3 months due to quality control processes.
> - Offense codes can be reclassified
> - Some statistics are reported using the "most serious offence method" and others use the "all violations method.", and thus they are not cross-comparable

## Research Questions & Usage Scenarios







## Exploratory Data Analysis 








## App Sketch & Description

![Dashboard Sketch](../img/sketch.png)

### Sidebar (Filters):

**NEIGHBOURHOOD**
- Select one or more neighbourhoods (select all button + dropdown)
- A list of currently selected neighbourhoods as tags

**TIMELINE**
- Select data to display: last week/last month/last year etc
- Select display type: daily/monthly/weekly

**CRIME TYPE**
dropdown to select crime type or category (also can be done from interactive chart)

### Charts:

**MAP**
- Interactive map of Vancouver with crime statistics visualised through circles
- Optional display exact crime locations
- Changes according to selection 

**BAR/DONUT CHART**
- Crime numbers displayed on interactive chart

**TIMELINE**
- Visualising crime trends over selected options/neighbourhoods/crime types
- Also includes numbers for exact trend values