"""
Command Line Interface (CLI) for TV Channel Analytics Pipeline.
Usage:
    python main.py --all
    python main.py --clean
    python main.py --analyze
    python main.py --visualize
    python main.py --report
    python main.py --dashboard
"""

import argparse
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import DataLoader
from src.cleaner import DataCleaner
from src.analytics import ChannelAnalytics
from src.visualizer import ChannelVisualizer
from src.report_generator import ReportGenerator
from config.settings import RAW_DATA_PATH, PROCESSED_DATA_PATH


def run_clean():
    """Runs the complete data cleaning and entity canonicalization pipeline."""
    print("=" * 60)
    print("--> [1/4] Running Data Cleaning Pipeline...")
    print("=" * 60)
    loader = DataLoader(raw_path=RAW_DATA_PATH)
    raw_df = loader.load_raw()
    print(f"Loaded raw dataset from: {RAW_DATA_PATH} ({len(raw_df):,} rows)")

    cleaner = DataCleaner()
    cleaned_df, stats = cleaner.clean_pipeline(raw_df)
    saved_path = cleaner.save_cleaned(cleaned_df)

    print("Cleaning complete!")
    print(f" - Out of bounds nulled: {stats.get('out_of_bounds_nulled')}")
    print(f" - Duplicates removed: {stats.get('duplicates_removed')}")
    print(f" - Final records: {stats.get('final_rows'):,}")
    print(f" - Remaining null values: {stats.get('final_nulls')}")
    print(f" - Saved cleaned data to: {saved_path}")
    return cleaned_df, stats


def run_analyze(df=None):
    """Executes the analytics calculations and prints KPI summary."""
    print("\n" + "=" * 60)
    print("--> [2/4] Running Analytics Engine...")
    print("=" * 60)
    if df is None:
        loader = DataLoader(processed_path=PROCESSED_DATA_PATH)
        df = loader.load_processed()

    analytics = ChannelAnalytics(df)
    kpis = analytics.get_overall_kpis()
    print("Network Summary KPIs:")
    for k, v in kpis.items():
        print(f"  * {k}: {v}")

    ch_summary = analytics.get_channel_summary()
    print("\nTop 5 Channels by Average Viewers:")
    print(ch_summary[["Channel_Name", "Avg_Viewers", "Avg_Rating", "Power_Index"]].head(5).to_string(index=False))

    return analytics, kpis, ch_summary


def run_visualize(df=None, analytics=None):
    """Generates and exports all publication figures."""
    print("\n" + "=" * 60)
    print("--> [3/4] Generating Publication Figures...")
    print("=" * 60)
    if df is None:
        loader = DataLoader(processed_path=PROCESSED_DATA_PATH)
        df = loader.load_processed()
    if analytics is None:
        analytics = ChannelAnalytics(df)

    visualizer = ChannelVisualizer()
    figures = visualizer.generate_all_plots(df, analytics)
    print(f"Successfully generated {len(figures)} figures in {visualizer.output_dir}:")
    for fig_path in figures:
        print(f"  [+] {fig_path.name}")
    return visualizer, figures


def run_report(df=None, analytics=None, stats=None):
    """Generates the executive markdown report."""
    print("\n" + "=" * 60)
    print("--> [4/4] Generating Executive Performance Report...")
    print("=" * 60)
    if df is None:
        loader = DataLoader(processed_path=PROCESSED_DATA_PATH)
        df = loader.load_processed()
    if analytics is None:
        analytics = ChannelAnalytics(df)
    if stats is None:
        stats = {
            "initial_rows": len(df),
            "final_rows": len(df),
            "duplicates_removed": 0,
            "out_of_bounds_nulled": {},
            "final_nulls": int(df.isnull().sum().sum()),
        }

    kpis = analytics.get_overall_kpis()
    ch_summary = analytics.get_channel_summary()
    cat_summary = analytics.get_category_summary()
    sig_shows = analytics.get_channel_signature_shows()
    hd_comp = analytics.get_hd_comparison()

    generator = ReportGenerator()
    report_file = generator.generate_markdown_report(
        kpis=kpis,
        cleaning_stats=stats,
        channel_summary=ch_summary,
        category_summary=cat_summary,
        signature_shows=sig_shows,
        hd_comparison=hd_comp,
    )
    print(f"Executive report generated at: {report_file}")
    return report_file


def run_dashboard():
    """Launches the Streamlit interactive dashboard."""
    print("\n--> Launching Streamlit Dashboard at http://localhost:8501 ...")
    app_path = PROJECT_ROOT / "app" / "dashboard.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])


def main():
    parser = argparse.ArgumentParser(description="TV Channel Analytics Pipeline Runner")
    parser.add_argument("--all", action="store_true", help="Run full pipeline: clean, analyze, visualize, report")
    parser.add_argument("--clean", action="store_true", help="Run data cleaning & entity resolution")
    parser.add_argument("--analyze", action="store_true", help="Run analytics & print KPIs")
    parser.add_argument("--visualize", action="store_true", help="Generate all plots")
    parser.add_argument("--report", action="store_true", help="Generate executive markdown report")
    parser.add_argument("--dashboard", action="store_true", help="Launch interactive Streamlit dashboard")

    args = parser.parse_args()

    # If no flags passed, default to --all
    if not any([args.all, args.clean, args.analyze, args.visualize, args.report, args.dashboard]):
        args.all = True

    cleaned_df = None
    stats = None
    analytics = None

    if args.all or args.clean:
        cleaned_df, stats = run_clean()

    if args.all or args.analyze:
        analytics, kpis, ch_summary = run_analyze(df=cleaned_df)

    if args.all or args.visualize:
        run_visualize(df=cleaned_df, analytics=analytics)

    if args.all or args.report:
        run_report(df=cleaned_df, analytics=analytics, stats=stats)

    if args.dashboard:
        run_dashboard()

    print("\n[SUCCESS] Pipeline execution completed successfully!")


if __name__ == "__main__":
    main()
