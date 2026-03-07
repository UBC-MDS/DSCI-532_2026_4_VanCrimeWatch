from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget
from pathlib import Path
import pandas as pd
import sys
from dotenv import load_dotenv
from querychat import QueryChat

load_dotenv(Path(__file__).parent.parent / ".env")

# sys.path.insert(0, Path(__file__).parent)
if __package__ and __package__ != "__main__":
    from src.kpi_cards import *
    from src.donut_chart import _make_donut_plot
    from src.map_render import _make_map
    from src.timeline_chart import _make_timeline_chart
else:
    from kpi_cards import *
    from donut_chart import _make_donut_plot
    from map_render import _make_map
    from timeline_chart import _make_timeline_chart

appdir = Path(__file__).parent

filename = f"combined_crime_data_2023_2025.csv"
path = appdir.parent / "data" / "processed" / filename
base_df = pd.read_csv(path)

neighbourhoods = base_df["NEIGHBOURHOOD"].unique().tolist()
crimetypes = base_df["TYPE"].unique().tolist()

business_crime_types = [
    'Break and Enter Commercial',
    'Theft from Vehicle',
    'Other Theft',
    'Mischief',
    'Theft of Vehicle'
]

base_df["TYPE"] = base_df["TYPE"].replace({
        "Vehicle Collision or Pedestrian Struck (with Fatality)": "Vehicle Collision or Pedestrian Struck",
        "Vehicle Collision or Pedestrian Struck (with Injury)": "Vehicle Collision or Pedestrian Struck",
    })


qc = QueryChat(
    base_df,
    "vancouver_crime",
    client="anthropic/claude-haiku-4-5",
    #    greeting="Welcome to the Vancouver Crime Data Explorer. Ask me anything about crime data from 2023-2025, such as 'top 5 crime types' or 'crimes in Downtown'.",
    extra_instructions="""
        This dataset contains Vancouver police crime records from 2023-2025.
        Key columns: TYPE (crime category), YEAR, MONTH, DAY, HOUR, MINUTE,
        HUNDRED_BLOCK (street address), NEIGHBOURHOOD, X (longitude), Y (latitude).
        Crime types include: Break and Enter Commercial, Break and Enter Residential/Other,
        Homicide, Mischief, Offence Against a Person, Other Theft, Theft from Vehicle,
        Theft of Bicycle, Theft of Vehicle, Vehicle Collision or Pedestrian Struck.

        When a user uses informal terms for crime types, map them as follows:
        - 'vandalism' or 'graffiti' or "property damage" = 'Mischief'
        - 'car theft' or 'stolen car' = 'Theft of Vehicle'
        - 'mugging', 'assault', or 'robbery' = 'Offence Against a Person'
        - 'bike theft' or 'stolen bike' = 'Theft of Bicycle'
        - 'break in' or 'burglary' at a house/home/apartment = 'Break and Enter Residential/Other'
        - 'break in' or 'burglary' at a store/shop/office/business = 'Break and Enter Commercial'
        - if unclear whether residential or commercial, query both types

        Valid NEIGHBOURHOOD values are EXACTLY (use these exact strings in SQL queries):
        'Arbutus Ridge', 'Central Business District', 'Dunbar-Southlands', 'Fairview',
        'Grandview-Woodland', 'Hastings-Sunrise', 'Kensington-Cedar Cottage', 'Kerrisdale',
        'Killarney', 'Kitsilano', 'Marpole', 'Mount Pleasant', 'Musqueam', 'Oakridge',
        'Renfrew-Collingwood', 'Riley Park', 'Shaughnessy', 'South Cambie', 'Stanley Park',
        'Strathcona', 'Sunset', 'Victoria-Fraserview', 'West End', 'West Point Grey'

        When a user refers to a neighbourhood using an informal name, map it as follows:
        - 'Downtown' or 'City Centre' = 'Central Business District'
        - 'East Van' or 'East Vancouver' = 'Hastings-Sunrise' or 'Grandview-Woodland'
        - 'Kits' = 'Kitsilano'
        - 'Riley' = 'Riley Park'
        - 'Strathy' = 'Strathcona'
        """,
)

