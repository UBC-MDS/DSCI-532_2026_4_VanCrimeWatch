from ipyleaflet import Map  
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget  
import plotly.express as px
from pathlib import Path
import pandas as pd

appdir = Path(__file__).parent

app_ui = ui.page_fluid(
    ui.include_css(appdir / "styles.css"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "year",  # This is the ID we use in the server
                "Select Year:",
                {"2023": "2023", "2024": "2024", "2025": "2025"},
                selected="2023",
                multiple=False,
            ),
            title="Dashboard Filters",
            bg="#ffffff",
            open="desktop", # "closed" works too, but "desktop" shows it by default on larger screens
        ),
        output_widget("map"),
        ui.value_box(
            "Total Crime",
            ui.output_text("yearly_crime_total"),
            ui.output_text("selected_year_label"),
            showcase=output_widget("sparkline"),
            showcase_layout="bottom",
        ),
        fillable_mobile=True,
    ),
) 

def server(input, output, session):
    @render_widget  
    def map():
        return Map(center=(49.25, -123.05), zoom=11)
    
    @reactive.calc
    def filtered_data():
        selected_year = input.year()
        filename = f"crimedata_csv_AllNeighbourhoods_{selected_year}.csv"
        path = appdir.parent / "data" / "raw" / filename
        
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            return None

    @render.text
    def yearly_crime_total():
        df = filtered_data()
        if df is None:
            return "N/A"
        
        total = df.shape[0]
        return f"{total:,}"
    
    @render.text
    def selected_year_label():
        return f"in {input.year()}"

    @render_widget
    def sparkline():
        df = filtered_data()
        if df is None:
            return px.line(title="Data not found")

        df["month_year"] = pd.to_datetime(df[['YEAR', 'MONTH']].assign(DAY=1))

        monthly_crimes = df.groupby("month_year").size().reset_index(name="crime_count")
        monthly_crimes = monthly_crimes.sort_values("month_year")

        fig = px.line(monthly_crimes, x="month_year", y="crime_count")

        fig.update_traces(
            line_color="#406EF1",
            line_width=1,
            fill="tozeroy",
            fillcolor="rgba(64,110,241,0.2)",
            hoverinfo="y",
        )
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        fig.update_layout(
            height=100,
            hovermode="x",
            margin=dict(t=0, r=0, l=0, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        return fig

app = App(app_ui, server)