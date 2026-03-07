import plotly.express as px
import pandas as pd
def _make_timeline_chart(df, input):
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
