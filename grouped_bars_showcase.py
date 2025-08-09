"""
Grouped Bars Showcase
-----------------------------------
Original mini‑project demonstrating how to build clean, publication‑quality
**grouped bar charts** with custom colors, spacing, value labels, and an
optional PNG export for README previews.

Run:
    python grouped_bars_showcase.py

Save a PNG for GitHub README:
    python -c "import grouped_bars_showcase as g; g.main(save_png=True)"
"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple


# ----------------- data synthesis -------------------------------------------
@dataclass
class Series:
    name: str
    values: np.ndarray


def make_dataset(seed: int = 7) -> Tuple[List[str], List[Series]]:
    """Create a small but realistic multi‑series dataset.

    We simulate three marketing channels across four quarters. Values are
    intentionally non‑uniform and include small trends so the groups are
    visually distinct.
    """
    rng = np.random.default_rng(seed)

    quarters = ["Q1", "Q2", "Q3", "Q4"]

    # Base levels with gentle trends + noise
    web      = np.array([220, 245, 270, 310], dtype=float) + rng.normal(0, 10, 4)
    email    = np.array([150, 165, 160, 175], dtype=float) + rng.normal(0, 8,  4)
    referral = np.array([ 90, 110, 140, 155], dtype=float) + rng.normal(0, 6,  4)

    series = [
        Series("Web Ads", web),
        Series("Email", email),
        Series("Referrals", referral),
    ]
    return quarters, series


# ----------------- plotting helpers -----------------------------------------
COLOR_CYCLE = ["#1e88e5", "#43a047", "#fb8c00"]  # blue, green, orange


def add_value_labels(ax: plt.Axes, rects, *, fmt: str = "{:.0f}") -> None:
    for r in rects:
        height = r.get_height()
        ax.annotate(
            fmt.format(height),
            xy=(r.get_x() + r.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )


def grouped_bars(ax: plt.Axes, categories: List[str], series: List[Series], *,
                 width: float = 0.25, gap: float = 0.15) -> None:
    n_groups = len(categories)
    n_series = len(series)
    x = np.arange(n_groups, dtype=float)

    # Center the group so bars are symmetric around each tick
    total_width = n_series * width + (n_series - 1) * gap
    start = - total_width / 2

    bars_by_series = []
    for idx, s in enumerate(series):
        offset = start + idx * (width + gap)
        rects = ax.bar(x + offset, s.values, width,
                       label=s.name,
                       color=COLOR_CYCLE[idx % len(COLOR_CYCLE)],
                       edgecolor="black",
                       linewidth=0.6)
        add_value_labels(ax, rects)
        bars_by_series.append(rects)

    ax.set_xticks(x, categories)
    ax.set_ylim(0, max([v for sr in series for v in sr.values]) * 1.25)
    ax.grid(True, axis="y", alpha=0.25)
    ax.set_ylabel("Leads")
    ax.set_xlabel("Quarter")


# ----------------- main ------------------------------------------------------

def main(*, save_png: bool = False) -> None:
    cats, sers = make_dataset()

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    grouped_bars(ax, cats, sers, width=0.22, gap=0.12)

    ax.legend(loc="upper left", framealpha=0.85, ncols=3)
    fig.suptitle("Grouped Bars Showcase — Quarterly Leads by Channel", fontsize=13)

    if save_png:
        fig.savefig("grouped_bars_showcase.png", dpi=160, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
