# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Upcoming features and fixes

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
