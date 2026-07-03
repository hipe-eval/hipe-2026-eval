"""Shared plotting style for HIPE-2026 error-analysis figures (analysis.d/figures/*)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLOR_AT = "#1f77b4"
COLOR_ISAT = "#ff7f0e"
TASK_COLORS = {"at": COLOR_AT, "isAt": COLOR_ISAT}

Y_LIM = (0.0, 1.0)
# CEUR/LNCS single-column width (~8.5cm).
FIG_WIDTH_IN = 3.35
FIG_HEIGHT_IN = 2.6


def bucket_tick_label(name: str, n: int) -> str:
    return f"{name}\n(n={n})"


def new_figure(width: float = FIG_WIDTH_IN, height: float = FIG_HEIGHT_IN, ncols: int = 1):
    fig, axes = plt.subplots(1, ncols, figsize=(width * ncols, height), squeeze=False)
    axes = axes[0]
    if ncols == 1:
        return fig, axes[0]
    return fig, axes


def style_axis(ax, ylabel: str = "macro recall") -> None:
    ax.set_ylim(*Y_LIM)
    ax.set_ylabel(ylabel, fontsize=7)
    ax.tick_params(labelsize=6)
    ax.grid(axis="y", linewidth=0.4, alpha=0.5)


def annotate_bars(ax, bars, values, ns=None) -> None:
    for index, (bar, value) in enumerate(zip(bars, values)):
        if value is None:
            continue
        n_suffix = f"\n(n={ns[index]})" if ns is not None and ns[index] is not None else ""
        ax.annotate(
            f"{value:.2f}{n_suffix}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 2),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=5,
        )


def grouped_bar(ax, bucket_labels, series: dict, colors: dict | None = None, ns: dict | None = None, bar_width: float = 0.35) -> None:
    """Draw a grouped bar chart.

    series: dict[series_name -> list of values aligned with bucket_labels] (None entries skipped).
    ns: optional dict[series_name -> list of per-bar counts] to annotate under each bar's value.
    """
    colors = colors or TASK_COLORS
    n_series = len(series)
    x = list(range(len(bucket_labels)))
    offsets = [(i - (n_series - 1) / 2) * bar_width for i in range(n_series)]
    for offset, (name, values) in zip(offsets, series.items()):
        plot_values = [v if v is not None else 0 for v in values]
        xpos = [xi + offset for xi in x]
        bars = ax.bar(xpos, plot_values, width=bar_width, label=name, color=colors.get(name))
        annotate_bars(ax, bars, values, ns.get(name) if ns else None)
    ax.set_xticks(x)
    ax.set_xticklabels(bucket_labels)
    ax.legend(fontsize=6)


def save_figure(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
