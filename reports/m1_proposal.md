## Motivation and Purpose 

**Our role:** Data Analysts at the Vancouver Police Department

**Target Audience:** Prospective business owners and entrepreneurs who are hoping to open a business in the Vancouver area.

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

### User Story: New Business Owner

**Persona:**
Jennie is an independent baker planning to open her first small cafe in Vancouver. As a first-time business owner, she prioritizes the safety of her staff and customers. She needs to identify which neighbourhoods have lower rates of property crime so she can choose a location that minimizes the risk of break-ins and ensures a welcoming environment for her customers.

**Usage Scenario:**
When Jennie logs into the VanCrimeWatch app, she is presented with a high-level spatial overview of criminal activity across Vancouver. Wanting to protect her physical storefront, she uses the "Crime Type" filter to specifically highlight "Break and Enter Commercial" incidents over the past three years.

As she explores the interactive map, she notices a high density of markers in the Downtown Eastside but observes a surprising "pocket of safety" in a specific area of Mount Pleasant she hadn't considered before. By toggling the neighbourhood view, she compares the frequency of nighttime versus daytime crimes to see if her early-morning baking shifts would be safe.

Based on these insights, Jennie decides to narrow her real estate search to Mount Pleasant, feeling confident that she can justify a slightly higher rent in exchange for the lower crime rates she visualized in the app.

**User Stories:**

> User Story 1: As a **business owner**, I want to **filter crimes by neighbourhood** so that I can **identify which areas of the city are statistically safest for a new storefront**.

> User Story 2: As a **baker working early hours**, I want to **filter crimes by type (e.g., Commercial B&E)** so that I can **specifically avoid areas where my business equipment and inventory would be at high risk**.

> User Story 3: As a **visual learner**, I want to **view crime data on an interactive map** so that I can **understand the spatial relationship between potential cafe locations and recent criminal activity**.

---

## Exploratory Data Analysis

To address the business-owner research question -- *How would new business owners choose between various localities in Vancouver depending on the crime rate and types of crime?* -- we performed an exploratory analysis in [`notebooks/VancouverCrimeAnalysis.ipynb`](../notebooks/VancouverCrimeAnalysis.ipynb).

**Analysis:** We filtered 2023-2025 crime data to five business-relevant types: *Break and Enter Commercial*, *Theft from Vehicle*, *Other Theft*, *Mischief*, and *Theft of Vehicle*. The **Central Business District** has the highest business-crime volume, driven by *Other Theft* and *Theft from Vehicle*, while **Musqueam**, **Shaughnessy**, and **South Cambie** consistently record the fewest incidents. Year-over-year trends are relatively stable across all neighbourhoods. Bucketing by time of day reveals that the **Afternoon (12-17h)** and **Evening (18-23h)** periods see the most business-related crime, and aggregating by month shows a **seasonal uptick during warmer months (May-October)**.

**Reflection:** These findings support the dashboard's value for prospective business owners by enabling them to identify low-risk areas, compare crime composition, examine temporal patterns, and track whether conditions are improving or worsening over time.

## App Sketch & Description

![Dashboard Sketch](../img/sketch.png)

### Sidebar (Filters) and Chart Description:
| **Filter Category**  | **Functionality** |
|--|--|
| **Neighbourhood** | - Select one or more neighbourhoods (dropdown with "Select All" option) <br> - Selected neighbourhoods displayed as tags |
| **Timeline** | - Select time range (e.g., last week, last month, last year) <br> - Select display frequency (daily, weekly, monthly) |
| **Crime Type** | - Dropdown to select specific crime type or category <br> - Can also filter via interactive chart |



| Chart| Description |
|--|--|
| **Map** | - Interactive map of Vancouver with crime statistics visualized using circles <br> - Option to display exact crime locations <br> - Updates dynamically based on selected filters |
| **Bar / Donut Chart** | - Interactive chart displaying crime counts <br> - Updates based on selected neighbourhoods, timeline, and crime type |
| **Timeline** | - Visualizes crime trends over selected time range, neighbourhoods, and crime types <br> - Displays exact numerical values for trend data |

KPIs: 
- Number and percentage of crime-specific incidents and comparison to total
- Trend percent increase/decrease
