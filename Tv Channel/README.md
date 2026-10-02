# 📺 TV Channel Broadcasting & Audience Engagement Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Pytest-Passed-success.svg)](https://docs.pytest.org/)

A production-grade television broadcasting and digital engagement intelligence platform. Refactored from exploratory Jupyter notebooks into a modular, test-driven, object-oriented software architecture with automated reporting, data cleaning pipelines, publication figures, and an interactive Streamlit dashboard.

---

## 📑 Table of Contents
- [1. In-Depth Analysis of Existing Code (`channel.ipynb`)](#1-in-depth-analysis-of-existing-code-channelipynb)
  - [Critical Bugs & Flaws in the Notebook](#critical-bugs--flaws-in-the-notebook)
  - [Data Quality Anomaly Discoveries](#data-quality-anomaly-discoveries)
- [2. Production Architecture & Directory Structure](#2-production-architecture--directory-structure)
- [3. Local Setup & Running Commands](#3-local-setup--running-commands)
  - [Step 1: Environment Setup](#step-1-environment-setup)
  - [Step 2: Install Dependencies](#step-2-install-dependencies)
  - [Step 3: Run the Complete Pipeline](#step-3-run-the-complete-pipeline)
  - [Step 4: Launch Interactive Streamlit Dashboard](#step-4-launch-interactive-streamlit-dashboard)
  - [Step 5: Run Automated Unit Tests](#step-5-run-automated-unit-tests)
- [4. CLI Options & Modular Execution](#4-cli-options--modular-execution)
- [5. Executive Insights & KPIs](#5-executive-insights--kpis)

---

## 1. In-Depth Analysis of Existing Code (`channel.ipynb`)

The original project consisted of a single 92-cell Jupyter notebook (`channel.ipynb`) performing linear data exploration on `TV_channel_dataset.csv` (60,249 rows, 16 features).

### Critical Bugs & Flaws in the Notebook:
1. **Execution-Order Imputation Bug (Cell 27 vs Cell 32)**:
   - In **Cell 27**, missing values were imputed via `fillna(median)` and `fillna(mode)`.
   - In **Cell 32**, string placeholders `['NA', 'N/A', 'Unknown', 'unknown', '']` were replaced with `np.nan`.
   - **Consequence**: Because string placeholders were replaced *after* the imputation step, the resulting output dataset (`cleaned_tv_channel_dataset.csv`) **still contained 82 missing values** (35 missing `Channel_Name`, 25 missing `Language`, 22 missing `Popular_Show`).
2. **Channel Entity Fragmentation**:
   - The notebook attempted normalization with `df['Channel_Name'] = df['Channel_Name'].str.strip().str.title()`.
   - This failed to resolve unspaced names (`SunTV` vs `Sun TV`, `VijayTV` vs `Vijay TV`, `ZeeTamil` vs `Zee Tamil`, `Colorstamil` vs `Colors Tamil`) and multi-space variations (`Vijay  TV`).
   - **Consequence**: The broadcasting statistics were split across **15 phantom channels** instead of the actual **10 television networks**.
3. **Piecemeal Boundary Checks**:
   - Out-of-bounds checks (`Avg_Rating < 0 | > 5`, `Subscription_Fee < 0`, `Years_Active < 0`) were scattered across cells 19–31 instead of a unified validation barrier.
4. **Duplicate Calculations & Lack of Modularity**:
   - Zero functions, zero classes, no type annotations, and hardcoded paths.
   - Redundant calculations across cells (e.g., duplicate calls to `df.nlargest(10, 'Social_Media_Followers')` in Cells 60 and 61; recomputing channel summaries in Cells 48, 84, and 91).
5. **No Interactive Interface or Automated Testing**:
   - Stakeholders had to manually scroll through 92 notebook cells to view static plots; no automated unit tests verified dataset integrity.

---

## 2. Production Architecture & Directory Structure

```
Tv Channel/
├── config/
│   ├── __init__.py
│   └── settings.py              # Centralized paths, canonical mappings, bounds, plot themes
├── src/
│   ├── __init__.py              # Unified package exports
│   ├── data_loader.py           # Robust CSV ingestion, schema validation & profiling
│   ├── cleaner.py               # Entity canonicalization, boundary enforcement, hierarchical imputation
│   ├── analytics.py             # KPIs, Channel Power Index, leaderboards, correlations
│   ├── visualizer.py            # High-resolution Matplotlib/Seaborn plots with formatted axes
│   └── report_generator.py      # Automated executive markdown & table generator
├── app/
│   └── dashboard.py             # Interactive Streamlit dashboard with tabs, filters & downloads
├── data/
│   ├── raw/                     # Original raw CSV repository
│   └── processed/               # Cleaned dataset (0 nulls, canonicalized)
├── reports/
│   ├── tv_channel_executive_report.md  # Generated executive report
│   └── figures/                 # 7 High-resolution figures (300 DPI)
├── tests/
│   ├── __init__.py
│   ├── test_cleaner.py          # DataCleaner unit & assertion tests
│   └── test_analytics.py        # KPI & Power Index calculation tests
├── TV_channel_dataset.csv       # Preserved original raw data
├── cleaned_tv_channel_dataset.csv # Generated production cleaned data
├── channel.ipynb                # Preserved original exploratory notebook
├── main.py                      # Production CLI pipeline entry point
├── requirements.txt             # Verified environment dependencies
└── README.md                    # Project documentation & instructions
```

---

## 3. Local Setup & Running Commands

Follow these commands to run the project locally on your machine.

### Step 1: Environment Setup
Open PowerShell or your terminal in the project directory:
```powershell
cd "c:\Users\DELL\ponasha\Tv Channel"
```
*(Optional) Create and activate a virtual environment:*
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Complete Pipeline
Run data cleaning, analytics calculation, figure generation, and executive reporting in one command:
```powershell
python main.py --all
```

**What this produces:**
- Cleans the raw data and exports `cleaned_tv_channel_dataset.csv` (100% clean, 0 nulls).
- Generates 7 high-res charts in [reports/figures/](file:///c:/Users/DELL/ponasha/Tv%20Channel/reports/figures/).
- Generates the executive report in [reports/tv_channel_executive_report.md](file:///c:/Users/DELL/ponasha/Tv%20Channel/reports/tv_channel_executive_report.md).

### Step 4: Launch Interactive Streamlit Dashboard
Launch the web application to interactively filter channels, inspect leaderboards, and visualize metrics:
```powershell
streamlit run app/dashboard.py
```
*(Or via the CLI shortcut):*
```powershell
python main.py --dashboard
```
The dashboard opens automatically in your browser at `http://localhost:8501`.

### Step 5: Run Automated Unit Tests
Verify data cleaning correctness and analytical calculations:
```powershell
pytest tests/
```

---

## 4. CLI Options & Modular Execution

You can run individual stages of the pipeline independently:

| Command | Action |
| :--- | :--- |
| `python main.py --all` | Runs end-to-end pipeline (Clean, Analyze, Visualize, Report) |
| `python main.py --clean` | Runs only data cleaning, canonicalization & imputation |
| `python main.py --analyze` | Computes and displays network KPIs and channel summaries |
| `python main.py --visualize` | Exports all 7 publication plots to `reports/figures/` |
| `python main.py --report` | Generates `reports/tv_channel_executive_report.md` |
| `python main.py --dashboard` | Starts the interactive Streamlit dashboard |

---

## 5. Executive Insights & KPIs

- **Active Network Scale**: 10 primary broadcasting networks across 27 distinct show titles.
- **Average Viewership**: ~6.14 Million viewers per broadcast.
- **Average Show Rating**: 3.65 / 5.0.
- **Average Digital Reach**: ~50.0 Million YouTube views and ~4.05 Million social followers per channel.
- **Top Channel by Power Index**: **Star Sports** (89.22), followed by **Jaya TV** (76.00) and **Colors Tamil** (74.02).
- **Most Popular Genre**: **Music** and **Reality** deliver the highest average viewership across networks.
