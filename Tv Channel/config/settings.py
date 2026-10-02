"""
Global settings and configuration for the TV Channel Analytics Pipeline.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = BASE_DIR / "TV_channel_dataset.csv"
if not RAW_DATA_PATH.exists():
    RAW_DATA_PATH = DATA_DIR / "raw" / "TV_channel_dataset.csv"

PROCESSED_DATA_PATH = BASE_DIR / "cleaned_tv_channel_dataset.csv"
PROCESSED_DATA_ALT_PATH = DATA_DIR / "processed" / "cleaned_tv_channel_dataset.csv"

REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Ensure target directories exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)

# Dataset Columns Specification
IDENTIFIER_COLUMNS = ["Channel_ID"]

NUMERIC_COLUMNS = [
    "Avg_Viewers",
    "Avg_Rating",
    "Total_Likes",
    "Social_Media_Followers",
    "YouTube_Views",
    "Monthly_Reach",
    "Subscription_Fee",
    "Years_Active",
    "No_of_Shows",
]

CATEGORICAL_COLUMNS = [
    "Channel_Name",
    "Language",
    "Channel_Category",
    "Popular_Show",
    "Show_Category",
    "HD_Available",
]

# Bounds and Validation Rules
BOUNDS = {
    "Avg_Rating": (0.0, 5.0),
    "Subscription_Fee": (0.0, None),
    "Years_Active": (0, 100),
    "Avg_Viewers": (0, None),
    "Total_Likes": (0, None),
    "Social_Media_Followers": (0, None),
    "YouTube_Views": (0, None),
    "Monthly_Reach": (0, None),
    "No_of_Shows": (0, None),
}

# Standardized Unknown Placeholders
UNKNOWN_PLACEHOLDERS = [
    "NA",
    "N/A",
    "na",
    "n/a",
    "Unknown",
    "unknown",
    "UNKNOWN",
    "None",
    "none",
    "null",
    "NULL",
    "",
    " ",
]

# Canonical Channel Name Normalization Dictionary
CANONICAL_CHANNEL_MAPPING = {
    "suntv": "Sun TV",
    "sun tv": "Sun TV",
    "vijaytv": "Vijay TV",
    "vijay tv": "Vijay TV",
    "vijay  tv": "Vijay TV",
    "zeetamil": "Zee Tamil",
    "zee tamil": "Zee Tamil",
    "colorstamil": "Colors Tamil",
    "colors tamil": "Colors Tamil",
    "ktv": "KTV",
    "raj tv": "Raj TV",
    "jaya tv": "Jaya TV",
    "kalaignar tv": "Kalaignar TV",
    "star sports": "Star Sports",
    "sony sports": "Sony Sports",
}

# Known Channel Metadata Defaults (Language & Category)
CHANNEL_METADATA_FALLBACK = {
    "Sun TV": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "Vijay TV": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "Zee Tamil": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "Colors Tamil": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "KTV": {"Language": "Tamil", "Channel_Category": "Movies"},
    "Kalaignar TV": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "Jaya TV": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "Raj TV": {"Language": "Tamil", "Channel_Category": "Entertainment"},
    "Star Sports": {"Language": "English", "Channel_Category": "Sports"},
    "Sony Sports": {"Language": "English", "Channel_Category": "Sports"},
}

# Visualization Configuration
PLOT_THEME = {
    "figure.figsize": (11, 6),
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
}

PALETTE_PRIMARY = [
    "#2563EB",  # Vibrant Blue
    "#7C3AED",  # Violet
    "#DB2777",  # Pink
    "#EA580C",  # Orange
    "#059669",  # Emerald
    "#0284C7",  # Sky
    "#D97706",  # Amber
    "#4F46E5",  # Indigo
    "#DC2626",  # Red
    "#0D9488",  # Teal
]
