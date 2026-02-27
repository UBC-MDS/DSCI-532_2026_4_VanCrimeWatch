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

sys.path.insert(0, Path(__file__).parent)
from kpi_cards import *

appdir = Path(__file__).parent

filename = f"combined_crime_data_2023_2025.csv"
path = appdir.parent / "data" / "processed" / filename
base_df = pd.read_csv(path)

neighbourhoods = base_df['NEIGHBOURHOOD'].unique().tolist()
crimetypes = base_df['TYPE'].unique().tolist()

header = ui.div(
    ui.div(
        ui.h1("VanCrimeWatch", class_="mb-0 fs-4"),
    ),
    ui.tags.span(ui.input_dark_mode(), class_="bg-transparent border-0 text-dark"),
    class_="bg-primary text-white p-4 mb-0 d-flex justify-content-between align-items-center",
)

app_ui = ui.page_fluid(
    ui.include_css(appdir.parent / "src" / "styles.css"),
    header,
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
    class_="container-fluid p-0"
) 

def server(input, output, session):
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
                    labelLimit=0
                )
            ),
            tooltip=["TYPE", "COUNT"]
        ).properties(
            width="container", 
            height=300,
            usermeta={'embedOptions': {'actions': False}},     
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
