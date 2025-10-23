import numpy as np
import plotly.graph_objects as go
from astropy.coordinates import EarthLocation, SkyCoord, HADec, AltAz
from astropy.time import Time


def split_two_on_gap_in_one(
    seq_to_split_on: list[int | float],
    threshold_for_split: int | float,
    *other_seqs: list[list[int | float]],
) -> list[list[int | float]]:
    n = len(seq_to_split_on)

    if any(len(s) != n for s in other_seqs):
        raise ValueError("All sequences must have the same length")
    if n == 0:
        return []
    groups = []
    start = 0
    for i in range(1, n):
        if seq_to_split_on[i] - seq_to_split_on[i - 1] > threshold_for_split:
            a_slice = seq_to_split_on[start:i]
            b_slices = [s[start:i] for s in other_seqs]
            groups.append([a_slice] + b_slices)
            start = i
    # final chunk
    a_slice = seq_to_split_on[start:]
    b_slices = [s[start:] for s in other_seqs]
    groups.append([a_slice] + b_slices)
    return groups


def generate_hadec_map(location: EarthLocation) -> go.Figure:
    """Given an earth location, generate a Ha-Dec map projected onto an azel grid."""
    time = Time.now()

    fig = go.Figure()

    # flags to show exactly one legend item per type
    ha_legend_shown = False
    dec_legend_shown = False

    for ha in range(-160, 161, 20):
        azs = []
        els = []
        has = []
        decs = []
        for dec in range(-40, 89, 1):
            azel_coord = SkyCoord(ha, dec, unit=(
                "deg", "deg"), frame=HADec, location=location, obstime=time).transform_to(AltAz)
            az = azel_coord.spherical.lon.degree
            el = azel_coord.spherical.lat.degree
            azs.append(az)
            els.append(el)
            has.append(ha)
            decs.append(dec)
        plot_groups = split_two_on_gap_in_one(azs, 5, els, has, decs)
        for azs, els, has, decs in plot_groups:
            label_idx = np.argmin([abs(el - 5) for el in els])
            show_legend_now = not ha_legend_shown
            fig.add_trace(
                go.Scatter(
                    x=azs,
                    y=els,
                    mode="lines+text",
                    line=dict(color="blue"),
                    showlegend=show_legend_now,
                    name="Hour angle",
                    customdata=list(zip(has, decs)),
                    hovertemplate="HA: %{customdata[0]:.2f}°<br>"
                    + "Dec: %{customdata[1]:.2f}°<br>"
                    + "Az: %{x:.2f}°<br>"
                    + "El: %{y:.2f}°<extra></extra>",
                )
            )
            if show_legend_now:
                ha_legend_shown = True
            fig.add_annotation(
                x=azs[label_idx],
                y=5,
                text=str(ha) + "°",
                showarrow=False,
                bgcolor="white",
                font=dict(color="blue", size=12, weight="bold"),
                align="center",
            )

    for dec in range(-30, 80, 10):
        azs = []
        els = []
        has = []
        decs = []
        for ha in range(-179, 179, 1):
            azel_coord = SkyCoord(ha, dec, unit=(
                "deg", "deg"), frame=HADec, location=location, obstime=time).transform_to(AltAz)
            az = azel_coord.spherical.lon.degree
            el = azel_coord.spherical.lat.degree
            azs.append(az)
            els.append(el)
            has.append(ha)
            decs.append(dec)
        plot_groups = split_two_on_gap_in_one(azs, 5, els, has, decs)
        for azs, els, has, decs in plot_groups:
            label_idx = np.argmin([abs(az - 180) for az in azs])
            show_legend_now = not dec_legend_shown
            fig.add_trace(
                go.Scatter(
                    x=azs,
                    y=els,
                    mode="lines+text",
                    line=dict(color="red"),
                    showlegend=show_legend_now,
                    name="Declination",
                    customdata=list(zip(has, decs)),
                    hovertemplate="HA: %{customdata[0]:.2f}°<br>"
                    + "Dec: %{customdata[1]:.2f}°<br>"
                    + "Az: %{x:.2f}°<br>"
                    + "El: %{y:.2f}°<extra></extra>",
                )
            )
            if show_legend_now:
                dec_legend_shown = True
            fig.add_annotation(
                x=azs[label_idx],
                y=els[label_idx],
                text=str(dec) + "°",
                showarrow=False,
                bgcolor="white",
                font=dict(color="red", size=12, weight="bold"),
                align="center",
            )

    for text, x in [
        ("North", 0),
        ("North", 360),
        ("East", 90),
        ("South", 180),
        ("West", 270),
    ]:
        fig.add_annotation(
            x=x,
            y=0,
            text=text,
            showarrow=False,
            font=dict(color="black", size=14, weight="bold"),
            align="center",
            yshift=-35,
        )
    fig.add_annotation(
        x=0,
        y=90,
        text="Zenith",
        showarrow=False,
        font=dict(color="black", size=14, weight="bold"),
        align="center",
        xshift=-50,
    )
    fig.add_annotation(
        x=360,
        y=90,
        text="Zenith",
        showarrow=False,
        font=dict(color="black", size=14, weight="bold"),
        align="center",
        xshift=50,
    )
    ncp_el = SkyCoord(0, 90, unit=(
        "deg", "deg"), frame=HADec, location=location, obstime=time).transform_to(AltAz).spherical.lat.degree

    fig.add_annotation(
        x=360,
        y=ncp_el,
        text="NCP",
        showarrow=False,
        font=dict(color="black", size=14, weight="bold"),
        align="center",
        bgcolor="white",
    )
    fig.add_annotation(
        x=0,
        y=ncp_el,
        text="NCP",
        showarrow=False,
        font=dict(color="black", size=14, weight="bold"),
        align="center",
        bgcolor="white",
    )
    fig.update_layout(
        # title="Ha-Dec Map Projected onto Az-El Grid",
        xaxis_title="Azimuth (degrees)",
        yaxis_title="Elevation (degrees)",
        xaxis=dict(
            range=[0, 360],
            dtick=20,
            showline=True,
            linecolor="black",
            ticks="inside",
            tickwidth=2,
            ticklen=10,
            linewidth=2,
            mirror="ticks",
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=0.5,
            minor=dict(ticklen=5, dtick=10, ticks="inside", showgrid=False),
        ),
        yaxis=dict(
            range=[0, 90],
            dtick=10,
            showline=True,
            linecolor="black",
            ticks="inside",
            tickwidth=2,
            ticklen=10,
            linewidth=2,
            mirror="ticks",
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=0.5,
            minor=dict(ticklen=5, dtick=5, ticks="inside", showgrid=False),
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1),
        font=dict(size=18),
    )
    return fig


if __name__ == "__main__":
    # this is the galt
    telescope_location = EarthLocation.from_geodetic(
        lat=49.32102306, lon=-119.61898028, height=546.566
    )
    figure = generate_hadec_map(telescope_location)
    figure.show()
    figure.update_layout(width=1250, height=900)
    figure.show()
    # figure.write_image("azel_hadec_map.pdf", format="pdf", width=3508, height=2480)
