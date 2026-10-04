# Excel Data Cleaning & Validation Documentation

## Project Context
This document details the **Excel data preparation, data cleaning, validation formulas, and Pivot Table modeling** performed on the raw pharmaceutical sales dataset (`data/salesdaily.csv`) before importing into SQL and Power BI.

---

## 1. Initial Raw Dataset Inspection

| Property | Inspection Finding |
| :--- | :--- |
| **Raw File Path** | `data/salesdaily.csv` |
| **Total Rows** | `2,106` records (excluding header) |
| **Total Columns** | `13` columns (`datum`, 8 ATC drug categories, `Year`, `Month`, `Hour`, `Weekday Name`) |
| **Date Range** | January 2, 2014 to October 8, 2019 (2,106 days) |
| **Primary Key / Granularity** | 1 record per calendar day |

---

## 2. Data Cleaning & Validation Workflow

### Step 1: Duplicate Records Check
- **Objective**: Ensure no duplicate date entries exist in the daily dataset.
- **Excel Feature Used**: `Data` -> `Remove Duplicates` on column `datum`.
- **Excel Formula Verification**:
  ```excel
  =IF(COUNTIF($A$2:$A$2107, A2)>1, "Duplicate", "Unique")
  ```
- **Result**: `0` duplicate rows found. Exactly 2,106 unique dates.

### Step 2: Missing Values / Null Value Treatment
- **Objective**: Identify blank cells or `#N/A` errors across numeric drug sales columns (`B` through `I`).
- **Excel Formula Used**:
  ```excel
  =COUNTBLANK(B2:I2107)
  ```
- **Result**: `0` missing values found across all 8 ATC categories. Zero-sales days are legitimately represented as `0.0`.

### Step 3: Date Format Standardization
- **Objective**: Convert text-formatted date column `datum` (`1/2/2014`) into standardized Excel Serial Date (`YYYY-MM-DD`).
- **Excel Transformation**:
  ```excel
  =DATEVALUE(A2)
  ```
  Formated cell as `YYYY-MM-DD`.

### Step 4: Total Daily Sales Column Creation
- **Objective**: Add a helper column `Total_Daily_Sales` in Column `J` aggregating sales quantity across all 8 ATC categories for that day.
- **Excel Formula**:
  ```excel
  =SUM(B2:I2)
  ```
  *(Copied down from row 2 to 2107)*.

### Step 5: Data Validation & Cross-Sum Reconciliation
- **Objective**: Verify dataset grand totals and confirm Excel formulas match Python and SQL outputs.
- **Excel Formulas Executed**:
  - **Grand Total Units**: `=SUM(J2:J2107)` -> **`127,595.50`**
  - **Average Daily Units**: `=AVERAGE(J2:J2107)` -> **`60.59`**
  - **Max Single Day Sales**: `=MAX(J2:J2107)` -> **`154.50`**
  - **Min Single Day Sales**: `=MIN(J2:J2107)` -> **`0.00`** *(July 7, 2014 - Store closure/holiday)*

---

## 3. Pivot Table Modeling & Analysis

Three primary Pivot Tables were built in Excel for validation:

### Pivot Table 1: Category Sales Summary
- **Rows**: ATC Drug Category Code
- **Values**: `Sum of Sales Quantity`, `% of Grand Total`
- **Results**:
  - `N02BE` (Paracetamol): **63,005.40** units (**49.38%** share)
  - `N05B` (Anxiolytics): **18,645.74** units (**14.61%** share)
  - `R03` (Respiratory): **11,608.82** units (**9.10%** share)
  - `M01AB` (Acetic Anti-inflammatory): **10,600.94** units (**8.31%** share)

### Pivot Table 2: Annual Sales Performance
- **Rows**: `Year`
- **Values**: `Sum of Total_Daily_Sales`, `Average Daily Sales`
- **Results**:
  - `2014`: 20,238.34 units (Avg: 55.60/day)
  - `2015`: 22,752.36 units (Avg: 62.34/day)
  - `2016`: **25,234.93** units (Avg: **68.95**/day) — *Peak Sales Year*
  - `2017`: 19,399.37 units (Avg: 53.15/day)
  - `2018`: 22,884.56 units (Avg: 62.70/day)
  - `2019`: 17,085.96 units (Partial year up to Oct 8)

### Pivot Table 3: Day-of-Week Purchasing Behavior
- **Rows**: `Weekday Name` (Sorted Monday -> Sunday)
- **Values**: `Sum of Total_Daily_Sales`
- **Formula Used**: `=SUMIFS(J:J, M:M, "Saturday")`
- **Results**:
  - **Saturday**: **19,767.59** units (**15.49%** of weekly sales — *Highest demand day*)
  - **Sunday**: **18,401.44** units (**14.42%**)
  - **Thursday**: **17,212.39** units (**13.49%** — *Lowest demand day*)

---

## 4. Key Takeaways for Portfolio & Interviews
1. **Source of Truth Integrity**: Excel data cleaning proved that `salesdaily.csv` contains zero missing values and 2,106 contiguous daily records.
2. **Key Formulas Mastered**: `SUMIFS`, `AVERAGEIFS`, `COUNTIF`, `XLOOKUP`, `DATEVALUE`, `TEXT`.
3. **Data Parity**: Excel grand total (`127,595.50`) perfectly matches Python pandas `df[drugs].sum().sum()` and Power BI DAX `SUM(Fact_PharmaSales[Quantity])`.
