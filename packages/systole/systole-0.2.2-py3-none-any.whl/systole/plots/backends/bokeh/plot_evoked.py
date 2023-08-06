# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

from typing import Iterable, List, Tuple

import numpy as np
import pandas as pd
from bokeh.models import Band, ColumnDataSource, Span
from bokeh.plotting import figure
from bokeh.plotting.figure import Figure


def plot_evoked(
    epochs: List[np.ndarray],
    time: np.ndarray,
    palette: Iterable,
    figsize: Tuple[float, float],
    labels: str,
    unit: str,
    ax=None,
    ci: str = "sd",
) -> Figure:
    """Plot continuous or discontinuous RR intervals time series.

    Parameters
    ----------
    epochs : list
        A 2d (trial * time) numpy array containing the time series
        of the epoched signal.
    time : float
        Start and end time of the epochs in seconds, relative to the
        time-locked event. Defaults to -1 and 10, respectively.
    palette : int
        The sampling frequency of the epoched data.
    figsize : str
        The lines color.
    labels : str
        The condition label.
    unit : str
        The heart rate unit. Can be `'rr'` (R-R intervals, in ms) or `'bpm'` (beats
        per minutes). Default is `'bpm'`.
    ax : tuple
        Figure size. Default is `(400, 400)`.
    ci : int | str
        The confidence interval around the point estimates. Only `"sd"` is currently
        implemented.

    Returns
    -------
    evoked_plot : :class:`bokeh.plotting.figure.Figure`
        The bokeh figure containing the plot.

    """

    if ci not in ["sd"]:
        raise ValueError("This method is not yet implemented.")

    ylabel = "R-R interval (ms)" if unit == "rr" else "Beats per minute (bpm)"

    evoked_plot = figure(
        title="Instantaneous heart rate",
        sizing_mode="fixed",
        plot_width=figsize[0],
        plot_height=figsize[1],
        x_axis_label="Time",
        y_axis_label=ylabel,
    )

    # Vertical and horizontal lines
    vline = Span(
        location=0,
        dimension="height",
        line_color="grey",
        line_width=2,
        line_dash="dashed",
    )
    hline = Span(location=0, dimension="width", line_color="black", line_width=1)
    evoked_plot.renderers.extend([vline, hline])

    # Loop across condition
    for ep, lab, col in zip(epochs, labels, palette):

        for i in range(ep.shape[0]):
            evoked_plot.line(
                x=time,
                y=ep[i],
                alpha=0.2,
                line_color=col,
            )

        df_source = pd.DataFrame(
            {
                "time": time,
                "average": ep.mean(0),
                "lower": ep.mean(0) - ep.std(0),
                "upper": ep.mean(0) + ep.std(0),
            }
        )

        source = ColumnDataSource(df_source)

        # Show confidence interval
        band = Band(
            base="time",
            lower="lower",
            upper="upper",
            source=source,
            level="underlay",
            fill_alpha=0.2,
            line_width=1,
            fill_color=col,
        )
        evoked_plot.add_layout(band)

        # Show average
        evoked_plot.line(
            x="time",
            y="average",
            source=source,
            line_width=2,
            legend_label=lab,
            line_color=col,
        )

    return evoked_plot
