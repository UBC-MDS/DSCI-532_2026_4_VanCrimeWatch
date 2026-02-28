## App Specification

### 1. Updated Job Stories

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | As a business owner, I want to filter crimes by neighbourhood so that I can identify which areas of the city are statistically safest for a new storefront. | ✅ Implemented  |                               |
| 2   | As a baker working early hours, I want to filter crimes by type (e.g., Commercial B&E) so that I can specifically avoid areas where my business equipment and inventory would be at high risk. | ✅ Implemented     |  |
| 3   | As a visual learner, I want to view crime data on an interactive map so that I can understand the spatial relationship between potential cafe locations and recent criminal activity. | ✅ Implemented  |                        |
| 4   | As a baker operating my business from mornings to evenings, I want to view crime trends by time of day, day of week, and month so that I can identify the safest hours, days, and seasons to operate my storefront. | ✅ Implemented | 

### 2. Component Inventory

| ID            | Type          | Shiny widget / renderer | Depends on                   | Job story  |
| ------------- | ------------- | ----------------------- | ---------------------------- | ---------- |
| `input_neighbourhood`    | Input         | `ui.input_selectize(multiple=True)` | —                                                       |#1 |
| `input_crime_type`       | Input         | `ui.input_selectize(multiple=True)` | —                                                       |#2|
| `input_year`             | Input         | `ui.input_checkbox_group()`         | —                                                       |#3|
| `input_time_agg`         | Input         | `ui.input_radio_buttons()`          | —                                                       |#3|
| `filtered_data`          | Reactive calc | `@reactive.calc`                    | `input_neighbourhood`, `input_crime_type`, `input_year` | #1,#2,#3|
| `output_map`             | Output        | `@render.ui` (leaflet)              | `filtered_data`                                         |#1, #3|
| `output_donut`           | Output        | `@render.plot`                      | `filtered_data`                                         |#2|
| `output_timeline`        | Output        | `@render.plot`                      | `filtered_data`, `input_time_agg`                       |#2|
| `output_kpi_most_common` | Output        | `@render.text`                      | `filtered_data`                                         |#1,#2|
| `output_kpi_safest_area` | Output        | `@render.text`                      | `filtered_data`                                         |#3|

### 3. Reactivity Diagram

```mermaid
flowchart TD

NS[/input_neighbourhood/]
CS[/input_crime/]
TS[/input_year/]
TD[/input_time_agg/]

RDF{{filtered_data}}

NS --> RDF
CS --> RDF
TS --> RDF

MAP([output_map])
DONUT([output_donut])
TIMELINE([output_timeline])
KPI([KPIs])

RDF --> MAP
RDF --> DONUT
RDF --> TIMELINE
RDF --> KPI
TD --> TIMELINE
```

### 4. Calculation Details

We have one `@reactive.calc` in our workflow `filtered_data` which controls all of our charts display. It is the common dataframe, of which we show different views to the user.

Depends on:
- Input Year (`input_year : list[str]`): 
    - List of selected years (Checkboxes)
    - The user can select one, two or three years as checkboxes and the dataframe will be filtered accordingly. Thus only the selected years will be displayed across all charts. 
    - Range from 2023-2025
    - default: all
- Input Neighbourhoods (`input_neighbourhood: list[str]`): list of selected neighbourhoods
    - List of selected Neighbourhoods (Multiple Select Dropdown)
    - The user can select one or more neighbourhoods and the dataframe will be filtered accordingly. Thus only the selected neighbourhoods will be displayed across all charts. 
    - Eg. Fairview, Oakridge.
    - default: all
- Input Crime Types (`input_crime : list[str]`): list of selected crime types
    - List of selected crime types (Multiple Select Dropdown)
    - The user can select one or more crime types and the dataframe will be filtered accordingly. Thus only the selected types will be displayed across all charts. 
    - Eg. Break and Enter Commercial, Theft of Vehicle
    - default: all

Outputs Affected:
- Map `output_map`
    - Shows circles for aggregated total crime (shown using size of circle) in each neighbourhood from `filtered_data`. 
    - Only displays the selected neighbourhoods, crime types and year according to `filtered_df` calculation
- Donut `output_donut`   
    - Distribution of crime for crime type from `filtered_data` after filtration.
- Timeline `output_timeline`
    - Line chart
    - Aggregated crimes for selected years from `filtered_data`: can show data from one, two or three years.
- KPIs: 
    - `output_kpi_most_common` - Display most common crime type from `filtered_data`
    - `output_kpi_safest_area` - Safest neighbourhood displays least total crime from `filtered_data`

> Note: (Not a responsive calc but affects the output display for one chart) The aggregation in `output_timeline` is based on `input_time_agg : str`. Eg. Selecting Weekly aggregation will aggregate ALL Mondays in 2023, ALL Tuesdays in 2023 etc. and give one value
---

### 5. Complexity Enhancement: Reset Filters Button

We implemented a Reset Filters button in the sidebar using `@reactive.effect` and `@reactive.event(input.reset_btn)`. Since our dashboard has 4 separate input components (neighbourhood selector, crime type selector, year checkboxes, and timeline aggregation), users who have applied multiple filters would otherwise need to manually deselect and reselect each widget individually to return to the default view.

The reset button restores all inputs to their defaults in a single click:

- Neighbourhood: all neighbourhoods (empty selection = displaying all)
- Crime Type: all crime types (empty selection = displaying all)
- Year: 2023, 2024, 2025 all selected
- Aggregate By: Monthly

The reset only triggers on button click and functions to programmatically restore each widget to its default value.