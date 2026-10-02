"""
Unit tests for ChannelAnalytics module.
"""

import pytest
import pandas as pd
from src.analytics import ChannelAnalytics


@pytest.fixture
def clean_sample_df():
    return pd.DataFrame(
        {
            "Channel_ID": [101, 102, 103, 104],
            "Channel_Name": ["Sun TV", "Vijay TV", "Sun TV", "Vijay TV"],
            "Language": ["Tamil", "Tamil", "Tamil", "Tamil"],
            "Channel_Category": ["Entertainment", "Entertainment", "Entertainment", "Entertainment"],
            "Popular_Show": ["Kayal", "Super Singer", "Vanathai Pola", "Bigg Boss"],
            "Show_Category": ["Serial", "Music", "Serial", "Reality"],
            "No_of_Shows": [20, 25, 20, 25],
            "Avg_Viewers": [1000000, 2000000, 1500000, 2500000],
            "Avg_Rating": [4.5, 4.0, 4.2, 4.8],
            "Total_Likes": [100000, 200000, 150000, 250000],
            "Social_Media_Followers": [500000, 1000000, 600000, 1200000],
            "YouTube_Views": [50000000, 80000000, 60000000, 90000000],
            "HD_Available": ["Yes", "Yes", "No", "Yes"],
            "Years_Active": [30, 20, 30, 20],
            "Subscription_Fee": [150.0, 180.0, 150.0, 180.0],
            "Monthly_Reach": [3000000, 5000000, 4000000, 6000000],
        }
    )


def test_overall_kpis(clean_sample_df):
    analytics = ChannelAnalytics(clean_sample_df)
    kpis = analytics.get_overall_kpis()

    assert kpis["total_channels"] == 2
    assert kpis["total_shows"] == 4
    assert kpis["total_records"] == 4
    assert kpis["avg_viewers"] == 1750000.0
    assert kpis["min_rating"] == 4.0
    assert kpis["max_rating"] == 4.8


def test_channel_summary(clean_sample_df):
    analytics = ChannelAnalytics(clean_sample_df)
    summary = analytics.get_channel_summary()

    assert len(summary) == 2
    assert "Power_Index" in summary.columns
    # Vijay TV has higher viewers and metrics, so should have higher power index
    vijay_power = summary.loc[summary["Channel_Name"] == "Vijay TV", "Power_Index"].iloc[0]
    sun_power = summary.loc[summary["Channel_Name"] == "Sun TV", "Power_Index"].iloc[0]
    assert vijay_power >= sun_power
