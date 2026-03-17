# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Upcoming features and fixes

## [0.4.0] - Milestone 4 - 2026-03-17

### Added

- Added logs for LLM output [#89](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/89)
- Added unit tests and Playwright UI tests [#99](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/99)
- Implemented lazy loading via parquet + duckdb [#100](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/100)
- Add analysis notebook for usage of llm logs [#111](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/111/changes)

### Changed

- Updated README with mongo URI instructions [#89](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/89)
- Addressed: Enhance input selection box (non-critical feedback) [#90](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/90) via [#91](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/91)
- Addressed: Year selector component (critical feedback) [#88](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/88) via [#97](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/97) 
- Addressed: Irregular font sizes (non-critical feedback) [#87](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/87) via [#98](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/98)
- Refactored filter data function [#99](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/99)
- Updated README with instructions to run tests [#99](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/99)
- Addressed: Mobile responsiveness (non-critical feedback) [#102](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/102) via [#101](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/101)
- Addressed: Implement meaningful message for missing data (critical feedback) [#92](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/92) via [#103](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/103)
- Addressed: Implement better comparison for areas with least crime vs most crime (non-critical feedback) [#93](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/93) via [#104](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/104)
- Addressed: Add label component for filters (non-critical feedback) [#107](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/107) via [#108](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/108)
- Address: Update readme with better example walkthrough (non-critical feedback) [#96](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/96) via [#110](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/110)
- Updated issue templates [#112](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/112)


### Fixed

- Fixed input selection box for issue [#90](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/90)
- **Feedback prioritization issue link:** [#86](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/86)

### Known Issues

- Due to the sizing on the device, may need to zoom out (ie. 75%) to see the all the feature details on the dashboard. 

### Known Issues

- **Dashboard Scaling:** Depending on the device's screen size and resolution, users may need to zoom out their browser window (e.g., to 75%) to comfortably view all feature details and outputs on the dashboard simultaneously.

### Release Highlight: Persistent LLM Logging

We implemented a backend logging feature using MongoDB to capture user queries and LLM responses from our AI Explorer tab. This tool provides valuable information on how our target users interact with the data. By analyzing these logs, we can identify which neighborhoods, crime types, and timeframes are most frequently searched, while also detecting edge cases where the LLM fails or returns unexpected results. This data directly informs how we refine the LLM's 'extra_instructions' and improve our dashboard components to better serve our audience.

- **Option chosen:** B 
- **PR:** [#89](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/89)
- **Why this option over the others:** We prioritized this logging feature because understanding real user behavior and query patterns is critical for iteratively improving the AI Explorer's accuracy and tailoring the dashboard to our target audience's actual needs.
- **Feature prioritization issue link:** [#94](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/94)

### Collaboration

For this milestone, our team heavily refined our collaboration strategies based on our M3 retrospective to ensure a smoother, more equitable development process. We codified these new norms directly into our `CONTRIBUTING.md` file.

- **CONTRIBUTING.md:** Update via PR [#106](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/106) documenting M3 retrospaective and M4 collaboration norms.
- **M3 retrospective:** 
During our M3 retrospective, we realized that our pull requests had become too large, which made testing, code review, and documentation a little messy. We also acknowledged that the workload was unevenly distributed, with some members taking on disproportionate amounts of coding and documentation. On the positive side, we found that refactoring code into separate files greatly improved our parallel workflow.
- **M4:** 
For Milestone 4, we implemented several new norms to directly address our M3 feedback. We committed to making smaller, single-issue PRs and required them to be reviewed by at least 2 team members within 24 hours. To balance the workload, every team member took responsibility for addressing at least one peer feedback item end-to-end, and distributed the coding and documentation workload evenly. Finally, we mandated that feature specifications must be updated before writing code for documentation.

### Reflection

Our dashboard currently provides a highly tailored and interactive experience for prospective business owners to assess crime risks. It successfully combines geospatial visualizations with a natural language AI query interface and MongoDB backend logging. By setting our default views to highlight business-relevant crimes in the most recent year, we provide users with an immediate, meaningful starting point rather than an overwhelming blank slate.

A current technical limitation involves our database connection management. We temporarily removed the `session.on_ended(con.disconnect)` call to avoid app crashes and closures when multiple users are running the dashboard concurrently. Optimizing this database connection (e.g., implementing proper connection pooling) to handle scale safely is a priority for future enhancements. Additionally, we still need to implement the improvements we considered in Milestone 3, such as creating a static greeting for the LLM upon refresh to optimize token usage, and restructuring the size of our outputs in the AI tab to improve the visibility of all components and better align with DSCI 531 visualization best practices.

**Trade-offs:** We prioritized our peer feedback based on user experience; any issues that caused confusion or required clarification for using the dashboard were classified as critical and addressed first. Details of the feedback prioritization and full rationale can be found in [#86](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/86).

**Most useful:** The two main lectures that drove the heart of this milestone were the topics on **Databases in Shiny** (learning lazy loading with the use of parquet + DuckDB + ibis) and documenting the responses of an LLM, which we directly applied to our implementation of MongoDB logging. Given our current technical limitations, it would have been helpful to cover concurrent user handling within Shiny.

#### Tests

For this milestone, we refactored the core data-filtering logic out of the Shiny server into a testable Python function (`src/helpers.py`) and implemented a testing suite using `pytest` and `playwright`.

1. Unit Tests (Logic)

`test_filter_empty_years`

- This test covers the edge case where a user deselects all years, passing an empty list to the filter function. It verifies that the function intercepts this and safely returns an empty dataframe.

- What could break: If this logic is accidentally removed, the Pandas filter evaluates an empty list as False and bypasses the year filter entirely. This would result in the dashboard confusingly displaying all years of data when the user specifically asked for zero years.

`test_filter_valid_conditions`

- This tests covers the accuracy of the helper filter data function. It verifies that when valid years and crime types are provided, the function correctly applies the logic to return the exact matching rows.

- What could break: If a future developer accidentally alters the Pandas logic, the charts would display wildly incorrect data, completely invalidating the user's analysis.

2. UI Tests (Playwright)

`test_initial_dashboard_state`

- This test acts as a baseline check, verifying that when the dashboard first loads, the UI components (like the year checkbox and time display radio buttons) correctly display their intended default parameters.

- What could break: If the default selected arguments are accidentally deleted from the app_ui layout code, the dashboard could load completely blank or with arbitrary choices, creating a confusing first impression.

`test_filter_changes_update_ui`

- This test verifies the basic interactivity of the dashboard, ensuring that when a user clicks on different radio buttons or checkboxes, the UI successfully registers and holds those new states.

- What could break: If a Shiny update or a code typo breaks the input bindings in the UI, the filters might become "frozen" and unresponsive to user clicks, rendering the dashboard useless.

`test_reset_button_restores_defaults`

- This test simulates a user changing the dashboard state and clicking the reset button. It verifies that the reset button's logic is correct to be able to physically flip the toggles back to their original defaults.

- What could break: As the dashboard grows, if new inputs are added or IDs change, but the `reset_filters()` function isn't updated to match, the reset button will become partially or fully broken, leaving old filters applied.

`test_empty_year_warning`

- This test verifies our custom reactive error handling. It ensures that when a user triggers an edge case (deselecting all years), the app actively forces the selection back to a safe default ("2025") and throws a visible warning on the screen.

- What could break: If the `_enforce_year_selection` reactive effect is broken, deleted, or disconnected, the user will not receive any visual feedback as to why their charts suddenly disappeared or broke, leading to a frustrating user experience.

## [0.3.0] - Milestone 3 - 2026-03-08

### Added

- Added querychat AI interface as new tab [#67](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/67)
- Connected all output components (map, donut chart, timeline) to update with the querychat filtered data frame [#71](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/71)
- Implemented LLM-linked filtered dataframe [#68](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/68)
- Added download button for filtered dataframe [1b3f927](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/68/changes/1b3f9270152b1219bfa589461f5015de24157a2d)
- Added extra instructions to LLM prompt to clarify informal naming conventions for neighborhoods + crime types [400ddb9](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/68/changes/400ddb91e3c69cc4aa3629814742198f2c95f5e3), [2ba2e98](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/68/changes/2ba2e98c98c431affd11c4cf6693cde0e935e192)
- Added hover/click prompts for clearer tooltip navigation [f3f01e8](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72/changes/f3f01e8aaa74bc2f4c791dfcfa4eb042b4f6827e)

### Changed 

- Addressed instructor's [HARD](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/issues/62) improvement, changed default options to be more user specific [#72](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72)
- Addressed TA improvement: Increased legend font size in donut chart + added percentage and hover labels for better user-guidance[#72](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72)
- Changed donut chart from altair to plotly to address display issues + accomodate additional features from TA feedback [20da210](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72/changes/20da210f9a486be9f2b1aabd066c17f862cbd777)
- Refactored code into separate files, one per output component [ade132a](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/71/changes/ade132a7ba5a55a703b92fba9d600e958cf4e1b9)
- Updated dashbaord demo in readme to reflect new additions [#73](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/73)
- Updated AI-chat related dependencies [35f5d16](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/67/changes/35f5d16e90eed83c30f7df19360535ddc9d99115)

### Fixed

- Fixed reset button to align with new default settings [89fca3d](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72/changes/89fca3d624e653a7a817f5aa712df6d03a6ed4f9)
- Fixed import statment in app.py to avoid local/remote errors upon deployment [3cbff4c](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/71/changes/3cbff4c83f3e659e1c88483b058e33dd9f29f658)
- Resized outputs in new AI tab to fix display errors(chart cutoffs, zooming defaults) [4587e14](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/71/changes/4587e142b2aff0b11ccf641e4efc4fe77b47d216), [061c233](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72/changes/061c233dd5ee18b058650e004e99eceb3938230f), [a6ff9a8](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/67/changes/a6ff9a81df8a725ba4b6035f491dfa85c6d30de7)
- Fixed color legend titles/column names/chart titles to better accomodate darkmode color changes [7c1c2bb](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72/changes/7c1c2bb7a5cacc493c9d8d90584d60aecbe23497), [58cfb63](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/72/changes/58cfb634c9726d220dc9626fdb91949b5569df78)

## Reflection 2:

This milestone expanded our dashboard's capabilities with the addition of the AI explorer tab, which now allows users, especially prospective business owners, to easily query the Vancouver crime dataset using natural language through a querychat interface. The AI tab mirror's the main dashboard's outputs so that users can simply search for their desired neighborhoods, relevant crime types and the years they are interested in exploring. Additionally, if users want to conduct their own analysis, they are able to download the filtered dataframe. We also updated our default settings to show the neighborhoods with the most bakeries and the most business-relevant crime types (like theft and break and enter-commercial) from the past year (2025). This allows for a more meaningful starting view, giving users better guidance in the questions they may want to explore further, instead of having all options selected as a default which we realized can be overwhelming. Since it is quite easy for users to miss useful tooltip features, we added icons to help with tooltip navigation for each plot. Lastly, we expanded LLM instructions so that informal naming conventions like 'downtown' or 'vandalism' can be translated to their related crime-type/neighborhoods which may be named differently in the raw data.

An improvement we will consider for M4 is implementing a static greeting instead of having the dashboard call the API each time it is refreshed, which will enable more mindful token usage. Furthermore, a current limitation is the size of our outputs after the addition of a dataframe in the AI tab. We will consider updating the layout of our app, to have better visibility of all components. The size of our outputs currently deviates from best visualization practises, but we thought each output was important to keep and communicates key insights from our dataset. Finally, a stretch goal would be implementing a modal pop up feature where users can input neighborhoods they want to see, and having our default settings update based on this user-specific selection.

## [0.2.0] - Milestone 2 - 2026-02-28

### Added

- Set up development branch [#22](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/22)
- Added requirements.txt for deployment [#22](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/22)
- Linked main and dev branches to Posit Cloud Connect for dashboard previewing
- Imported Data to app [#41](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/41)
- Implemented input component 1: year selection filter [#39](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/39)
- Implemented input component 2: neighborhood selection filter [#42](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/42)
- Implemented input component 3: crime type selection filter [#43](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/43)
- Implemented input component 4: time aggregation selection [#47](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/47)
- Implemented reactive calculation for filtered data [#45](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/45)
- Generated output 1: donut plot showing distribution of crime types [#44](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/44)
- Generated output 2: timeline chart [#47](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/47)
- Generated output 3: geospatial map of Vancouver neighborhoods[#48](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/48)
- Added KPI cards to dashboard [#50](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/50)
- Added additional complexity enhancement feature: reset filters button [#55](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/55)
- Added app specification to report [#46](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/46)
- Added 4th job story to integrate timeline chart output [a82f7d0](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/commit/a82f7d01aa0c076c8b3b7e2bc9fd182c723ab1eb)

### Changed

- Changed time filter input ([from M1 sketch](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/blob/dev/reports/m1_proposal.md#app-sketch--description)) to year selection input [#39](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/39)
- Updated readme instructions, included deployment links and demo of dashboard [#49](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/49), [#58](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/58)
- Updated component inventory to reflect new KPIs,reset button and new input/output ID names [9580267](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/59/changes/9580267b2268fb1a3917085c0bcc22b7ee999b30)

### Fixed

- Fixed timeline chart axis label[#51](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/51)
- Added empty data checks to avoid KPI errors for missing location/time data [a50ceac](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/55/commits/a50ceac614e718fb2ae9bc9f953f495ed4773694)
- Adjusted axis label colors to accomodate visibility in dark mode [#57](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/57)
- Cleaned and concatenated raw data files for easier implementation [#40](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/40)

## Reflection

From our initial [App sketch](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/blob/dev/reports/m1_proposal.md#app-sketch--description), we implemented all outputs as planned: a geospatial view using a map, a timeline chart, and a donut chart showing crime type distributions.

In terms of changes, our original 'filter time' input was changed from 'last month/last year' radio buttons to a year selector, giving users more flexibility to extract trends from all years. The time display aggregation (monthly/weekly/hourly) was kept but 'yearly' was removed since we adopted a one-line-per-year approach on the timeline. The rest of the inputs were implemented as planned. We also opted to remove the map's toggle feature from our sketch as we agreed that showing exact data points on the map would be too cluttered, given our large dataset, and instead, aggregating total crimes per neighborhood and illutrsating these through bubbles, made for a nicer, less cluttered visualization that encoded crime density more clearly.

For KPIs, we replaced our original sketch's ideas with three new ones: Least Crime neighbourhood, Peak Crime Time, and Total Crimes by Year, which were displayed at the top of the dashboard as they conveyed important data summaries. We agreed that this was a smarter design choice. A future refinement would be to add a KPI that is linked to an additional interactivity feature in the donut chart, where clicking on each sector of the chart updates the KPI with the crime type name and percentage value.

In future milestones, we also plan to explore finer-grained map views that allow users to zoom into individual neighbourhoods and see where crimes are occurring at a more local level.

All 3 [job stories](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/blob/dev/reports/m2_spec.md#1-updated-job-stories) were successfully implemented in this milestone. We also added a fourth job story to capture time-based comparisons, allowing the store owner to identify the safest hours, days, and seasons to operate their business.

In terms of known issues, we noticed during app development that location and time data (specifically hour and minute data) are omitted for homicide crimes. This is likely due to homicide records being sensitive and the need to protect persons affected. To avoid related errors, we implemented empty data checks so that when time data is unavailable, the KPI returns 'N/A'. Additionally, when the dashboard is deployed multiple times, the map often doesn't render correctly and may need to be refreshed to ensure all bubbles are correctly illustrated.

One limitation with our current app implementation is that each output component is coded with a different package (map is coded with ipyleaflet, donut chart with altair and timeline chart with plotly). For better conistsency, standardizing visualization libraries across all outputs is a planned M3/M4 refinement. A strength of our dashboard is that our donut chart uses tableau10 which is a color-blind friendly palette. We will extend this to our timeline chart to better adhere to data vis practises. Overall, our dashboard satisfies a geospaital comparison of crime hotsports, enables easy time-based and crime-type comparisons, with user-friendly selection options.

## [0.1.0] - Milestone 1 - 2026-02-14

### Added

- Conducted EDA on Crime Dataset, with step by step analysis documented in [notebook](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/blob/dev/notebooks/VancouverCrimeAnalysis.ipynb)[#13](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/13)
- Created User persona and Job stories, added to proposal document [#13](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/13)
- Adapted contributing and code of conduct files[#17](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/17)
- Added Dashboard summaries to documentation[#18](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/18)
- Added Dashboard motivation and purpose to proposal[#19](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/19)
- Generated dataset description and app sketch[#20](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/20)
- Set up environment.yml for EDA [cfb1fbb](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/commit/cfb1fbb9eb60ef0d6969ee9e84cf950faccf63c2)
- Created App skeleton [#16](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/16)

### Changed

- Updated Readme with set up/how to run dashboard locally instructions [#21](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/21)
- Updated User stories to reflect business owner persona [bab737e](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/13/changes/bab737e0c905afff34bf573e54a5eaf0dd97244e)
- Updated environment.yml with app dependencies [807cc2b](https://github.com/UBC-MDS/DSCI-532_2026_4_VanCrimeWatch/pull/16/changes/807cc2b65452f79607fbc1cb38df1684c7223a2e)


