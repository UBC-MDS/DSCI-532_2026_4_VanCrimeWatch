from shiny import ui, render
import pandas as pd

def metric_col(m, last=None):
    """Display total counts for all years passed"""
    classes = []
    if last is not None:
        classes.append("col-md-4")
        if not last:
            classes.append("mb-3 mb-md-0")
    return ui.div(
        ui.div(
            m["value"],
            class_="metric-value text-center"
        ),
        ui.div(
            ui.span(m["sub1"], class_="metric-sub"),
            ui.span(
                m["sub2"],
                class_=f"badge {m['badge']} {m['text']} metric-trend"
            ),
            class_="d-flex justify-content-center align-items-center gap-2 mt-1",
        ),
        class_=f"col-12 {' '.join(classes)}",
    )

def render_kpis(output, input, filtered_data):

    @output
    @render.ui
    def metrics_row():
        """Output widget for total count"""
        df = filtered_data()
        yearly = df.groupby('YEAR').size().sort_index()
        result = []
        prev_count = None

        for year, count in yearly.items():
            if prev_count is None:
                trend = None
                badge = None
                text = None
            else:
                pct = round((count - prev_count) / prev_count * 100, 1)
                arrow = "▲" if pct >= 0 else "▼"
                trend = f"{arrow} {abs(pct)}%"
                badge = "bg-success" if pct < 0 else ("bg-warning" if pct < 5 else "bg-danger")
                text = "text-dark" if badge == "bg-warning" else ""

            result.append({
                "sub1": str(year),
                "value": f"{count:,}",
                "sub2": trend,
                "badge": badge,
                "text": text,
            })
            prev_count = count

        cols = []
        for i, m in enumerate(result):
            last = i == len(result) - 1
            cols.append(metric_col(m, last=last))

        return ui.div(*cols, class_="row text-center metrics-row")

    @output
    @render.ui
    def safest_block():
        """Output widget for safest neighbourhood"""
        df = filtered_data()
        block_counts = df['NEIGHBOURHOOD'].value_counts()
        safest = block_counts.idxmin()
        count = int(block_counts.min())
        pct = round(count / len(df) * 100, 1)

        return metric_col({
            "sub1": f"{count:,}",
            "value": safest,
            "sub2": f"{pct}% of total",
            "badge": "bg-info",
            "text": "text-dark",
        })

    @output
    @render.ui
    def peak_crime_period():
        """Output widget for peak crime time from timeline chart"""
        df = filtered_data()
        agg = input.time_display()
        val = ""
        if agg == "monthly":
            month_names = {
                1: "January", 2: "February", 3: "March", 4: "April",
                5: "May", 6: "June", 7: "July", 8: "August",
                9: "September", 10: "October", 11: "November", 12: "December"
            }
            counts = df.groupby("MONTH").size()
            if counts.empty:
                return metric_col({"sub1": "", "value": "N/A", "sub2": "No data", "badge": "bg-secondary", "text": ""})
            peak = month_names[counts.idxmax()]
            val = int(counts.max())

        elif agg == "weekly":
            df = df.copy()
            df["weekday"] = pd.to_datetime(df[["YEAR", "MONTH", "DAY"]].rename(
                columns={"YEAR": "year", "MONTH": "month", "DAY": "day"}
            )).dt.day_name()
            counts = df.groupby("weekday").size()
            if counts.empty:
                return metric_col({"sub1": "", "value": "N/A", "sub2": "No data", "badge": "bg-secondary", "text": ""})
            peak = counts.idxmax()
            val = int(counts.max())

        else:
            hourly_df = df[~((df["HOUR"] == 0) & (df["MINUTE"] == 0))]
            counts = hourly_df.groupby("HOUR").size().reset_index(name="count")
            if counts.empty:
                return metric_col({"sub1": "", "value": "N/A", "sub2": "No time data available", "badge": "bg-secondary", "text": ""})
            peak_idx = counts["count"].idxmax()
            peak_hour = counts.loc[peak_idx, "HOUR"]
            peak = f"{peak_hour}:00-{peak_hour + 1}:00"
            val = int(counts["count"].max())

        pct = round(val / len(df) * 100, 1)
        return metric_col({
            "sub1": f"{pct}% of total",
            "value": peak,
            "sub2": "",
            "badge": "bg-info",
            "text": "text-dark",
        })
    
def render_card(title, block, cols):
    """Metric display helper"""
    return ui.div(
                ui.div(
                    ui.div(title, class_="card-header fw-semibold"),
                    ui.div(
                        block,
                        class_="card-body",
                    ),
                    class_="card shadow-sm h-100",
                ),
                class_=f"col-12 col-md-{cols}",
                )

def kpi_card_widget():
    """Main widget to collect and display all KPIs"""
    card_details = [
        ("Least Crime", ui.output_ui("safest_block"), 3),
        ("Peak Crime Time", ui.output_ui("peak_crime_period"), 3),
        ("Total Crimes by Year", ui.output_ui("metrics_row"), 6)
    ]
    return ui.div(
                    *[
                        render_card(title, block, cols)
                        for title, block, cols in card_details
                    ],
                    class_="row g-3",
                )