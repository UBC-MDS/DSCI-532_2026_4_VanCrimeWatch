from pyproj import Transformer
from ipywidgets import HTML
from ipyleaflet import Map, CircleMarker, Popup

import math

def _make_map(df):
    df = df[(df['X'] != 0) & (df['Y'] != 0)]
    m = Map(center=(49.25, -123.10), zoom=12)

    if df.empty:
        return m

    neighbourhood_counts = df.groupby('NEIGHBOURHOOD').agg(
        COUNT=('TYPE', 'count'),
        X=('X', 'mean'),
        Y=('Y', 'mean')
    ).reset_index()

    transformer = Transformer.from_crs("EPSG:32610", "EPSG:4326", always_xy=True)
    neighbourhood_counts['LON'], neighbourhood_counts['LAT'] = transformer.transform(
        neighbourhood_counts['X'].values,
        neighbourhood_counts['Y'].values,
    )

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
            weight=1,
        )
        circle.popup = Popup(
            location=(row['LAT'], row['LON']),
            child=HTML(value=f"<b>{row['NEIGHBOURHOOD']}</b><br>Total Crimes: {row['COUNT']}"),
            close_button=True,
        )
        m.add(circle)

    return m