dashboard_tab = ui.nav_panel(
    "Dashboard",
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
                ui.input_selectize(
                    id="input_neighbourhood",
                    label="Select Neighbourhoods:",
                    choices=neighbourhoods,
                    multiple=True,
                    selected=["Central Business District","West End"],  # default selects popular neighbourhoods
                    options={
                        "placeholder": "Displaying All",
                        "plugins": ["clear_button"],
                    },
                )
            ),
            ui.input_selectize(
                id="input_crime_type",
                label="Select Crime Types:",
                choices=crimetypes,
                multiple=True,
                selected=business_crime_types,  # default selects common business crime types
                options={"placeholder": "Displaying All", "plugins": ["clear_button"]},
            ),
            ui.p("TIMELINE"),
            ui.input_radio_buttons(
                "time_display",
                "Aggregate By:",
                {
                    "monthly": "Monthly",
                    "weekly": "Weekly (Day of Week)",
                    "hourly": "Hourly",
                },
                selected="monthly",
            ),
            ui.input_checkbox_group(
                id="input_year",
                label="Select Year:",
                choices={"2023": "2023", "2024": "2024", "2025": "2025"},
                selected=["2025"],  # default selects latest year
            ),
            ui.input_action_button(
                "reset_btn", "Reset Filters", class_="btn-success w-100"
            ),
            title="Dashboard Filters",
            open="desktop",
        ),
        # card for KPIs
        kpi_card_widget(),
        # map widget
        ui.div(
            ui.div(
                ui.span(
                    ui.HTML(
                        '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px;vertical-align:middle"><path d="M14 4.1 12 6"/><path d="m5.1 8-2.9-.8"/><path d="m6 12-1.9 2"/><path d="M7.2 2.2 8 5.1"/><path d="M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z"/></svg>'
                    ),
                    "Click for more",
                    style="display:inline-flex; align-items:center;",
                    class_="badge-right",
                ),
                style="display:flex; justify-content:flex-end; margin-bottom:4px;",
            ),
            output_widget("map"),
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header(
                    ui.div(
                        "Types of Crime",
                        ui.span(
                            ui.HTML(
                                '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px;vertical-align:middle"><path d="M22 14a8 8 0 0 1-8 8"/><path d="M18 11v-1a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v1"/><path d="M10 9.5V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v10"/><path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>'
                            ),
                            "Hover for more",
                            style="margin-left:auto; display:inline-flex; align-items:center;",
                            class_="badge-right",
                        ),
                        style="display:flex; align-items:center; width:100%;",
                    )
                ),
                output_widget("donut_plot"),
            ),
            ui.card(
                ui.card_header(
                    ui.div(
                        "Crime Timeline",
                        ui.span(
                            ui.HTML(
                                '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px;vertical-align:middle"><path d="M22 14a8 8 0 0 1-8 8"/><path d="M18 11v-1a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v1"/><path d="M10 9.5V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v10"/><path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>'
                            ),
                            "Hover for more",
                            style="margin-left:auto; display:inline-flex; align-items:center;",
                            class_="badge-right",
                        ),
                        style="display:flex; align-items:center; width:100%;",
                    ),
                ),
                output_widget("timeline_chart"),
            ),
        ),
        fillable_mobile=True,
    ),
)

