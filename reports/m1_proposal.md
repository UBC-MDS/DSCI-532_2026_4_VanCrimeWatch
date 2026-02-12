## Section 3: Research Questions & Usage Scenarios

### User Story: New Home Buyer

**Persona:**
Steve is a first-time home buyer relocating to Vancouver. He has shortlisted neighbourhoods by transit access and affordability, but safety is a critical factor for his family. He needs a data-driven way to compare crime conditions before committing to a purchase.

**Usage Scenario:**
When Steve logs onto VanCrimeWatch, he filters to the 2023-2025 date range and selects residential-relevant crime categories: *Break and Enter Residential/Other*, *Offence Against a Person*, and *Mischief*. The dashboard shows a neighbourhood-level comparison of crime volume and type breakdown. Steve notices that the Central Business District has high counts driven mostly by *Mischief*, while Dunbar-Southlands shows consistently low numbers. Switching to the year-over-year view, he spots a steady decline in *Break and Enter Residential* in Renfrew-Collingwood, flagging it as a promising area worth investigating.

**User Story:**
> As a **first-time home buyer**, I want to **compare neighbourhood-level crime rates filtered by residential-relevant crime types and time period (2023-2025)**, in order to **identify the safest neighbourhoods for my family and make an informed home purchase decision**.

---

## Section 4: Exploratory Data Analysis

To address the business-owner research question -- *How would new business owners choose between various localities in Vancouver depending on the crime rate and types of crime?* -- we performed an exploratory analysis in [`notebooks/VancouverCrimeAnalysis.ipynb`](../notebooks/VancouverCrimeAnalysis.ipynb).

**Analysis:** We filtered 2023-2025 crime data to five business-relevant types: *Break and Enter Commercial*, *Theft from Vehicle*, *Other Theft*, *Mischief*, and *Theft of Vehicle*. The **Central Business District** has the highest business-crime volume, driven by *Other Theft* and *Theft from Vehicle*, while **Musqueam**, **Shaughnessy**, and **South Cambie** consistently record the fewest incidents. Year-over-year trends are relatively stable across all neighbourhoods.

**Reflection:** These findings support the dashboard's value for prospective business owners by enabling them to identify low-risk areas, compare crime composition, and track whether conditions are improving or worsening over time.
