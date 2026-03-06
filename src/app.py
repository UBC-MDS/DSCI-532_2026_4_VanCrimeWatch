from ipyleaflet import Map, CircleMarker, Popup
from ipywidgets import HTML
import math
from pyproj import Transformer
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget, render_altair
import plotly.express as px
from pathlib import Path
import pandas as pd
import altair as alt
import sys
from dotenv import load_dotenv
from querychat import QueryChat

load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, Path(__file__).parent)
from src.kpi_cards import *

appdir = Path(__file__).parent

filename = f"combined_crime_data_2023_2025.csv"
path = appdir.parent / "data" / "processed" / filename
base_df = pd.read_csv(path)

neighbourhoods = base_df['NEIGHBOURHOOD'].unique().tolist()
crimetypes = base_df['TYPE'].unique().tolist()


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

Valid NEIGHBOURHOOD values are EXACTLY (use these exact strings in SQL queries):
'Arbutus Ridge', 'Central Business District', 'Dunbar-Southlands', 'Fairview',
'Grandview-Woodland', 'Hastings-Sunrise', 'Kensington-Cedar Cottage', 'Kerrisdale',
'Killarney', 'Kitsilano', 'Marpole', 'Mount Pleasant', 'Musqueam', 'Oakridge',
'Renfrew-Collingwood', 'Riley Park', 'Shaughnessy', 'South Cambie', 'Stanley Park',
'Strathcona', 'Sunset', 'Victoria-Fraserview', 'West End', 'West Point Grey'

