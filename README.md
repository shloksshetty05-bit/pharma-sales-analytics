# Pharmaceutical Sales Analytics

A comprehensive data analytics project examining 5.5 years of daily pharmaceutical sales data (2,106 calendar days, 127,595.50 units sold) across 8 Anatomical Therapeutic Chemical (ATC) drug categories. This repository demonstrates end-to-end data analysis workflows encompassing **Excel data cleaning**, **SQL relational modeling & querying**, **Python data processing & exploratory data analysis (EDA)**, and an interactive **Power BI analytics dashboard**.

---

## Project Overview

Pharmaceutical distributors and pharmacy managers require data-driven visibility into medication demand patterns to optimize inventory procurement, prevent stockouts during seasonal disease spikes, and streamline supply chain operations. 

This project analyzes daily sales transactions across 8 therapeutic drug groups between January 2014 and October 2019 to identify seasonality trends, weekday buying behaviors, YoY growth dynamics, and category sales contributions.

---

## Business Objectives

1. **Category Demand Analysis**: Quantify total unit sales and market share across 8 distinct ATC drug categories to identify top-revenue drivers.
2. **Seasonality & Trend Identification**: Analyze monthly and annual sales patterns to pinpoint peak consumption periods (e.g., flu season vs. summer months).
3. **Purchasing Behavior Mapping**: Evaluate day-of-week demand trends to optimize pharmacy staffing and delivery schedules.
4. **Cross-Tool Data Reconciliation**: Establish single-source-of-truth data governance ensuring 100% calculation parity across Excel, SQL, Python, and Power BI DAX metrics.

---

## Dataset Description

The dataset comprises daily sales transactions recorded across 6 consecutive years (2014–2019) for 8 standardized Anatomical Therapeutic Chemical (ATC) drug classification codes.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `datum` | Date | Transaction date (`YYYY-MM-DD` / `MM/DD/YYYY`) |
| `M01AB` | Float | Anti-inflammatory & antirheumatic products, non-steroids (Acetic acid derivatives) |
| `M01AE` | Float | Anti-inflammatory & antirheumatic products, non-steroids (Propionic acid derivatives) |
| `N02BA` | Float | Other analgesics and antipyretics (Salicylic acid and derivatives - Aspirin) |
| `N02BE` | Float | Other analgesics and antipyretics (Anilides - Paracetamol / Acetaminophen) |
| `N05B` | Float | Psycholeptics (Anxiolytics - Anti-anxiety medications) |
| `N05C` | Float | Psycholeptics (Hypnotics and sedatives - Sleep aids) |
| `R03` | Float | Drugs for obstructive airway diseases (Asthma / COPD inhalers & medications) |
| `R06` | Float | Antihistamines for systemic use (Allergy relief) |
| `Year` | Integer | Transaction year (`2014` - `2019`) |
| `Month` | Integer | Transaction month (`1` - `12`) |
| `Hour` | Integer | Aggregated transaction hour |
| `Weekday Name` | String | Day of week (`Monday` through `Sunday`) |

### Key Dataset Statistics
- **Total Days Analyzed**: `2,106` days (January 2, 2014 to October 8, 2019)
- **Total Sales Volume**: `127,595.50` units
- **Average Daily Volume**: `60.59` units/day
- **Missing Values / Nulls**: `0` null values across all drug columns

---

## Tools & Technology Stack

