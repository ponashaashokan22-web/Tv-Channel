"""
Unit tests for DataCleaner and entity resolution.
"""

import pytest
import pandas as pd
import numpy as np
from src.cleaner import DataCleaner


@pytest.fixture
def sample_raw_df():
    return pd.DataFrame(
        {
            "Channel_ID": [101, 102, 103, 104, 105],
            "Channel_Name": ["suntv", "Vijay  TV", "ZeeTamil", "unknown", "Star Sports"],
            "Language": ["Tamil", "unknown", "Tamil", "English", "NA"],
            "Channel_Category": ["Entertainment", "Entertainment", "Entertainment", "Sports", "Sports"],
            "Popular_Show": ["Kayal", "Super Singer", "Sembaruthi", "unknown", "Cricket"],
            "Show_Category": ["Serial", "Music", "Serial", "News", "Sports"],
            "No_of_Shows": [20, 25, 15, 10, 30],
            "Avg_Viewers": ["1200000", "1500000", np.nan, "800000", "2000000"],
            "Avg_Rating": [4.5, -1.0, 6.2, 3.8, 4.0],  # Invalid ratings: -1.0, 6.2
            "Total_Likes": [100000, 150000, 120000, 90000, 200000],
            "Social_Media_Followers": [500000, 600000, 450000, 300000, 800000],
            "YouTube_Views": [50000000, 60000000, 40000000, 30000000, 70000000],
            "HD_Available": ["Yes", "no", "yes", "NO", "Yes"],
            "Years_Active": [25, 20, 15, -5, 10],  # Invalid year: -5
            "Subscription_Fee": [150.0, -50.0, 200.0, 100.0, 250.0],  # Invalid fee: -50.0
            "Monthly_Reach": [2500000, 3000000, 2000000, 1500000, 4000000],
        }
    )


def test_channel_name_canonicalization():
    cleaner = DataCleaner()
    assert cleaner.normalize_channel_name("suntv") == "Sun TV"
    assert cleaner.normalize_channel_name("Vijay  TV") == "Vijay TV"
    assert cleaner.normalize_channel_name("zeetamil") == "Zee Tamil"
    assert cleaner.normalize_channel_name("colorstamil") == "Colors Tamil"
    assert pd.isna(cleaner.normalize_channel_name("unknown"))
    assert pd.isna(cleaner.normalize_channel_name("NA"))


def test_clean_pipeline(sample_raw_df):
    cleaner = DataCleaner()
    cleaned_df, stats = cleaner.clean_pipeline(sample_raw_df)

    # Check zero nulls remain
    assert cleaned_df.isnull().sum().sum() == 0

    # Check bounds
    assert (cleaned_df["Avg_Rating"] >= 0.0).all()
    assert (cleaned_df["Avg_Rating"] <= 5.0).all()
    assert (cleaned_df["Subscription_Fee"] >= 0.0).all()
    assert (cleaned_df["Years_Active"] >= 0).all()

    # Check channel names canonicalized
    assert "suntv" not in cleaned_df["Channel_Name"].values
    assert "Sun TV" in cleaned_df["Channel_Name"].values
    assert "Vijay TV" in cleaned_df["Channel_Name"].values
    assert "Zee Tamil" in cleaned_df["Channel_Name"].values