When a user refers to a neighbourhood using an informal name, map it as follows:
- 'Downtown' or 'City Centre' → 'Central Business District'
- 'East Van' or 'East Vancouver' → 'Hastings-Sunrise' or 'Grandview-Woodland'
- 'Kits' → 'Kitsilano'
- 'Riley' → 'Riley Park'
- 'Strathy' → 'Strathcona'
""",
)

header = ui.div(
    ui.div(
        ui.h1("VanCrimeWatch", class_="mb-0 fs-4"),
    ),
    ui.tags.span(ui.input_dark_mode(id="mode", mode="light"), class_="bg-transparent border-0 text-dark"),
    class_="bg-primary text-white p-4 mb-0 d-flex justify-content-between align-items-center",
)

dashboard_tab = ui.nav_panel(
    "Dashboard",
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
                ui.input_selectize(  
                id = "input_neighbourhood",  
                label = "Select Neighbourhoods:",  
                choices = neighbourhoods,  
                multiple=True,
                options={
                    "placeholder": "Displaying All",
                    "plugins": ["clear_button"]
                }
            )),
            ui.input_selectize(
                id = "input_crime_type",
                label = "Select Crime Types:", 
                choices = crimetypes, 
                multiple = True,
                options={
                    "placeholder": "Displaying All",
                    "plugins": ["clear_button"]
                }),
            ui.p("TIMELINE"),
            ui.input_radio_buttons(
                "time_display",
                "Aggregate By:",
                {"monthly": "Monthly", "weekly": "Weekly (Day of Week)", "hourly": "Hourly"},
                selected="monthly",
            ),
            ui.input_checkbox_group(
                id = "input_year",  
                label = "Select Year:",
                choices = {
                    "2023": "2023", 
                    "2024": "2024", 
                    "2025": "2025"
                },
                selected=["2023", "2024", "2025"], # default selects all the years
            ),
            ui.input_action_button("reset_btn", "Reset Filters", class_="btn-success w-100"),
            title="Dashboard Filters",
            open="desktop", 
        ),
        # card for KPIs
        kpi_card_widget(),

        #map widget
        output_widget("map"),

        ui.layout_columns(
            ui.card(
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Types of Crime"),
                        output_widget("donut_plot"),
                    ),
                    ui.card(
                        ui.card_header("Crime Timeline"),
                        output_widget("timeline_chart"),
                    ),
                )
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
            # TODO: Replace placeholder with interactive map using qc_vals.df()
            ui.card(
                ui.card_header("Map"),
                ui.div(
                    ui.p("Map placeholder", class_="text-muted text-center mt-5"),
                    ui.p("Use qc_vals.df() to render an ipyleaflet map here.", class_="text-muted text-center small"),
                    style="height: 100%;",
                ),
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
            # TODO: Replace placeholder with donut chart using qc_vals.df().to_native()
            ui.card(
                ui.card_header("Types of Crime"),
                ui.div(
                    ui.p("Donut chart placeholder", class_="text-muted text-center mt-5"),
                    ui.p("Use qc_vals.df().to_native() to render a donut chart here.", class_="text-muted text-center small"),
                    style="height: 100%;",
                ),
                height="380px",
            ),
            # TODO: Replace placeholder with timeline chart using qc_vals.df().to_native()
            ui.card(
                ui.card_header("Crime Timeline"),
                ui.div(
                    ui.p("Timeline chart placeholder", class_="text-muted text-center mt-5"),
                    ui.p("Use qc_vals.df().to_native() to render a timeline chart here.", class_="text-muted text-center small"),
                    style="height: 100%;",
                ),
                height="380px",
            ),
        ),

        # Download button
        ui.div(
            ui.download_button("download_filtered", "Download Filtered CSV", class_="btn-success w-100"),
            style="position: sticky; bottom: 0; padding: 10px; z-index: 100;"
        ),

        fillable_mobile=True,
    ),
)

app_ui = ui.page_fluid(
    ui.include_css(appdir.parent / "src" / "styles.css"),
    header,
    ui.navset_tab(
        dashboard_tab,
        ai_tab,
        id="navbar",
    ),
    class_="container-fluid p-0",
)

def server(input, output, session):
    qc_vals = qc.server()

    # TODO: Add server-side render functions here for:
    #   - @render.data_frame for "ai_data_table" using qc_vals.df()
    #   - @render_widget for "ai_map" using qc_vals.df()
    #   - @render_widget / @render_altair for "ai_donut_plot"
    #   - @render_widget for "ai_timeline_chart"
    #   - @render.download for "download_filtered"
    #
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
    def map():
        df = filtered_data().copy()
        df = df[(df['X'] != 0) & (df['Y'] != 0)]
        map = Map(center=(49.25, -123.10), zoom=12)
        
        if df.empty:
            return map
        
        neighbourhood_counts = df.groupby('NEIGHBOURHOOD').agg(
            COUNT=('TYPE', 'count'),
            X=('X', 'mean'),
            Y=('Y', 'mean')).reset_index()

        transformer = Transformer.from_crs("EPSG:32610", "EPSG:4326", always_xy=True)
        neighbourhood_counts['LON'], neighbourhood_counts['LAT'] = transformer.transform(
            neighbourhood_counts['X'].values,
            neighbourhood_counts['Y'].values)

        max_count = neighbourhood_counts['COUNT'].max()

        for _, row in neighbourhood_counts.iterrows():
            count = row['COUNT']
            radius = int(5 + math.sqrt(count / max_count) * 50) if count > 0 else 5
            
            circle = CircleMarker(
                location=(row['LAT'], row['LON']),
                radius=radius,
                color='steelblue',
                fill_color='steelblue',
                fill_opacity=0.4,
                weight=1)
            
            circle.popup = Popup(
                location=(row['LAT'], row['LON']),
                child=HTML(value=f"<b>{row['NEIGHBOURHOOD']}</b><br>Total Crimes: {row['COUNT']}"),
                close_button=True)

            map.add(circle)

        return map
    
    @reactive.calc
    def filtered_data():
        selected_years = list(input.input_year())
        selected_crimes = list(input.input_crime_type())
        selected_neighbourhoods = list(input.input_neighbourhood())

        df = base_df
        if selected_years:
            df = df[df['YEAR'].astype(str).isin(selected_years)]
        if selected_crimes:
            df = df[df['TYPE'].isin(selected_crimes)]
        if selected_neighbourhoods:
            df = df[df['NEIGHBOURHOOD'].isin(selected_neighbourhoods)]
        return df
    
    render_kpis(output, input, filtered_data)

    @reactive.effect
    @reactive.event(input.reset_btn)
    def reset_filters():
        ui.update_selectize("input_neighbourhood", selected=[])
        ui.update_selectize("input_crime_type", selected=[])
        ui.update_checkbox_group("input_year", selected=["2023", "2024", "2025"])
        ui.update_radio_buttons("time_display", selected="monthly")
    
    @render_altair
    def donut_plot():  
        df = filtered_data().copy()

        if df.empty:
            return alt.Chart(pd.DataFrame()).mark_text().encode(text=alt.value("No data"))

        df["TYPE"] = df["TYPE"].replace({
            "Vehicle Collision or Pedestrian Struck (with Fatality)": "Vehicle Collision or Pedestrian Struck",
            "Vehicle Collision or Pedestrian Struck (with Injury)": "Vehicle Collision or Pedestrian Struck",
        })

        crime_type_counts = df.groupby("TYPE").size().reset_index(name="COUNT")

        # Detect dark mode
        is_dark = input.mode() == "dark"
        bg_color = "#00000000"
        text_color = "#ffffff" if is_dark else "#000000"

        donutplot = alt.Chart(
            crime_type_counts
        ).mark_arc(
            innerRadius=50
        ).encode(
            theta="COUNT:Q",
            color=alt.Color(
                "TYPE:N",
                scale=alt.Scale(scheme="tableau20"),
                legend=alt.Legend(
                    title=None,
                    orient="bottom",
                    columns=3,
                    labelLimit=0,
                    labelColor=text_color,
                )
            ),
            tooltip=["TYPE", "COUNT"]
        ).properties(
            width="container", 
            height=300,
            usermeta={'embedOptions': {'actions': False}},
        ).configure(
            background=bg_color,
            axis=alt.AxisConfig(labelColor=text_color, titleColor=text_color),
            legend=alt.LegendConfig(labelColor=text_color, titleColor=text_color),
            title=alt.TitleConfig(color=text_color),
        )

        return donutplot

    @render_widget
    def timeline_chart():
        df = filtered_data()
        if df is None or (hasattr(df, 'empty') and df.empty):
            return px.line(title="No data available")

        agg = input.time_display()
        df_copy = df.copy()
        df_copy["year"] = df_copy["YEAR"].astype(str)
        month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                     7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        if agg == "monthly":
            grouped = df_copy.groupby(["year", "MONTH"]).size().reset_index(name="count")
            grouped["label"] = grouped["MONTH"].map(month_map)
            grouped = grouped.sort_values(["year", "MONTH"])
            fig = px.line(grouped, x="label", y="count", color="year",
                          labels={"label": "Month", "count": "Incidents", "year": "Year"},
                          category_orders={"label": month_order})

        elif agg == "weekly":
            df_copy["date"] = pd.to_datetime(
                df_copy[["YEAR", "MONTH", "DAY"]].rename(
                    columns={"YEAR": "year", "MONTH": "month", "DAY": "day"}
                ),
                errors="coerce",
            )
            df_copy["weekday"] = df_copy["date"].dt.day_name()
            grouped = df_copy.groupby(["year", "weekday"]).size().reset_index(name="count")
            grouped["weekday"] = pd.Categorical(grouped["weekday"], categories=day_order, ordered=True)
            grouped = grouped.sort_values(["year", "weekday"])
            fig = px.line(grouped, x="weekday", y="count", color="year",
                          labels={"weekday": "Day", "count": "Incidents", "year": "Year"},
                          category_orders={"weekday": day_order})

        else:  # hourly
            # Filter out HOUR=0 & MINUTE=0 (default timestamp for unknown time)
            hourly_df = df_copy[~((df_copy["HOUR"] == 0) & (df_copy["MINUTE"] == 0))]
            grouped = hourly_df.groupby(["year", "HOUR"]).size().reset_index(name="count")
            grouped = grouped.sort_values(["year", "HOUR"])
            fig = px.line(grouped, x="HOUR", y="count", color="year",
                          labels={"HOUR": "Hour", "count": "Incidents", "year": "Year"})

        fig.update_traces(
            line_width=2,
            mode="lines+markers",
            marker=dict(size=5),
        )
        fig.update_layout(
            height=350,
            margin=dict(t=10, r=20, l=50, b=60),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(0,0,0,0.08)", gridwidth=1),
            font=dict(family="Inter, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        if agg == "hourly":
            tick_hours = list(range(0, 24, 3))
            tick_labels = ["12AM", "3AM", "6AM", "9AM", "12PM", "3PM", "6PM", "9PM"]
            fig.update_layout(xaxis=dict(tickvals=tick_hours, ticktext=tick_labels))
        return fig

app = App(app_ui, server)
