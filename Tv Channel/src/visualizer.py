"""
Visualization module for generating publication-quality figures and plots.
"""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd

from config.settings import FIGURES_DIR, PLOT_THEME, PALETTE_PRIMARY


class ChannelVisualizer:
    """Generates and saves publication-ready figures for TV Channel Analytics."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else FIGURES_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._apply_style()

    def _apply_style(self):
        """Applies clean, modern Matplotlib and Seaborn styling."""
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
        plt.rcParams.update(PLOT_THEME)
        sns.set_palette(PALETTE_PRIMARY)

    def _format_millions(self, x, pos):
        """Formats numbers in millions (M) or thousands (K)."""
        if abs(x) >= 1e6:
            return f"{x*1e-6:.1f}M"
        elif abs(x) >= 1e3:
            return f"{x*1e-3:.0f}K"
        return f"{x:.0f}"

    def plot_viewers_by_channel(self, channel_summary: pd.DataFrame) -> Path:
        """Bar plot: Average Viewers by Channel."""
        fig, ax = plt.subplots(figsize=(11, 5.5))
        data = channel_summary.sort_values(by="Avg_Viewers", ascending=False)
        bars = ax.bar(data["Channel_Name"], data["Avg_Viewers"], color="#2563EB", edgecolor="#1D4ED8", alpha=0.85)

        ax.set_title("Average Viewership by TV Channel", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Channel Name", fontsize=11, fontweight="semibold")
        ax.set_ylabel("Average Viewers", fontsize=11, fontweight="semibold")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_millions))
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()

        out_path = self.output_dir / "01_viewers_by_channel.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def plot_ratings_by_channel(self, channel_summary: pd.DataFrame) -> Path:
        """Bar plot: Average Rating by Channel."""
        fig, ax = plt.subplots(figsize=(11, 5.5))
        data = channel_summary.sort_values(by="Avg_Rating", ascending=False)
        bars = ax.bar(data["Channel_Name"], data["Avg_Rating"], color="#7C3AED", edgecolor="#6D28D9", alpha=0.85)

        ax.set_title("Average Content Rating by TV Channel (1-5 Scale)", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Channel Name", fontsize=11, fontweight="semibold")
        ax.set_ylabel("Average Rating", fontsize=11, fontweight="semibold")
        ax.set_ylim(0, 5.2)
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()

        out_path = self.output_dir / "02_ratings_by_channel.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def plot_digital_engagement(self, channel_summary: pd.DataFrame) -> Path:
        """Grouped Bar plot: YouTube Views & Social Media Followers by Channel."""
        fig, ax1 = plt.subplots(figsize=(12, 6))
        data = channel_summary.sort_values(by="YouTube_Views", ascending=False)

        x = range(len(data))
        width = 0.38

        rects1 = ax1.bar(
            [i - width / 2 for i in x],
            data["YouTube_Views"],
            width,
            label="YouTube Views",
            color="#DC2626",
            alpha=0.85,
        )
        rects2 = ax1.bar(
            [i + width / 2 for i in x],
            data["Social_Media_Followers"],
            width,
            label="Social Media Followers",
            color="#0284C7",
            alpha=0.85,
        )

        ax1.set_title("Digital Footprint: YouTube Views vs Social Followers", fontsize=14, fontweight="bold", pad=15)
        ax1.set_xlabel("Channel Name", fontsize=11, fontweight="semibold")
        ax1.set_ylabel("Count", fontsize=11, fontweight="semibold")
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(data["Channel_Name"], rotation=35, ha="right")
        ax1.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_millions))
        ax1.legend(loc="upper right")
        plt.tight_layout()

        out_path = self.output_dir / "03_digital_engagement.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def plot_viewers_by_category(self, category_summary: pd.DataFrame) -> Path:
        """Bar plot: Average Viewers by Show Category."""
        fig, ax = plt.subplots(figsize=(10, 5))
        data = category_summary.sort_values(by="Avg_Viewers", ascending=False)
        ax.barh(data["Show_Category"], data["Avg_Viewers"], color="#059669", edgecolor="#047857", alpha=0.85)

        ax.set_title("Average Viewership by Show Category", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Average Viewers", fontsize=11, fontweight="semibold")
        ax.set_ylabel("Show Category", fontsize=11, fontweight="semibold")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self._format_millions))
        ax.invert_yaxis()
        plt.tight_layout()

        out_path = self.output_dir / "04_viewers_by_show_category.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def plot_distributions(self, df: pd.DataFrame) -> Path:
        """Dual distribution plot: Histograms with KDE for Viewers and Ratings."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Viewers distribution
        sns.histplot(df["Avg_Viewers"], bins=30, kde=True, color="#2563EB", ax=axes[0])
        axes[0].set_title("Distribution of Average Viewers", fontsize=12, fontweight="bold")
        axes[0].set_xlabel("Average Viewers")
        axes[0].set_ylabel("Frequency")
        axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(self._format_millions))

        # Ratings distribution
        sns.histplot(df["Avg_Rating"], bins=20, kde=True, color="#7C3AED", ax=axes[1])
        axes[1].set_title("Distribution of Average Ratings", fontsize=12, fontweight="bold")
        axes[1].set_xlabel("Average Rating (0-5)")
        axes[1].set_ylabel("Frequency")

        plt.tight_layout()
        out_path = self.output_dir / "05_distributions.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def plot_channel_market_share(self, df: pd.DataFrame) -> Path:
        """Donut chart: Channel Share of Total Shows."""
        fig, ax = plt.subplots(figsize=(8, 8))
        counts = df["Channel_Name"].value_counts()

        wedges, texts, autotexts = ax.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%",
            pctdistance=0.75,
            colors=sns.color_palette("tab10", len(counts)),
            wedgeprops=dict(width=0.4, edgecolor="w", linewidth=2),
        )
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")

        ax.set_title("Broadcast Share by Channel", fontsize=14, fontweight="bold", pad=15)
        plt.tight_layout()

        out_path = self.output_dir / "06_channel_market_share.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def plot_correlation_heatmap(self, corr_df: pd.DataFrame) -> Path:
        """Correlation heatmap across all key broadcast and engagement variables."""
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr_df,
            annot=True,
            fmt=".2f",
            cmap="Blues",
            cbar=True,
            linewidths=0.5,
            ax=ax,
            square=True,
        )
        ax.set_title("Engagement & Performance Metric Correlation Matrix", fontsize=14, fontweight="bold", pad=15)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        out_path = self.output_dir / "07_correlation_heatmap.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        return out_path

    def generate_all_plots(self, df: pd.DataFrame, analytics) -> list:
        """Generates the full suite of figures and returns list of paths."""
        ch_summary = analytics.get_channel_summary()
        cat_summary = analytics.get_category_summary()
        corr_matrix = analytics.get_correlation_matrix()

        saved_figures = [
            self.plot_viewers_by_channel(ch_summary),
            self.plot_ratings_by_channel(ch_summary),
            self.plot_digital_engagement(ch_summary),
            self.plot_viewers_by_category(cat_summary),
            self.plot_distributions(df),
            self.plot_channel_market_share(df),
            self.plot_correlation_heatmap(corr_matrix),
        ]
        return saved_figures
