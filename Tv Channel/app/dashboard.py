"""
Streamlit Web Dashboard for TV Channel Broadcasting & Engagement Analytics.
Run locally with: streamlit run app/dashboard.py
"""

import sys
from pathlib import Path

# Add project root to sys.path so config and src can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import PROCESSED_DATA_PATH, RAW_DATA_PATH
from src.cleaner import DataCleaner

st.set_page_config(
    page_title="TV Channel Analytics Hub",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern visual polish
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #0f172a;
        font-size: 1.75rem;
        font-weight: 700;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """Loads cleaned dataset, or cleans raw dataset if cleaned does not exist."""
    if PROCESSED_DATA_PATH.exists():
        df = pd.read_csv(PROCESSED_DATA_PATH)
    else:
        df_raw = pd.read_csv(RAW_DATA_PATH)
        cleaner = DataCleaner()
        df, _ = cleaner.clean_pipeline(df_raw)
        cleaner.save_cleaned(df)
    return df


df = load_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.title("📺 Filter Controls")
st.sidebar.markdown("Customize view by channel, genre, or quality.")

all_channels = sorted(df["Channel_Name"].dropna().unique().tolist())
selected_channels = st.sidebar.multiselect(
    "Select TV Channels",
    options=all_channels,
    default=all_channels,
)

all_categories = sorted(df["Show_Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select Show Categories",
    options=all_categories,
    default=all_categories,
)

hd_options = ["All"] + sorted(df["HD_Available"].dropna().unique().tolist())
selected_hd = st.sidebar.selectbox("HD Broadcast", options=hd_options, index=0)

min_rating = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)

# Apply Filters
filtered_df = df[
    (df["Channel_Name"].isin(selected_channels))
    & (df["Show_Category"].isin(selected_categories))
    & (df["Avg_Rating"] >= min_rating)
]
if selected_hd != "All":
    filtered_df = filtered_df[filtered_df["HD_Available"] == selected_hd]

# ----------------- MAIN HEADER -----------------
st.title("📺 TV Channel Broadcasting & Engagement Analytics")
st.markdown(
    "Comprehensive executive intelligence platform analyzing viewership metrics, content ratings, "
    "digital footprint across YouTube and Social Media, and show category performance."
)

# ----------------- KPI SUMMARY ROW -----------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Active Channels</div>
            <div class="metric-value">{filtered_df['Channel_Name'].nunique()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg Viewership</div>
            <div class="metric-value">{filtered_df['Avg_Viewers'].mean() / 1e6:.2f}M</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg Rating</div>
            <div class="metric-value">{filtered_df['Avg_Rating'].mean():.2f} / 5.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg YouTube Views</div>
            <div class="metric-value">{filtered_df['YouTube_Views'].mean() / 1e6:.1f}M</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Avg Monthly Reach</div>
            <div class="metric-value">{filtered_df['Monthly_Reach'].mean() / 1e6:.1f}M</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ----------------- TABS SECTION -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview & Rankings",
    "🏢 Channel Comparison",
    "🎭 Genre & Content",
    "📱 Digital Footprint",
    "📋 Data Explorer",
])

# ----- TAB 1: Overview & Rankings -----
with tab1:
    st.subheader("TV Channel Performance Overview")
    ch_agg = (
        filtered_df.groupby("Channel_Name")
        .agg(
            Avg_Viewers=("Avg_Viewers", "mean"),
            Avg_Rating=("Avg_Rating", "mean"),
            Total_Likes=("Total_Likes", "mean"),
            YouTube_Views=("YouTube_Views", "mean"),
            Monthly_Reach=("Monthly_Reach", "mean"),
            Broadcasts=("Channel_ID", "count"),
        )
        .reset_index()
        .sort_values(by="Avg_Viewers", ascending=False)
    )

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("**Average Viewership by Channel**")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(ch_agg["Channel_Name"], ch_agg["Avg_Viewers"] / 1e6, color="#2563EB", alpha=0.85)
        ax.set_ylabel("Viewers (Millions)")
        plt.xticks(rotation=40, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with c2:
        st.markdown("**Catalog Share by Channel**")
        fig, ax = plt.subplots(figsize=(6, 4.5))
        counts = filtered_df["Channel_Name"].value_counts()
        ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=sns.color_palette("tab10", len(counts)))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("### Channel Summary Metrics")
    display_df = ch_agg.copy()
    display_df["Avg_Viewers"] = display_df["Avg_Viewers"].apply(lambda x: f"{x/1e6:.2f}M")
    display_df["Avg_Rating"] = display_df["Avg_Rating"].apply(lambda x: f"{x:.2f}")
    display_df["Total_Likes"] = display_df["Total_Likes"].apply(lambda x: f"{x/1e3:.1f}K")
    display_df["YouTube_Views"] = display_df["YouTube_Views"].apply(lambda x: f"{x/1e6:.2f}M")
    display_df["Monthly_Reach"] = display_df["Monthly_Reach"].apply(lambda x: f"{x/1e6:.2f}M")
    st.dataframe(display_df, width="stretch")

