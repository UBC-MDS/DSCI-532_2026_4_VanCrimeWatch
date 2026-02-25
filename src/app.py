from ipyleaflet import Map  
from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_widget  
import plotly.express as px
from pathlib import Path
import pandas as pd

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
                "CHARTS",
                ui.layout_columns(
                    ui.card(
                        ui.p("BAR/DONUT CHART"),
                        ui.p("Crime numbers displayed on interactive chart."),
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
                          labels={"label": "Month", "count": "Avg Incidents", "year": "Year"},
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
                          labels={"weekday": "Day", "count": "Avg Incidents", "year": "Year"},
                          category_orders={"weekday": day_order})

        else:  # hourly
            # Filter out HOUR=0 & MINUTE=0 (default timestamp for unknown time)
            hourly_df = df_copy[~((df_copy["HOUR"] == 0) & (df_copy["MINUTE"] == 0))]
            grouped = hourly_df.groupby(["year", "HOUR"]).size().reset_index(name="count")
            grouped = grouped.sort_values(["year", "HOUR"])
            fig = px.line(grouped, x="HOUR", y="count", color="year",
                          labels={"HOUR": "Hour", "count": "Avg Incidents", "year": "Year"})

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
