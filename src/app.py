from ipyleaflet import Map  
from shiny import App, ui
from shinywidgets import output_widget, render_widget  
import plotly.express as px
from pathlib import Path
import pandas as pd

appdir = Path(__file__).parent

app_ui = ui.page_fluid(
    ui.include_css(appdir / "styles.css"),
    ui.layout_sidebar(
        ui.sidebar(
            "Sidebar", 
            bg="#ffffff", 
            open="closed"
        ),
        output_widget("map"),
        ui.value_box(
            "Total Crime",
            "per month",
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
    
    @render_widget
    def sparkline():
        path = appdir.parent / "data" / "raw" / "crimedata_csv_AllNeighbourhoods_2023.csv"
        df = pd.read_csv(path)

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

# Open in shinylive to see additional files


# app_ui = ui.page_fixed(
#     ui.include_css(appdir / "styles.css"),
#     ui.value_box(
#         "Total Sales in Q2",
#         "$2.45M",
#         showcase=output_widget("sparkline"),
#         showcase_layout="bottom",
#     ),
#     fillable_mobile=True,
# )

# def server(input, output, session):
#     @render_widget
#     def sparkline():
#         economics = pd.read_csv(appdir / "economics.csv")
#         fig = line(economics, x="date", y="psavert")
#         fig.update_traces(
#             line_color="#406EF1",
#             line_width=1,
#             fill="tozeroy",
#             fillcolor="rgba(64,110,241,0.2)",
#             hoverinfo="y",
#         )
#         fig.update_xaxes(visible=False, showgrid=False)
#         fig.update_yaxes(visible=False, showgrid=False)
#         fig.update_layout(
#             height=100,
#             hovermode="x",
#             margin=dict(t=0, r=0, l=0, b=0),
#             plot_bgcolor="rgba(0,0,0,0)",
#             paper_bgcolor="rgba(0,0,0,0)",
#         )
#         return fig

# app = App(app_ui, server)