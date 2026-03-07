import plotly.express as px

def wrap_label(text, max_chars=20):
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            lines.append(current.strip())
            current = word
        else:
            current += " " + word
    lines.append(current.strip())
    return "<br>".join(lines)


def _make_donut_plot(df, input, compact=False):
    """Shared helper that builds a donut chart from a pre-processed DataFrame."""
    if df is None or (hasattr(df, 'empty') and df.empty):
        return px.pie(title="No data available")

    df = df.copy()

    crime_type_counts = df.groupby("TYPE").size().reset_index(name="COUNT")
    total = crime_type_counts["COUNT"].sum()
    crime_type_counts["PERCENTAGE"] = (crime_type_counts["COUNT"] / total * 100).round(
        1
    ).astype(str) + "%"
    crime_type_counts["TYPE"] = crime_type_counts["TYPE"].apply(wrap_label)

    # Detect dark mode
    is_dark = input.mode() == "dark"
    text_color = "#ffffff" if is_dark else "#000000"

    fig = px.pie(
        crime_type_counts,
        values="COUNT",
        names="TYPE",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        hole=0.5,
    )
    chart_domain = 0.75
    fig.update_traces(
        domain=dict(x=[0, chart_domain])  # reserve space on the right for legend
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=300 if compact else 370,
        margin=dict(t=10, b=10, l=0, r=100),
        legend=dict(
            title=None,
            orientation="v",  # vertical legend
            x=chart_domain,  # move legend to right of chart
            xanchor="left",
            y=0.5,
            yanchor="middle",
            font=dict(color=text_color, size=10 if compact else 14),
        ),
        font=dict(color=text_color),
        annotations=[
            dict(
                text=f"<b>{total}</b><br>Total",
                x=chart_domain / 2,  # center of donut domain (0 to 0.75)
                y=0.5,
                showarrow=False,
                font=dict(size=20, color=text_color),
                align="center",
            )
        ],
    )

    return fig
