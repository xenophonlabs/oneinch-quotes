import warnings
import pandas as pd
import matplotlib.pyplot as plt

warnings.simplefilter("ignore", UserWarning)

plt.rcParams["font.family"] = "serif"
plt.rcParams.update({"font.size": 10})
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

plt.rcParams["grid.color"] = "white"
plt.rcParams["grid.linestyle"] = "-"
plt.rcParams["grid.linewidth"] = 2

S = 5


def save(fig: plt.Figure, fn: str | None) -> plt.Figure:
    """Save plot."""
    fig.tight_layout()
    if fn:
        plt.savefig(fn, bbox_inches="tight", dpi=300)
        # plt.close()
    return fig


def plot_quotes(
    df: pd.DataFrame, in_token: str, out_token: str, fn: str | None = None
) -> plt.Figure:
    """Plot 1inch quotes for a given token pair."""
    f, ax = plt.subplots(figsize=(10, 5))

    scatter = ax.scatter(
        df["in_amount"], df["price"], s=S, c=df["timestamp"], cmap="viridis"
    )

    ax.set_xscale("log")
    ax.set_title(f"Prices for Swapping {in_token} into {out_token}")
    ax.set_ylabel("Exchange Rate (out/in)")
    ax.set_xlabel(f"Trade Size ({in_token})")

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.ax.set_yticklabels(
        pd.to_datetime(cbar.get_ticks(), unit="s").strftime("%d %b %Y")
    )
    cbar.set_label("Date")

    return save(f, fn)


# pylint: disable=too-many-arguments, too-many-locals
def plot_price_impact(
    df: pd.DataFrame,
    in_token: str,
    out_token: str,
    in_decimals: int,
    fn: str | None = None,
    scale: str = "log",
    xlim: float | None = None,
) -> plt.Figure:
    """
    Plot price impact from 1inch quotes against
    predicted price impact from market model.
    """
    f, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(
        df["in_amount"] / 10**in_decimals,
        df["price_impact"] * 100,
        c=df["timestamp"],
        s=S,
        label="1inch Quotes",
    )

    ax.set_xscale(scale)
    ax.legend()
    ax.set_xlabel(f"Amount in ({in_token})")
    ax.set_ylabel("Price Impact %")
    ax.set_title(f"{in_token} -> {out_token} Price Impact")

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.ax.set_yticklabels(
        pd.to_datetime(cbar.get_ticks(), unit="s").strftime("%d %b %Y")
    )
    cbar.set_label("Date")

    if xlim:
        ax.set_xlim(0, xlim)
        ax.set_ylim(0, df[df["in_amount"] < xlim]["price_impact"].max() * 100)

    return save(f, fn)