- **Data Cleaning & Validation**: Excel (`SUMIFS`, `AVERAGEIFS`, `COUNTIF`, `XLOOKUP`, Pivot Tables)
- **Database & Querying**: SQL / PostgreSQL (`DDL`, `DML`, Unpivoting `UNION ALL`, `GROUP BY`, Window Functions `LAG()`, `RANK()`, `ROW_NUMBER()`)
- **Data Processing & Scripting**: Python 3.10, `pandas`, `numpy`
- **Exploratory Data Analysis & Visualization**: `matplotlib`, `seaborn`
- **Business Intelligence & Dashboarding**: Power BI Desktop, DAX Time Intelligence (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DIVIDE`, Star Schema Modeling)

---

## Project Architecture & Directory Structure

```text
pharma-sales-analytics/
│
├── data/
│   ├── salesdaily.csv              # Granular daily sales source of truth (2,106 rows)
│   ├── saleshourly.csv             # Hourly transaction records (50,534 rows)
│   ├── salesmonthly.csv            # Monthly aggregated summary (70 rows)
│   └── salesweekly.csv             # Weekly aggregated summary (304 rows)
│
├── excel/
│   ├── pharma_sales_excel_cleaning.md       # Step-by-step Excel cleaning documentation
│   └── data_cleaning_validation_summary.csv # Excel pivot validation summary dataset
│
├── sql/
│   ├── 01_schema_and_import.sql    # DDL scripts for staging, dim, and fact tables
│   ├── 02_data_cleaning.sql        # Data transformation & unpivoting queries
│   └── 03_analytical_queries.sql   # SQL business analytical queries & window functions
│
├── python/
│   ├── pharma_data_analysis.py     # Python data analysis & chart generator
│   └── data_verification.py        # Automated cross-tool reconciliation script
│
├── powerbi/
│   ├── dax_measures.dax            # Complete DAX measures library
│   ├── data_model_schema.md        # Star schema relationships & modeling guide
│   └── dashboard_layout_guide.md   # Visual layout & canvas specifications
│
├── screenshots/
│   ├── chart_category_sales.png    # Sales quantity by category visualization
│   ├── chart_monthly_trend.png     # Monthly trend visualization
│   └── chart_weekday_sales.png     # Weekday sales distribution chart
│
├── README.md                       # Main project documentation
├── INTERVIEW_PREPARATION.md        # Detailed interview guide, pitches & Q&A
├── INTERVIEW_CHEATSHEET.md         # Pre-interview quick revision cheat sheet
└── .gitignore                      # Git ignore file
```

---

## Data Cleaning Workflow

1. **Duplicate Verification**: Checked `datum` column for duplicates; verified 2,106 unique contiguous daily entries.
2. **Null Value Inspection**: Scanned all numeric columns for missing values or NaN errors; verified 0 nulls exist.
3. **Data Type Casting**: Transformed date text fields into ISO-8601 standard dates (`YYYY-MM-DD`).
4. **Data Normalization (Unpivoting)**: Transformed 8 wide ATC category columns into normalized long fact rows (`Date`, `Category_Code`, `Quantity_Sold`), converting 2,106 wide rows into 16,848 normalized fact rows.
5. **Reconciliation Audit**: Discovered that pre-aggregated `salesmonthly.csv` had a minor variance (126,585.77 units vs 127,595.50 units in `salesdaily.csv` - 0.79% variance). Designated `salesdaily.csv` as the official source of truth.

---

## Key Analytical Insights

1. **Bestseller Dominance**: `N02BE` (Paracetamol / Anilides) is the single largest category, accounting for **63,005.40 units** (**49.38%** of total pharmaceutical sales).
2. **Secondary Categories**: `N05B` (Anxiolytics - 14.61%), `R03` (Respiratory Airway - 9.10%), and `M01AB` (Anti-Inflammatory Acetic - 8.31%) represent secondary revenue pillars.
3. **Seasonal Peak Consumption**: Sales peak significantly during winter/autumn months — **January** (**13,970.69 units**) and **October** (**12,051.02 units**) — driven by surge demand for analgesics (`N02BE`) and respiratory products (`R03`). Summer months (June-August) experience lowest demand (~8,750–9,000 units/month).
4. **Annual Peak Year**: **2016** recorded highest annual sales (**25,234.93 units**, **+10.91% YoY growth**), averaging 68.95 units/day.
5. **Weekend Purchasing Behavior**: **Saturday** generates the highest sales volume (**19,767.59 units**, **15.49%** of weekly total), followed by Sunday (**18,401.44 units**), indicating strong weekend retail replenishment.

---

## Business Recommendations

1. **Paracetamol Stock Buffer**: Maintain a minimum safety stock buffer of +25% for `N02BE` (Paracetamol) starting in September to meet cold/flu demand surges through January.
2. **Weekend Staffing Optimization**: Increase pharmacy fulfillment and retail sales staffing on Saturdays and Sundays, when transaction volume peaks by ~15% compared to mid-week days (Thursday low of 17,212 units).
3. **Targeted Respiratory Promotion**: Align respiratory drug (`R03` / `R06`) promotions and inventory stock-ups with spring allergy (March/April) and autumn respiratory illness seasons.
4. **Slow-Moving Inventory Management**: `N05C` (Hypnotics & Sedatives) accounts for under 1% of total sales (1,249.96 units over 5.5 years). Transition `N05C` procurement to on-demand ordering to minimize holding costs and expiration write-offs.

---

## Project Limitations

- **Pricing Data Absence**: Dataset contains sales quantities (unit counts) but lacks unit prices and profit margins. Consequently, financial revenue and margin analysis cannot be directly computed.
- **Geographic Scope**: Dataset lacks store-level or regional location metadata, preventing geographic spatial analysis.
- **Partial Year 2019**: Data for 2019 concludes on October 8, 2019, rendering 2019 full-year comparison incomplete.

---

## Future Improvements

- Incorporate unit cost and retail price fields to analyze gross profit margins and product profitability.
- Build predictive time-series forecasting models (ARIMA / Prophet in Python) to forecast category-level monthly demand.
- Integrate store-location dimension tables to enable spatial region-wise sales benchmarking.
