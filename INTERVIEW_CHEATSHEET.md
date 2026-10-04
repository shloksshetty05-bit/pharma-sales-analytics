# Quick Interview Cheat Sheet: Pharmaceutical Sales Analytics

---

## 1. DATASET AT A GLANCE
- **Period Analyzed**: Jan 2, 2014 – Oct 8, 2019 (5.5 years / 2,106 calendar days).
- **Total Sales Volume**: **127,595.50 units** (Daily Source of Truth).
- **Average Daily Sales**: **60.59 units/day**.
- **Drug Categories (8 ATC Codes)**:
  - `N02BE` (Paracetamol / Anilides): **63,005.40 units** (**49.38%** share - #1 Bestseller)
  - `N05B` (Anxiolytics): **18,645.74 units** (**14.61%** share)
  - `R03` (Respiratory Airway): **11,608.82 units** (**9.10%** share)
  - `M01AB` (Acetic Anti-inflammatory): **10,600.94 units** (**8.31%** share)
  - `M01AE` (Propionic Anti-inflammatory): **8,204.62 units** (**6.43%** share)
  - `N02BA` (Salicylic Acid / Aspirin): **8,172.21 units** (**6.40%** share)
  - `R06` (Antihistamines): **6,107.82 units** (**4.79%** share)
  - `N05C` (Hypnotics / Sedatives): **1,249.96 units** (**0.98%** share)

---

## 2. KEY EXCEL FORMULAS & WORKFLOWS
- **Deduplication**: `=COUNTIF($A$2:$A$2107, A2)` -> `0` duplicates found.
- **Null Inspection**: `=COUNTBLANK(B2:I2107)` -> `0` null values found.
- **Daily Sum**: `=SUM(B2:I2)` -> Copied across 2,106 rows.
- **Segment Sums**: `=SUMIFS(J:J, K:K, 2016)` -> Peak year 2016 = 25,234.93 units.
- **Weekday Sums**: `=SUMIFS(J:J, M:M, "Saturday")` -> Peak day Saturday = 19,767.59 units.

---

## 3. KEY SQL QUERIES & SCHEMAS
- **Star Schema**: `fact_pharma_sales` (16,848 rows) connected to `dim_date` (2,106 rows) and `dim_drug_category` (8 rows).
- **Unpivoting Wide Data**:
  ```sql
  INSERT INTO fact_pharma_sales SELECT date, 1, 'M01AB', M01AB FROM staging UNION ALL ...
  ```
- **Year-over-Year Growth (Window Function)**:
  ```sql
  LAG(annual_units) OVER (ORDER BY year)
  ```
- **Category Annual Ranking**:
  ```sql
  ROW_NUMBER() OVER (PARTITION BY year ORDER BY SUM(quantity_sold) DESC)
  ```

---

## 4. KEY PYTHON PANDAS FUNCTIONS
- **Wide to Long Transformation**:
  ```python
  pd.melt(df, id_vars=['datum', 'Year', 'Month', 'Weekday Name'], value_vars=drug_cols, var_name='Drug_Category_Code', value_name='Quantity_Sold')
  ```
- **Aggregations**: `df.groupby('Year')['Total_Sales_Units'].sum()`
- **Cross-Tool Verification**: Verified daily total (`127,595.50`) vs monthly total (`126,585.77`).

---

## 5. KEY POWER BI DAX MEASURES
- `Total Units Sold = SUM(Fact_PharmaSales[Quantity])`
- `Average Daily Sales = AVERAGE(Fact_PharmaSales[Quantity])`
- `YTD Sales = TOTALYTD([Total Units Sold], Dim_Date[Date])`
- `Prior Year Sales = CALCULATE([Total Units Sold], SAMEPERIODLASTYEAR(Dim_Date[Date]))`
- `YoY Growth % = DIVIDE([Total Units Sold] - [Prior Year Sales], [Prior Year Sales], 0)`
- `Sales % Contribution = DIVIDE([Total Units Sold], CALCULATE([Total Units Sold], ALL(Dim_Category)), 0)`

---

## 6. TOP INSIGHTS & RECOMMENDATIONS
1. **Paracetamol Dominance**: N02BE accounts for ~50% of all sales. Maintain +25% inventory buffer starting in September.
2. **Winter Seasonality**: Demand peaks in Jan (13,971 units) and Oct (12,051 units) due to cold/flu remedies.
3. **Weekend Retail Peak**: Saturday is the highest volume day (19,768 units). Increase weekend store fulfillment staffing.
4. **Slow-Moving Item**: N05C (Hypnotics) accounts for <1% of sales; transition to on-demand ordering.

---

## 7. CONCEPTS YOU MUST UNDERSTAND BEFORE ADDING TO RESUME

1. **Star Schema Data Modeling**:
   - *What to know*: Fact tables store numeric quantitative events (`Quantity_Sold`); Dimension tables store descriptive context (`Date`, `Category_Name`). Relationships must be 1-to-Many single-direction filters.
2. **Data Unpivoting (Wide to Long)**:
   - *What to know*: Transforming multiple measure columns into attribute-value rows so slicers can dynamically filter categories.
3. **DAX Evaluation Context**:
   - *What to know*: Filter Context is defined by visual row/column headers and slicers. `CALCULATE()` modifies or overrides current filter context (e.g. `ALL(Dim_Category)`).
4. **Time Intelligence Functions**:
   - *What to know*: Functions like `SAMEPERIODLASTYEAR` require a contiguous date table marked as a Date Table with no missing calendar days.
5. **SQL Window Functions**:
   - *What to know*: `LAG()`, `RANK()`, `ROW_NUMBER()` compute calculations across a set of rows related to the current row without collapsing rows like `GROUP BY` does.
