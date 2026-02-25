from ipyleaflet import Map  
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget, render_altair
import plotly.express as px
from pathlib import Path
import pandas as pd
import altair as alt

appdir = Path(__file__).parent

filename = f"combined_crime_data_2023_2025.csv"
path = appdir.parent / "data" / "processed" / filename
base_df = pd.read_csv(path)

neighbourhoods = base_df['NEIGHBOURHOOD'].unique().tolist()
crimetypes = base_df['TYPE'].unique().tolist()

app_ui = ui.page_fluid(
    ui.include_css(appdir / "styles.css"),
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
            ui.div(
                "Select data to display: last week/last month/last year etc",
                ui.br(), 
                "Select display type: daily/monthly/weekly"),
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
            title="Dashboard Filters",
            bg="#ffffff",
            open="desktop", 
        ),
        ui.card(
            "MAP: Interactive map of Vancouver with crime statistics visualised through circles. ",
            "Changes according to selection. ",
            "Optional display exact crime locations.",
            output_widget("map"),
        ),
        ui.layout_columns(
            ui.card(
                ui.layout_columns(
                    ui.card(
                        ui.p("Types of Crime"),
                        output_widget("donut_plot"),
                    ),
                    ui.value_box(
                        "TIMELINE: Total Crime",
                        ui.output_text("yearly_crime_total"),
                        ui.output_text("selected_year_label"),
                        showcase=output_widget("sparkline"),
                        showcase_layout="bottom",
                    ),
                )
            ),
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
            usermeta={'embedOptions': {'actions': False}},     
        )

        return donutplot

    @render.text
    def yearly_crime_total():
        df = filtered_data()
        if df is None:
            return "N/A"
        
        total = df.shape[0]
        return f"{total:,}"
    
    @render.text
    def selected_year_label():
        return f"in {input.input_year()}"

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
