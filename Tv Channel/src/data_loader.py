"""
Data Loading and Validation Module for TV Channel Analytics.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

from config.settings import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    NUMERIC_COLUMNS,
    CATEGORICAL_COLUMNS,
    IDENTIFIER_COLUMNS,
)


class DataLoader:
    """Handles loading, file validation, and initial schema inspection."""

    def __init__(self, raw_path: Optional[Path] = None, processed_path: Optional[Path] = None):
        self.raw_path = Path(raw_path) if raw_path else RAW_DATA_PATH
        self.processed_path = Path(processed_path) if processed_path else PROCESSED_DATA_PATH

    def load_raw(self) -> pd.DataFrame:
        """Loads the raw TV channel dataset with integrity checks."""
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw data file not found at: {self.raw_path.resolve()}")
        
        df = pd.read_csv(self.raw_path)
        return df

    def load_processed(self) -> pd.DataFrame:
        """Loads the cleaned/processed TV channel dataset."""
        if not self.processed_path.exists():
            raise FileNotFoundError(
                f"Processed data file not found at: {self.processed_path.resolve()}. "
                "Please run data cleaning first."
            )
        
        df = pd.read_csv(self.processed_path)
        return df

    def inspect_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Produces comprehensive inspection metrics for a dataset.
        """
        all_expected_cols = IDENTIFIER_COLUMNS + NUMERIC_COLUMNS + CATEGORICAL_COLUMNS
        missing_expected = [c for c in all_expected_cols if c not in df.columns]

        inspection = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "missing_expected_columns": missing_expected,
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
            "numeric_summary": df.describe().to_dict(),
        }
        return inspection
