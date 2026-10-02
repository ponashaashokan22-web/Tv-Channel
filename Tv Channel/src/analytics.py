"""
Analytics engine for TV Channel Performance and Viewer Engagement.
Computes KPIs, multi-dimensional aggregations, rankings, and statistical metrics.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


class ChannelAnalytics:
    """Computes advanced aggregations, leaderboards, and KPI summaries."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_overall_kpis(self) -> Dict[str, Any]:
        """Calculates macro-level KPIs across the TV broadcast network."""
        return {
            "total_channels": int(self.df["Channel_Name"].nunique()),
            "total_shows": int(self.df["Popular_Show"].nunique()),
            "total_records": len(self.df),
            "avg_viewers": round(float(self.df["Avg_Viewers"].mean()), 2),
            "median_viewers": round(float(self.df["Avg_Viewers"].median()), 2),
            "avg_rating": round(float(self.df["Avg_Rating"].mean()), 2),
            "min_rating": round(float(self.df["Avg_Rating"].min()), 2),
            "max_rating": round(float(self.df["Avg_Rating"].max()), 2),
            "avg_likes": round(float(self.df["Total_Likes"].mean()), 2),
            "avg_youtube_views": round(float(self.df["YouTube_Views"].mean()), 2),
            "avg_social_followers": round(float(self.df["Social_Media_Followers"].mean()), 2),
            "avg_monthly_reach": round(float(self.df["Monthly_Reach"].mean()), 2),
            "avg_subscription_fee": round(float(self.df["Subscription_Fee"].mean()), 2),
        }

    def get_channel_summary(self) -> pd.DataFrame:
        """
        Calculates channel-level metrics and a normalized Power Score.
        """
        summary = (
            self.df.groupby("Channel_Name")
            .agg(
                Avg_Viewers=("Avg_Viewers", "mean"),
                Avg_Rating=("Avg_Rating", "mean"),
                Total_Likes=("Total_Likes", "mean"),
                YouTube_Views=("YouTube_Views", "mean"),
                Social_Media_Followers=("Social_Media_Followers", "mean"),
                Monthly_Reach=("Monthly_Reach", "mean"),
                Subscription_Fee=("Subscription_Fee", "mean"),
                Record_Count=("Channel_ID", "count"),
            )
            .reset_index()
        )

        # Composite Engagement Score (Min-Max scaled normalized index)
        metric_cols = ["Avg_Viewers", "Avg_Rating", "Total_Likes", "YouTube_Views", "Social_Media_Followers"]
        scaled_metrics = pd.DataFrame()
        for col in metric_cols:
            c_min, c_max = summary[col].min(), summary[col].max()
            if c_max > c_min:
                scaled_metrics[col] = (summary[col] - c_min) / (c_max - c_min)
            else:
                scaled_metrics[col] = 1.0

        summary["Power_Index"] = (
            scaled_metrics["Avg_Viewers"] * 0.35
            + scaled_metrics["Avg_Rating"] * 0.25
            + scaled_metrics["Total_Likes"] * 0.15
            + scaled_metrics["YouTube_Views"] * 0.15
            + scaled_metrics["Social_Media_Followers"] * 0.10
        ) * 100
        summary["Power_Index"] = summary["Power_Index"].round(2)

        return summary.sort_values(by="Avg_Viewers", ascending=False)

    def get_category_summary(self) -> pd.DataFrame:
        """Calculates viewership and engagement aggregations by Show Category."""
        summary = (
            self.df.groupby("Show_Category")
            .agg(
                Avg_Viewers=("Avg_Viewers", "mean"),
                Avg_Rating=("Avg_Rating", "mean"),
                Total_Likes=("Total_Likes", "mean"),
                YouTube_Views=("YouTube_Views", "mean"),
                Monthly_Reach=("Monthly_Reach", "mean"),
                Total_Episodes_Count=("Channel_ID", "count"),
            )
            .reset_index()
            .sort_values(by="Avg_Viewers", ascending=False)
        )
        return summary

    def get_channel_category_summary(self) -> pd.DataFrame:
        """Calculates aggregations by Channel Category (Entertainment, Movies, Sports)."""
        summary = (
            self.df.groupby("Channel_Category")
            .agg(
                Avg_Viewers=("Avg_Viewers", "mean"),
                Avg_Rating=("Avg_Rating", "mean"),
                Total_Likes=("Total_Likes", "mean"),
                YouTube_Views=("YouTube_Views", "mean"),
                Total_Shows=("No_of_Shows", "sum"),
                Record_Count=("Channel_ID", "count"),
            )
            .reset_index()
            .sort_values(by="Avg_Viewers", ascending=False)
        )
        return summary

    def get_hd_comparison(self) -> pd.DataFrame:
        """Compares performance between HD and Standard Definition broadcast shows."""
        return (
            self.df.groupby("HD_Available")
            .agg(
                Avg_Viewers=("Avg_Viewers", "mean"),
                Avg_Rating=("Avg_Rating", "mean"),
                Total_Likes=("Total_Likes", "mean"),
                YouTube_Views=("YouTube_Views", "mean"),
                Total_Broadcasts=("Channel_ID", "count"),
            )
            .reset_index()
        )

    def get_language_comparison(self) -> pd.DataFrame:
        """Compares performance metrics across languages."""
        return (
            self.df.groupby("Language")
            .agg(
                Avg_Viewers=("Avg_Viewers", "mean"),
                Avg_Rating=("Avg_Rating", "mean"),
                Total_Likes=("Total_Likes", "mean"),
                YouTube_Views=("YouTube_Views", "mean"),
                Broadcast_Count=("Channel_ID", "count"),
            )
            .reset_index()
            .sort_values(by="Avg_Viewers", ascending=False)
        )

    def get_top_leaderboards(self, top_n: int = 10) -> Dict[str, pd.DataFrame]:
        """Returns top N leaderboards across key metrics."""
        cols = ["Channel_Name", "Popular_Show", "Show_Category"]
        return {
            "top_viewers": self.df.nlargest(top_n, "Avg_Viewers")[cols + ["Avg_Viewers"]],
            "top_rated": self.df.nlargest(top_n, "Avg_Rating")[cols + ["Avg_Rating"]],
            "top_likes": self.df.nlargest(top_n, "Total_Likes")[cols + ["Total_Likes"]],
            "top_youtube": self.df.nlargest(top_n, "YouTube_Views")[cols + ["YouTube_Views"]],
            "top_social_followers": self.df.nlargest(top_n, "Social_Media_Followers")[
                cols + ["Social_Media_Followers"]
            ],
            "top_monthly_reach": self.df.nlargest(top_n, "Monthly_Reach")[cols + ["Monthly_Reach"]],
        }

    def get_channel_signature_shows(self) -> Dict[str, pd.DataFrame]:
        """Identifies the flagship (most viewed, highest rated, most liked) show for each channel."""
        most_viewed = self.df.loc[self.df.groupby("Channel_Name")["Avg_Viewers"].idxmax()][
            ["Channel_Name", "Popular_Show", "Show_Category", "Avg_Viewers"]
        ].sort_values(by="Avg_Viewers", ascending=False)

        highest_rated = self.df.loc[self.df.groupby("Channel_Name")["Avg_Rating"].idxmax()][
            ["Channel_Name", "Popular_Show", "Show_Category", "Avg_Rating"]
        ].sort_values(by="Avg_Rating", ascending=False)

        most_liked = self.df.loc[self.df.groupby("Channel_Name")["Total_Likes"].idxmax()][
            ["Channel_Name", "Popular_Show", "Show_Category", "Total_Likes"]
        ].sort_values(by="Total_Likes", ascending=False)

        return {
            "most_viewed": most_viewed,
            "highest_rated": highest_rated,
            "most_liked": most_liked,
        }

    def get_correlation_matrix(self) -> pd.DataFrame:
        """Computes Pearson correlation coefficients across numerical attributes."""
        numeric_cols = [
            "Avg_Viewers",
            "Avg_Rating",
            "Total_Likes",
            "Social_Media_Followers",
            "YouTube_Views",
            "Monthly_Reach",
            "Subscription_Fee",
            "Years_Active",
        ]
        return self.df[numeric_cols].corr()
