"""Chart functions with one consistent style: labelled axes + units, colour-blind-safe palette,
reference lines for thresholds."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Okabe-Ito palette (colour-blind safe)
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442"]
UNIT = "µg/m³"


def _style(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(title=title, template="plotly_white", font=dict(size=13),
                      margin=dict(l=10, r=10, t=50, b=10), legend_title_text="", hovermode="closest")
    return fig


def line_chart(ts: pd.DataFrame, pollutant: str, who: float) -> go.Figure:
    fig = px.line(ts, x="month", y="value", color="influence", markers=True,
                  color_discrete_sequence=PALETTE,
                  labels={"month": "Month", "value": f"Mean {pollutant} ({UNIT})", "influence": "Station type"})
    fig.add_hline(y=who, line_dash="dash", line_color="#D55E00",
                  annotation_text=f"WHO 24-h guideline ({who} {UNIT})", annotation_position="top left")
    return _style(fig, f"Monthly mean {pollutant} by station type")


def bar_chart(by_zone: pd.DataFrame, pollutant: str) -> go.Figure:
    fig = px.bar(by_zone, x="mean", y="zone", orientation="h", color="pct_above",
                 color_continuous_scale="Oranges",
                 labels={"mean": f"Mean {pollutant} ({UNIT})", "zone": "Zone",
                         "pct_above": "% days > WHO"},
                 hover_data={"mean": ":.1f", "pct_above": ":.1f"})
    fig.update_layout(height=max(380, 28 * len(by_zone)))
    return _style(fig, f"{pollutant}: the {len(by_zone)} most exposed zones (mean concentration)")


def map_chart(geo: pd.DataFrame, pollutant: str) -> go.Figure:
    geo = geo.dropna(subset=["lat", "lon"]).assign(dot=lambda g: g["days_above"] + 1)  # size 0 = invisible
    mainland = geo["lat"].between(41, 51.5) & geo["lon"].between(-5.5, 10)
    if mainland.any():   # default view: mainland France (overseas stations are reachable by zooming out)
        center, zoom = {"lat": 46.6, "lon": 2.4}, 4.3
    else:                # only overseas stations selected: world view centred on them
        center, zoom = {"lat": geo["lat"].mean(), "lon": geo["lon"].mean()}, 1
    fig = px.scatter_map(geo, lat="lat", lon="lon", color="mean", size="dot", size_max=18,
                         color_continuous_scale="YlOrRd", zoom=zoom, center=center,
                         hover_name="site",
                         hover_data={"zone": True, "influence": True, "mean": ":.1f",
                                     "days_above": True, "dot": False, "lat": False, "lon": False},
                         labels={"mean": f"Mean ({UNIT})", "days_above": "Days > WHO"},
                         map_style="carto-positron", height=520)
    return _style(fig, f"{pollutant}: mean concentration per station (size = days above WHO)")


def season_small_multiples(season: pd.DataFrame, pollutant: str) -> go.Figure:
    order = ["Winter", "Spring", "Summer", "Autumn"]
    fig = px.bar(season, x="season", y="value", facet_col="zone", facet_col_wrap=3,
                 category_orders={"season": order}, color="season", color_discrete_sequence=PALETTE,
                 labels={"value": f"Mean {pollutant} ({UNIT})", "season": "Season"}, height=480)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(showlegend=False)
    return _style(fig, f"{pollutant}: seasonal profile of the most exposed zones")
