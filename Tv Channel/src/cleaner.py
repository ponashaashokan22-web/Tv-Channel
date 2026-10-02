"""
Data Cleaning and Preprocessing Pipeline for TV Channel Analytics.
Fixes data anomalies, canonicalizes entity names, and applies robust imputation.
"""

from pathlib import Path
from typing import Any, Optional, Tuple
import re
import numpy as np
import pandas as pd

from config.settings import (
    NUMERIC_COLUMNS,
    CATEGORICAL_COLUMNS,
    BOUNDS,
    UNKNOWN_PLACEHOLDERS,
    CANONICAL_CHANNEL_MAPPING,
    CHANNEL_METADATA_FALLBACK,
    PROCESSED_DATA_PATH,
    PROCESSED_DATA_ALT_PATH,
)


class DataCleaner:
    """Robust, reproducible data cleaning pipeline for TV broadcast data."""

    def __init__(self):
        self.mapping = CANONICAL_CHANNEL_MAPPING
        self.metadata_fallback = CHANNEL_METADATA_FALLBACK

    def normalize_channel_name(self, val: Any) -> Optional[str]:
        """Normalizes channel name string and applies canonical entity mapping."""
        if pd.isna(val):
            return np.nan
        s = str(val).strip()
        # Collapse multiple spaces to single space
        s = re.sub(r"\s+", " ", s)
        key = s.lower()
        if key in self.mapping:
            return self.mapping[key]
        if key in [p.lower() for p in UNKNOWN_PLACEHOLDERS]:
            return np.nan
        # Default title-case fallback
        return s.title()

    def clean_text_field(self, val: Any) -> Optional[str]:
        """Standardizes a text column by stripping and removing placeholder values."""
        if pd.isna(val):
            return np.nan
        s = str(val).strip()
        s = re.sub(r"\s+", " ", s)
        if s.lower() in [p.lower() for p in UNKNOWN_PLACEHOLDERS]:
            return np.nan
        return s.title()

    def clean_pipeline(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """
        Executes complete cleaning pipeline:
        1. Replace string placeholders with NaN.
        2. Clean and canonicalize channel and text fields.
        3. Coerce numeric types.
        4. Validate and enforce boundary rules.
        5. Smart group-stratified imputation.
        6. Final validation.
        """
        data = df.copy()
        stats = {
            "initial_rows": len(data),
            "initial_nulls": int(data.isnull().sum().sum()),
        }

        # Step 1: Replace unknown placeholder strings with NaN across all columns
        data = data.replace(UNKNOWN_PLACEHOLDERS, np.nan)

        # Step 2: Canonicalize Channel Name
        if "Channel_Name" in data.columns:
            data["Channel_Name"] = data["Channel_Name"].apply(self.normalize_channel_name)

        # Standardize other categorical fields
        for col in ["Popular_Show", "Show_Category", "Language", "Channel_Category"]:
            if col in data.columns:
                data[col] = data[col].apply(self.clean_text_field)

        # Normalize HD_Available
        if "HD_Available" in data.columns:
            data["HD_Available"] = (
                data["HD_Available"]
                .astype(str)
                .str.strip()
                .str.capitalize()
                .replace({"True": "Yes", "False": "No", "Nan": np.nan})
            )

        # Step 3: Numeric Coercion
        for col in NUMERIC_COLUMNS:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors="coerce")

        # Step 4: Boundary Validation & Anomaly Correction
        invalid_counts = {}
        for col, (low, high) in BOUNDS.items():
            if col in data.columns:
                mask = pd.Series(False, index=data.index)
                if low is not None:
                    mask |= data[col] < low
                if high is not None:
                    mask |= data[col] > high
                invalid_counts[col] = int(mask.sum())
                data.loc[mask, col] = np.nan
        stats["out_of_bounds_nulled"] = invalid_counts

        # Step 5: Deduplication
        initial_count = len(data)
        data = data.drop_duplicates()
        stats["duplicates_removed"] = initial_count - len(data)

        # Step 6: Group-Aware Smart Imputation
        # 6a. Impute Channel_Name mode if missing
        if data["Channel_Name"].isnull().any():
            mode_channel = data["Channel_Name"].mode().iloc[0]
            data["Channel_Name"] = data["Channel_Name"].fillna(mode_channel)

        # 6b. Impute Language and Channel_Category using Channel_Name metadata
        for channel, meta in self.metadata_fallback.items():
            mask = data["Channel_Name"] == channel
            if "Language" in data.columns:
                data.loc[mask & data["Language"].isnull(), "Language"] = meta["Language"]
            if "Channel_Category" in data.columns:
                data.loc[mask & data["Channel_Category"].isnull(), "Channel_Category"] = meta["Channel_Category"]

        # Fallback to column modes for categorical
        for col in CATEGORICAL_COLUMNS:
            if col in data.columns and data[col].isnull().any():
                col_mode = data[col].mode().iloc[0] if len(data[col].mode()) > 0 else "Unknown"
                data[col] = data[col].fillna(col_mode)

        # 6c. Impute Numeric Columns:
        # Hierarchical median imputation: Channel_Name + Show_Category -> Channel_Name -> Global Median
        for col in NUMERIC_COLUMNS:
            if col in data.columns and data[col].isnull().any():
                # Level 1: Channel + Show Category median
                grouped_median_l1 = data.groupby(["Channel_Name", "Show_Category"])[col].transform("median")
                data[col] = data[col].fillna(grouped_median_l1)

                # Level 2: Channel median
                grouped_median_l2 = data.groupby("Channel_Name")[col].transform("median")
                data[col] = data[col].fillna(grouped_median_l2)

                # Level 3: Global median
                global_median = data[col].median()
                data[col] = data[col].fillna(global_median)

        # Round appropriate columns to integers
        int_cols = [
            "Channel_ID",
            "Avg_Viewers",
            "Total_Likes",
            "Social_Media_Followers",
            "YouTube_Views",
            "Monthly_Reach",
            "Years_Active",
            "No_of_Shows",
        ]
        for col in int_cols:
            if col in data.columns:
                data[col] = data[col].round().astype(int)

        stats["final_rows"] = len(data)
        stats["final_nulls"] = int(data.isnull().sum().sum())

        return data, stats

    def save_cleaned(self, df: pd.DataFrame, target_path: Optional[Path] = None) -> Path:
        """Saves cleaned dataset to standard file paths."""
        save_target = Path(target_path) if target_path else PROCESSED_DATA_PATH
        save_target.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_target, index=False)

        # Also save in data/processed for clean project structure
        try:
            PROCESSED_DATA_ALT_PATH.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(PROCESSED_DATA_ALT_PATH, index=False)
        except Exception:
            pass

        return save_target
