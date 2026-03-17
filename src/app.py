from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget
from pathlib import Path
import pandas as pd
import sys, os
from dotenv import load_dotenv
from querychat import QueryChat
import ibis

load_dotenv(Path(__file__).parent.parent / ".env")

# sys.path.insert(0, Path(__file__).parent)
if __package__ and __package__ != "__main__":
    from src.kpi_cards import *
    from src.donut_chart import _make_donut_plot
    from src.map_render import _make_map
    from src.timeline_chart import _make_timeline_chart
    from src.helpers import *
    from src.llm_logger import COOKIE_JS, history_tab, llm_logger
else:
    from kpi_cards import *
    from donut_chart import _make_donut_plot
    from map_render import _make_map
    from timeline_chart import _make_timeline_chart
    from helpers import *
    from llm_logger import COOKIE_JS, history_tab, llm_logger

appdir = Path(__file__).parent

#replaced data loading with lazy loading: parquet + DuckDB
parquet_path = str(appdir.parent / "data" / "processed" / "combined_crime_data_2023_2025.parquet")
con = ibis.duckdb.connect()
base_df = con.read_parquet(parquet_path)

base_df = base_df.mutate(
    TYPE=base_df.TYPE.re_replace("Vehicle Collision or Pedestrian Struck.*", "Vehicle Collision or Pedestrian Struck"))

neighbourhoods = base_df.select("NEIGHBOURHOOD").distinct().execute()["NEIGHBOURHOOD"].dropna().tolist()
crimetypes = base_df.select("TYPE").distinct().execute()["TYPE"].dropna().tolist()

business_crime_types = [
    "Break and Enter Commercial",
    "Theft from Vehicle",
    "Other Theft",
    "Mischief",
    "Theft of Vehicle",
]


qc = QueryChat(
    base_df.execute(),
    "vancouver_crime",
    client="anthropic/claude-haiku-4-5",
    #    greeting="Welcome to the Vancouver Crime Data Explorer. Ask me anything about crime data from 2023-2025, such as 'top 5 crime types' or 'crimes in Downtown'.",
    extra_instructions=extra_instructions,
)


dashboard_tab = ui.nav_panel(
    "Dashboard",
    COOKIE_JS,
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
            ui.input_selectize(
                id="input_neighbourhood",
                label="Select Neighbourhoods:",
                choices=neighbourhoods,
                multiple=True,
                selected=[
                    "Central Business District",
                    "West End",
                ],
                options={
                    "placeholder": "Displaying All",
                },
            ),
            ui.input_action_button(
                id="clear_neighbourhood",
                label="✕ Clear Selection",
                class_="btn btn-sm btn-outline-secondary mt-1 d-block mx-auto",
            ),
        ),
            ui.div(
                ui.input_selectize(
                    id="input_crime_type",
                    label="Select Crime Types:",
                    choices=crimetypes,
                    multiple=True,
                    selected=business_crime_types,
                    options={
                        "placeholder": "Displaying All",
                    },
                ),
                ui.input_action_button(
                    id="clear_crime_type",
                    label="✕ Clear Selection",
                    class_="btn btn-sm btn-outline-secondary mt-1 d-block mx-auto",
                ),
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
        ui.output_ui("selection_summary"),
        # card for KPIs
        kpi_card_widget(),
        # map widget
        ui.div(
            get_card_header("", icon="Click"),
            output_widget("map"),
        ),
        ui.layout_columns(
            ui.card(
                get_card_header("Types of Crime", icon="Hover"),
                ui.output_ui("donut_plot"),
            ),
            ui.card(
                get_card_header("Crime Timeline", icon="Hover"),
                ui.output_ui("timeline_chart"),
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
                ui.card_header(
                    ui.div(
                        "Filtered Data",
                        ui.span(
                            ui.download_button(
                                "download_filtered",
                                ui.span(
                                    ui.HTML(
                                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-download-icon lucide-download"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>'
                                    ),
                                    " Download Filtered CSV",
                                ),
                                class_="btn-success btn-sm",
                            ),
                            style="margin-left:auto; display:inline-flex; align-items:center;",
                        ),
                        style="display:flex; align-items:center; width:100%;",
                    )
                ),
                ui.output_data_frame("ai_data_table"),
                height="380px",
            ),
        ),
        # Bottom row: Donut chart (left) + Timeline chart (right)
        ui.layout_columns(
            # AI Types of Crime Donut Chart
            ui.card(
                get_card_header("Types of Crime", icon="Hover"),
                ui.output_ui("ai_donut_plot"),
                style="min-height: 400px;",
            ),
            # AI Crime Timeline
            ui.card(
                get_card_header("Crime Timeline", icon="Hover"),
                ui.output_ui("ai_timeline_chart"),
                style="min-height: 400px;",
            ),
        ),
        # Download button
        fillable_mobile=True,
    ),
)