# ----- TAB 2: Channel Comparison -----
with tab2:
    st.subheader("Deep-Dive Channel Analysis")
    selected_channel = st.selectbox("Select Channel for Detailed Profiling", options=all_channels)
    ch_data = df[df["Channel_Name"] == selected_channel]

    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.markdown(f"#### Profile: **{selected_channel}**")
        st.write(f"- **Language**: {ch_data['Language'].iloc[0]}")
        st.write(f"- **Primary Category**: {ch_data['Channel_Category'].iloc[0]}")
        st.write(f"- **Years Active**: {int(ch_data['Years_Active'].iloc[0])} years")
        st.write(f"- **Monthly Subscription**: ₹{ch_data['Subscription_Fee'].iloc[0]:.2f}")
        st.write(f"- **Total Cataloged Records**: {len(ch_data):,}")
        st.write(f"- **Average Show Rating**: {ch_data['Avg_Rating'].mean():.2f}")

    with c_right:
        st.markdown(f"#### Top Shows on {selected_channel}")
        top_shows = (
            ch_data.groupby("Popular_Show")
            .agg(
                Avg_Viewers=("Avg_Viewers", "mean"),
                Avg_Rating=("Avg_Rating", "mean"),
                Show_Category=("Show_Category", "first"),
            )
            .reset_index()
            .sort_values(by="Avg_Viewers", ascending=False)
            .head(5)
        )
        top_shows["Avg_Viewers"] = top_shows["Avg_Viewers"].apply(lambda x: f"{x/1e6:.2f}M")
        top_shows["Avg_Rating"] = top_shows["Avg_Rating"].apply(lambda x: f"{x:.2f}")
        st.table(top_shows)

# ----- TAB 3: Genre & Content -----
with tab3:
    st.subheader("Genre & Content Category Performance")
    cat_agg = (
        filtered_df.groupby("Show_Category")
        .agg(
            Avg_Viewers=("Avg_Viewers", "mean"),
            Avg_Rating=("Avg_Rating", "mean"),
            Total_Likes=("Total_Likes", "mean"),
            YouTube_Views=("YouTube_Views", "mean"),
        )
        .reset_index()
        .sort_values(by="Avg_Viewers", ascending=False)
    )

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**Viewership by Show Category**")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.barh(cat_agg["Show_Category"], cat_agg["Avg_Viewers"] / 1e6, color="#059669")
        ax.set_xlabel("Average Viewers (Millions)")
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with g2:
        st.markdown("**Average Rating by Show Category**")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.barh(cat_agg["Show_Category"], cat_agg["Avg_Rating"], color="#7C3AED")
        ax.set_xlabel("Average Rating (0-5)")
        ax.set_xlim(0, 5.2)
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ----- TAB 4: Digital Footprint -----
with tab4:
    st.subheader("Digital Footprint & Correlation Analysis")
    d1, d2 = st.columns([3, 2])
    with d1:
        st.markdown("**YouTube Views vs. Social Media Followers**")
        ch_dig = filtered_df.groupby("Channel_Name")[["YouTube_Views", "Social_Media_Followers"]].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(
            ch_dig["Social_Media_Followers"] / 1e6,
            ch_dig["YouTube_Views"] / 1e6,
            s=180,
            color="#DC2626",
            alpha=0.8,
            edgecolors="black",
        )
        for _, row in ch_dig.iterrows():
            ax.annotate(
                row["Channel_Name"],
                (row["Social_Media_Followers"] / 1e6 + 0.05, row["YouTube_Views"] / 1e6 + 0.5),
                fontsize=9,
            )
        ax.set_xlabel("Social Media Followers (Millions)")
        ax.set_ylabel("YouTube Views (Millions)")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with d2:
        st.markdown("**Metric Correlation Heatmap**")
        corr_cols = ["Avg_Viewers", "Avg_Rating", "Total_Likes", "YouTube_Views", "Social_Media_Followers", "Monthly_Reach"]
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(filtered_df[corr_cols].corr(), annot=True, fmt=".2f", cmap="Blues", ax=ax, cbar=False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ----- TAB 5: Data Explorer -----
with tab5:
    st.subheader("Cleaned Dataset Explorer")
    st.write(f"Showing **{len(filtered_df):,}** records matching current filters.")

    search_query = st.text_input("🔍 Search by Show Name or Channel", "")
    table_view = filtered_df
    if search_query:
        mask = (
            table_view["Popular_Show"].astype(str).str.contains(search_query, case=False, na=False)
            | table_view["Channel_Name"].astype(str).str.contains(search_query, case=False, na=False)
        )
        table_view = table_view[mask]

    st.dataframe(table_view.head(100), width="stretch")

    csv_data = table_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="tv_channel_filtered_data.csv",
        mime="text/csv",
    )