# TODO : Wire up the following outputs using
# qc_vals.df() in the server function.
#
# qc_vals = qc.server()  <-- already called in server()
#
# Access the filtered dataframe with:
#   df = qc_vals.df()          # returns narwhals DataFrame
#   df_pd = df.to_native()     # convert to pandas
#
# Access the generated SQL with:
#   sql = qc_vals.sql()
#
# Reset filters with:
#   qc_vals.sql.set("")
#   qc_vals.title.set(None)
ai_tab = ui.nav_panel(
    "AI Explorer",
    ui.layout_sidebar(
        qc.sidebar(width=400),
        # Top row: Map (left) + Filtered Dataframe (right)
        ui.layout_columns(
            # AI Map
            ui.card(
                ui.card_header("Map"),
                output_widget("ai_map"),
                height="380px",
            ),
            ui.card(
                ui.card_header("Filtered Data"),
                ui.output_data_frame("ai_data_table"),
                height="380px",
            ),
        ),
        # Bottom row: Donut chart (left) + Timeline chart (right)
        ui.layout_columns(
            # AI Types of Crime Donut Chart
            ui.card(
                ui.card_header("Types of Crime"),
                output_widget("ai_donut_plot"),
                height="380px",
            ),
            # AI Crime Timeline
            ui.card(
                ui.card_header("Crime Timeline"),
                ui.output_ui("ai_timeline_chart"),
                height="380px",
            ),
        ),
        # Download button
        ui.div(
            ui.download_button(
                "download_filtered", "Download Filtered CSV", class_="btn-success w-100"
            ),
            style="position: sticky; bottom: 0; padding: 10px; z-index: 100;",
        ),
        fillable_mobile=True,
    ),
)

app_ui = ui.page_navbar(
    dashboard_tab,
    ai_tab,
    ui.nav_spacer(),
    ui.nav_control(
        ui.input_dark_mode(id="mode", mode="light"),
    ),
    title=ui.div(
        ui.h1("VanCrimeWatch", class_="mb-0 fs-4 text-white"),
        class_="d-flex align-items-center",
    ),
    header=ui.include_css(appdir.parent / "src" / "styles.css"),
    navbar_options=ui.navbar_options(
        theme="dark",
        class_="bg-primary text-white p-4 mb-0 d-flex justify-content-between align-items-center",
    ),
    id="navbar",
)


def server(input, output, session):
    qc_vals = qc.server()

    # Helper to get pandas df from querychat:
    #   df = qc_vals.df()
    #   df = df.to_native() if hasattr(df, "to_native") else df

    @render.data_frame
    def ai_data_table():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        return df

    @render.download(filename="filtered_crime_data.csv")
    def download_filtered():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        yield df.to_csv(index=False)

    @render_widget
    def ai_donut_plot():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        return _make_donut_plot(df, input, compact=True)

    @render_widget
    def donut_plot():
        return _make_donut_plot(filtered_data(), input)

    @render_widget
    def ai_map():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        return _make_map(df)

    @render_widget
    def map():
        return _make_map(filtered_data().copy())

    @reactive.calc
    def filtered_data():
        selected_years = list(input.input_year())
        selected_crimes = list(input.input_crime_type())
        selected_neighbourhoods = list(input.input_neighbourhood())

        df = base_df
        if selected_years:
            df = df[df["YEAR"].astype(str).isin(selected_years)]
        if selected_crimes:
            df = df[df["TYPE"].isin(selected_crimes)]
        if selected_neighbourhoods:
            df = df[df["NEIGHBOURHOOD"].isin(selected_neighbourhoods)]
        return df

    render_kpis(output, input, filtered_data)

    @reactive.effect
    @reactive.event(input.reset_btn)
    def reset_filters():
        ui.update_selectize("input_neighbourhood", selected=[])
        ui.update_selectize("input_crime_type", selected=[])
        ui.update_checkbox_group("input_year", selected=["2023", "2024", "2025"])
        ui.update_radio_buttons("time_display", selected="monthly")

    @render.ui
    def ai_timeline_chart():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        fig = _make_timeline_chart(df, input, compact=True)
        return ui.HTML(
            fig.to_html(
                full_html=False, include_plotlyjs="cdn", config={"responsive": True}
            )
        )

    @render_widget
    def timeline_chart():
        return _make_timeline_chart(filtered_data(), input)


app = App(app_ui, server)