app_ui = ui.page_navbar(
    dashboard_tab,
    ai_tab,
    history_tab,
    ui.nav_spacer(),
    ui.nav_control(
        ui.input_dark_mode(id="mode", mode="light"),
    ),
    title=ui.div(
        ui.h1("VanCrimeWatch", class_="mb-0 fs-4 text-white"),
        class_="d-flex align-items-center",
    ),
    header=ui.TagList(
        ui.include_css(appdir.parent / "src" / "styles.css"),
        ui.tags.script(src="https://cdn.plot.ly/plotly-2.35.2.min.js"),
    ),
    navbar_options=ui.navbar_options(
        theme="dark",
        class_="bg-primary text-white p-4 mb-0 d-flex justify-content-between align-items-center",
    ),
    id="navbar",
)


def server(input, output, session):
    #session.on_ended(con.disconnect)
    qc_vals = qc.server()

    llm_logger(input, output, session, qc_vals)

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

    @render.ui
    def ai_donut_plot():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        if df.empty:
            return ui.p("No data found for your query. The crime type you are searching for has no records or does not exist, " \
                        "Try rephrasing or broadening your search.",
                    style="color: #6c757d; text-align: center; padding: 40px;")
        fig = _make_donut_plot(df, input, compact=True)
        return ui.HTML(
            fig.to_html(
                full_html=False, include_plotlyjs=False, config={"responsive": True}
            )
        )

    @render.ui
    def donut_plot():
        fig = _make_donut_plot(filtered_data(), input)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True}))

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
        df = filter_crime_data(
            df=base_df,
            years=list(input.input_year()),
            crimes=list(input.input_crime_type()),
            neighbourhoods=list(input.input_neighbourhood())
        )

        return df

    render_kpis(output, input, filtered_data)
    
    @render.ui
    def selection_summary():
        return selection_summary_helper(output, input, crimetypes, neighbourhoods)

    @reactive.effect
    @reactive.event(input.reset_btn)
    def reset_filters():
        ui.update_selectize("input_neighbourhood", selected=["Central Business District", "West End"])
        ui.update_selectize("input_crime_type", selected=business_crime_types)
        ui.update_checkbox_group("input_year", selected=["2025"])
        ui.update_radio_buttons("time_display", selected="monthly")

    @reactive.effect
    def _enforce_year_selection():
        selected_years = input.input_year()
        
        # Check if selected_years is empty (if the user deselected everything)
        if not selected_years:
            # Force the checkbox group back to a default value ("2025")
            ui.update_checkbox_group("input_year", selected=["2025"])
            
            # Let the user know why their action was reversed
            ui.notification_show("Please select at least one year.", type="warning", duration=3)

    @reactive.effect
    @reactive.event(input.clear_neighbourhood)
    def _():
        ui.update_selectize("input_neighbourhood", selected=[])

    @reactive.effect
    @reactive.event(input.clear_crime_type)
    def _():
        ui.update_selectize("input_crime_type", selected=[])
        
    @render.ui
    def ai_timeline_chart():
        df = qc_vals.df()
        df = df.to_native() if hasattr(df, "to_native") else df
        if df.empty:
            return ui.p("No data found for your query. Only data from the years 2023, 2024 and 2025 exist in our records." \
                        " Try rephrasing or broadening your search.",
                    style="color: #6c757d; text-align: center; padding: 40px;")
        fig = _make_timeline_chart(df, input, compact=True)
        return ui.HTML(
            fig.to_html(
                full_html=False, include_plotlyjs=False, config={"responsive": True}
            )
        )

    @render.ui
    def timeline_chart():
        fig = _make_timeline_chart(filtered_data(), input)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"responsive": True}))


app = App(app_ui, server)
