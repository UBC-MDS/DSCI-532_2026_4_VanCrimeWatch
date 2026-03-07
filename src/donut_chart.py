import altair as alt
import pandas as pd

def _make_donut_plot(df, input):
    """Shared helper that builds a donut chart from a pre-processed DataFrame."""
    if df.empty:
        return alt.Chart(pd.DataFrame()).mark_text().encode(text=alt.value("No data"))

    df = df.copy()
    df["TYPE"] = df["TYPE"].replace({
        "Vehicle Collision or Pedestrian Struck (with Fatality)": "Vehicle Collision or Pedestrian Struck",
        "Vehicle Collision or Pedestrian Struck (with Injury)": "Vehicle Collision or Pedestrian Struck",
    })

    crime_type_counts = df.groupby("TYPE").size().reset_index(name="COUNT")
    is_dark = input.mode() == "dark"
    bg_color = "#00000000"
    text_color = "#ffffff" if is_dark else "#000000"

    return (
        alt.Chart(crime_type_counts)
        .mark_arc(innerRadius=50)
        .encode(
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
                ),
            ),
            tooltip=["TYPE", "COUNT"],
        )
        .properties(
            width="container",
            height=300,
            usermeta={"embedOptions": {"actions": False}},
        )
        .configure(
            background=bg_color,
            axis=alt.AxisConfig(labelColor=text_color, titleColor=text_color),
            legend=alt.LegendConfig(labelColor=text_color, titleColor=text_color),
            title=alt.TitleConfig(color=text_color),
        )
    )


