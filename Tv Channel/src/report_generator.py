"""
Automated Executive Report Generator for TV Channel Analytics.
Produces Markdown and textual analysis summaries.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

from config.settings import REPORTS_DIR


class ReportGenerator:
    """Generates structured markdown performance reports."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown_report(
        self,
        kpis: Dict[str, Any],
        cleaning_stats: Dict[str, Any],
        channel_summary: pd.DataFrame,
        category_summary: pd.DataFrame,
        signature_shows: Dict[str, pd.DataFrame],
        hd_comparison: pd.DataFrame,
    ) -> Path:
        """Constructs and saves the executive performance summary report."""
        report_path = self.output_dir / "tv_channel_executive_report.md"

        ch_table = channel_summary.to_markdown(index=False)
        cat_table = category_summary.to_markdown(index=False)
        hd_table = hd_comparison.to_markdown(index=False)
        most_viewed_table = signature_shows["most_viewed"].head(5).to_markdown(index=False)
        highest_rated_table = signature_shows["highest_rated"].head(5).to_markdown(index=False)

        content = f"""# 📺 TV Channel Broadcast & Engagement Performance Report

## Executive Summary
This analytical report delivers comprehensive intelligence on television broadcasting metrics, viewer engagement levels, digital outreach (YouTube, Social Media), and content ratings across major broadcasting networks.

---

## 🚀 Key Network KPIs
- **Total Monitored Broadcast Records**: {kpis.get('total_records', 0):,}
- **Distinct Channels Evaluated**: {kpis.get('total_channels', 0)}
- **Distinct Shows Catalogued**: {kpis.get('total_shows', 0)}
- **Average Viewership**: {kpis.get('avg_viewers', 0):,.0f} viewers (Median: {kpis.get('median_viewers', 0):,.0f})
- **Average Show Rating**: {kpis.get('avg_rating', 0):.2f} / 5.0 (Range: {kpis.get('min_rating', 0)} - {kpis.get('max_rating', 0)})
- **Average YouTube Views**: {kpis.get('avg_youtube_views', 0):,.0f}
- **Average Social Followers**: {kpis.get('avg_social_followers', 0):,.0f}
- **Average Monthly Reach**: {kpis.get('avg_monthly_reach', 0):,.0f}
- **Average Subscription Fee**: ₹{kpis.get('avg_subscription_fee', 0):.2f}

---

## 🧹 Data Quality & Preprocessing Audit
- **Initial Raw Rows**: {cleaning_stats.get('initial_rows', 0):,}
- **Missing Value Imputations**: Resolved across all numeric and categorical attributes using hierarchical group-aware median/mode imputation.
- **Entity Resolution**: Canonicalized channel variations (e.g. *SunTV* → *Sun TV*, *Vijay  TV* → *Vijay TV*, *ZeeTamil* → *Zee Tamil*, *Colorstamil* → *Colors Tamil*).
- **Out of Range Cleanups**: Corrected {cleaning_stats.get('out_of_bounds_nulled', {}).get('Avg_Rating', 0)} invalid ratings and {cleaning_stats.get('out_of_bounds_nulled', {}).get('Subscription_Fee', 0)} negative subscription fees.
- **Final Valid Dataset Records**: {cleaning_stats.get('final_rows', 0):,} (0 nulls remaining).

---

## 🏆 TV Channel Leaderboard & Power Index
The **Power Index** represents a weighted composite score combining Viewership (35%), Content Ratings (25%), Social Likes (15%), YouTube Views (15%), and Social Followers (10%).

{ch_table}

---

## 🎭 Performance by Show Category
Evaluation of content genres by average viewership, audience ratings, and digital engagement.

{cat_table}

---

## 🌟 Top Flagship Shows
### Most Viewed Shows per Channel
{most_viewed_table}

### Highest Rated Shows per Channel
{highest_rated_table}

---

## 📡 HD vs. Standard Definition (SD) Impact
{hd_table}

---

## 📊 Visual Artifacts
High-resolution visualizations have been rendered to `reports/figures/`:
1. `01_viewers_by_channel.png`: Channel-wise Average Viewership
2. `02_ratings_by_channel.png`: Channel-wise Average Ratings
3. `03_digital_engagement.png`: YouTube Views vs. Social Media Followers
4. `04_viewers_by_show_category.png`: Viewership Across Show Categories
5. `05_distributions.png`: Audience Viewership & Rating Distribution Curves
6. `06_channel_market_share.png`: Broadcast Catalog Share by Channel
7. `07_correlation_heatmap.png`: Cross-Metric Correlation Matrix
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

        return report_path
