# Comprehensive Interview Preparation Guide
## Pharmaceutical Sales Analytics Portfolio Project

This guide provides verbatim interview scripts, answers to 30+ technical and business questions, and detailed real-world problem-solving narratives based on the **Pharmaceutical Sales Analytics** project.

---

# SECTION 1: PROJECT ELEVATOR PITCHES

### 30-Second Pitch
> "I built an end-to-end Pharmaceutical Sales Analytics project analyzing 5.5 years of daily sales data across 8 drug categories totaling 127,500+ units sold. Using Excel, SQL, Python, and Power BI, I transformed raw daily records into an interactive star-schema dashboard. My analysis revealed that Paracetamol (N02BE) drives nearly 50% of total sales, with demand peaking sharply on Saturdays and during winter months. I also established cross-tool data governance to ensure 100% calculation parity across SQL, Python, and DAX."

---

### 60-Second Pitch
> "In my Pharmaceutical Sales Analytics project, I analyzed over 2,100 daily sales records spanning from 2014 to 2019 across 8 Anatomical Therapeutic Chemical drug groups. My goal was to help pharmacy managers understand product demand trends, seasonality, and purchasing behaviors. 
> 
> I cleaned and validated the raw data in Excel, unpivoted the wide category columns into a normalized star schema using SQL, performed exploratory data analysis in Python pandas, and built an interactive Power BI dashboard with DAX time-intelligence measures. 
> 
> Key insights showed that Paracetamol accounts for 49.4% of total sales volume, winter months experience a 35% surge in cold and respiratory medications, and Saturday is the peak purchasing day. Based on these findings, I recommended adjusting safety stock buffers in September and optimizing weekend store staffing."

---

### 2-Minute Project Walkthrough
> "For my portfolio, I completed an end-to-end Data Analytics project on Pharmaceutical Sales data covering 2,106 calendar days between 2014 and 2019. 
> 
> **Data Cleaning & Governance**:
> I started in Excel by verifying data completeness, checking date formatting, and validating zero-sales records. I discovered that pre-aggregated monthly summary files contained a 0.79% discrepancy compared to daily records, so I designated the daily dataset as our primary single source of truth.
> 
> **SQL & Modeling**:
> In SQL, I created a star schema consisting of `Fact_PharmaSales`, `Dim_Date`, and `Dim_DrugCategory`. I unpivoted the 8 wide drug columns using `UNION ALL` to normalize the fact table into 16,848 rows. I wrote complex queries using window functions like `LAG()` for Year-over-Year growth and `RANK()` for monthly demand seasonality.
> 
> **Python Analysis**:
> Using Python pandas and seaborn, I performed exploratory analysis, validated category aggregations, and generated seasonal trend charts.
> 
> **Power BI & DAX**:
> In Power BI, I implemented DAX measures like `YTD Sales`, `SamePeriodLastYear`, `YoY Growth %`, and `Sales % Contribution`. I built an interactive dashboard featuring executive KPI cards, a monthly sales line chart, a category volume column chart, a weekday purchasing bar chart, and a granular matrix table.
> 
> **Business Impact**:
> The project proved that Paracetamol (N02BE) drives nearly half of overall sales volume, Saturday is the highest revenue day (15.5% share), and winter months experience massive sales surges. These insights directly inform inventory procurement buffers and store labor scheduling."

---

# SECTION 2: 30+ REALISTIC INTERVIEW QUESTIONS & ANSWERS

## A. General & Project Overview Questions

#### Q1: Tell me about your pharmaceutical sales project.
**Answer**: I analyzed 5.5 years of daily drug sales transactions (2,106 days, 127,595 units) across 8 ATC medication categories using Excel, SQL, Python, and Power BI. I modeled the data into a star schema, discovered key seasonal demand patterns (winter cold/flu surges and Saturday purchasing peaks), and built a Power BI dashboard to guide inventory buffering and pharmacy staffing.

#### Q2: Why did you choose pharmaceutical sales analysis?
**Answer**: Pharmaceutical supply chains are highly sensitive to seasonality and stockouts. Running out of critical medications like analgesics or respiratory drugs impacts public health and revenue. Analyzing 8 standardized ATC categories provided a rich dataset to showcase relational modeling, DAX time-intelligence, and business strategy skills.

#### Q3: What were the main business objectives?
**Answer**: To identify top-performing drug categories, quantify monthly and yearly seasonality, evaluate day-of-week customer purchasing behavior, and deliver an interactive Power BI dashboard that helps store managers optimize procurement and labor allocation.

#### Q4: What tools did you use and why?
**Answer**: Excel for initial data inspection and Pivot Table validation; SQL (PostgreSQL/SQLite) for relational database schema design, unpivoting, and window queries; Python (pandas/seaborn) for statistical EDA and automated reconciliation; and Power BI (DAX) for interactive data modeling and dashboarding.

#### Q5: What was your primary source of data?
**Answer**: A Kaggle daily pharmaceutical sales dataset (`salesdaily.csv`) containing 2,106 daily records from January 2, 2014 to October 8, 2019 for 8 ATC categories: M01AB, M01AE, N02BA, N02BE, N05B, N05C, R03, and R06.

#### Q6: What did this project teach you about data analyst workflows?
**Answer**: It taught me the critical importance of data governance and cross-tool reconciliation. Discovering variances between daily records and pre-aggregated monthly files emphasized that a data analyst must always verify underlying data integrity before building dashboards.

---

## B. Excel Questions

#### Q7: How did you clean and validate the dataset in Excel?
**Answer**: I checked for duplicate date entries using `=COUNTIF($A$2:$A$2107, A2)`, scanned for null values across numeric columns using `=COUNTBLANK()`, standardized dates using `=DATEVALUE()`, and created a helper column `=SUM(B2:I2)` to calculate total daily units.

#### Q8: Did you identify any duplicate records or missing values?
**Answer**: Zero duplicate date records were found across all 2,106 days. Zero null values existed in the numeric columns; zero-sales days were legitimately logged as `0.0`.

#### Q9: How did you use Pivot Tables to analyze the data?
**Answer**: I created three Pivot Tables: Category Sales Share (ranking N02BE #1 at 49.38%), Annual Trend Analysis (identifying 2016 as peak year with 25,235 units), and Weekday Purchasing Distribution (highlighting Saturday as peak day with 19,768 units).

#### Q10: Which Excel formulas did you rely on most?
**Answer**: `=SUMIFS()` for multi-criteria segment totals, `=AVERAGEIFS()` for daily averages, `=COUNTIF()` for deduplication, `=XLOOKUP()` for dimension mapping, and `=TEXT()` for extracting day names.

#### Q11: How did you validate that Excel calculations matched Python and SQL?
**Answer**: I verified that Excel's grand total `=SUM(J2:J2107)` yielded exactly **127,595.50 units**, matching Python `df[drugs].sum().sum()` and SQL `SUM(quantity_sold)` with 0.00 difference.

#### Q12: How would you handle missing date values in Excel?
**Answer**: I would construct a complete date calendar using `SEQUENCE()` or Excel's Fill Series, join the sales data using `XLOOKUP()`, and fill missing sales entries with `0` using `IFERROR(..., 0)`.

---

## C. SQL Questions

#### Q13: How did you design the database schema in SQL?
**Answer**: I built a Star Schema with a central fact table `fact_pharma_sales` connected via 1-to-many foreign keys to two dimension tables: `dim_date` (2,106 rows) and `dim_drug_category` (8 rows).

#### Q14: How did you unpivot the wide CSV format into a normalized fact table?
**Answer**: I used a multi-branch `UNION ALL` query selecting date and category code for each of the 8 columns (`M01AB` through `R06`), inserting 16,848 normalized fact rows (`2,106` days x `8` categories) into `fact_pharma_sales`.

#### Q15: How did you calculate Year-over-Year (YoY) growth in SQL?
**Answer**: I used a Common Table Expression (CTE) to aggregate annual sales, then applied the `LAG()` window function:
```sql
LAG(annual_units_sold) OVER (ORDER BY year)
```
and computed `((current - prior) / prior) * 100`.

#### Q16: How did you rank the top drug categories per year?
**Answer**: I used `ROW_NUMBER() OVER (PARTITION BY year ORDER BY SUM(quantity_sold) DESC)` inside a CTE, then filtered `WHERE category_rank <= 3`.

#### Q17: What is the difference between WHERE and HAVING in SQL?
**Answer**: `WHERE` filters individual rows before aggregation occurs (e.g. filtering dates in 2016), whereas `HAVING` filters aggregated groups after `GROUP BY` (e.g. `HAVING SUM(quantity_sold) > 10000`).

#### Q18: What SQL query did you write to analyze weekday sales?
**Answer**: I joined `fact_pharma_sales` with `dim_date`, grouped by `weekday_name` and `day_of_week`, computed `SUM(quantity_sold)`, and ordered by `day_of_week` to track Monday-to-Sunday progression.

---

## D. Python Questions

#### Q19: How did you use Python in this project?
**Answer**: I used Python 3.10 with `pandas` for data ingestion, unpivoting (`pd.melt`), statistical aggregation (`groupby`), and data reconciliation; and `seaborn`/`matplotlib` for visual chart generation.

#### Q20: How did you reshape wide data into long format in pandas?
**Answer**: I used `pd.melt()`:
```python
pd.melt(df, id_vars=['datum', 'Year', 'Month', 'Weekday Name'], value_vars=drug_cols, var_name='Drug_Category_Code', value_name='Quantity_Sold')
```

#### Q21: What statistical aggregations did you perform in Python?
**Answer**: I calculated total unit volume, daily averages, standard deviations, percentage market share per category, YoY growth rates, and monthly aggregated demand.

#### Q22: What charts did you generate using matplotlib/seaborn?
**Answer**: I generated a Category Bar Chart (`sns.barplot`), a Monthly Sales Trend Line (`plt.plot`), and a Weekday Sales Distribution Bar Chart, saving high-resolution PNGs to the `screenshots/` directory.

#### Q23: How did Python help you discover data discrepancies?
**Answer**: I wrote `python/data_verification.py` which compared category sums between `salesdaily.csv` and `salesmonthly.csv`. Python flagged a 1,009.73 unit variance (0.79%), establishing `salesdaily.csv` as our governing source of truth.

#### Q24: What is the difference between `groupby().sum()` and `pivot_table()` in pandas?
**Answer**: `groupby().sum()` returns a Series or DataFrame grouped by specified index columns, while `pivot_table()` provides multi-dimensional cross-tabulation with built-in margin totals, similar to Excel Pivot Tables.

---

## E. Power BI & DAX Questions

#### Q25: What is the structure of your Power BI data model?
**Answer**: A clean Star Schema consisting of `Fact_PharmaSales` connected via 1-to-many single-direction relationships to `Dim_Date` and `Dim_Category`.

#### Q26: What is the difference between a Calculated Column and a DAX Measure?
**Answer**: Calculated Columns are evaluated during data refresh and stored in RAM for every row. DAX Measures are dynamic calculations evaluated on-the-fly in response to user filter context, consuming minimal RAM.

#### Q27: How did you calculate Year-to-Date (YTD) sales in DAX?
**Answer**: Using the time-intelligence function:
```dax
YTD Sales = TOTALYTD(SUM(Fact_PharmaSales[Quantity]), Dim_Date[Date])
```

#### Q28: How did you calculate Prior Year Sales and YoY Growth %?
**Answer**:
```dax
Prior Year Sales = CALCULATE([Total Units Sold], SAMEPERIODLASTYEAR(Dim_Date[Date]))
YoY Growth % = DIVIDE([Total Units Sold] - [Prior Year Sales], [Prior Year Sales], 0)
```

#### Q29: How did you display the top-selling category name dynamically?
**Answer**: Using DAX:
```dax
Top Selling Category = CALCULATE(FIRSTNONBLANK(Dim_Category[Category_Name], 1), TOPN(1, ALL(Dim_Category), [Total Units Sold], DESC))
```

#### Q30: What charts did you include in the Power BI dashboard and why?
**Answer**: KPI Cards for top-level metrics; Line Chart for monthly sales trends to highlight winter seasonality; Column Chart for drug category sales volume; Clustered Bar Chart for weekday purchasing; and a Matrix Table for detailed tabular inspection.

---

# SECTION 3: "WHAT DIFFICULTIES DID YOU FACE?"

### Difficulty 1: Source File Discrepancy Between Daily Records & Monthly Summaries

- **Problem**: When cross-verifying `salesdaily.csv` and `salesmonthly.csv`, total category sales did not match perfectly (127,595.50 units in daily vs 126,585.77 units in monthly — a 1,009.73 unit variance).
- **Why It Happened**: The original pre-aggregated monthly file suffered from partial-month truncation in October 2019 and minor rounding differences.
- **How I Identified It**: I wrote an automated python reconciliation script (`python/data_verification.py`) that iterated through each ATC category and calculated variance.
- **How I Solved It**: I established data governance rules declaring `salesdaily.csv` as the single primary source of truth, deriving all SQL tables, Python models, and Power BI DAX measures from the daily granular dataset.
- **What I Learned**: Never assume pre-aggregated summary files are accurate. Always audit granular raw data to establish single-source-of-truth governance.
- **Verbal Interview Answer (45 sec)**:
  > *"During data validation, I wrote a Python script to compare sales totals between the daily file and the pre-aggregated monthly summary file. I discovered a 0.79% discrepancy where the monthly file was missing about 1,000 units due to truncation in the final month. To solve this, I established a strict data governance rule using the daily file as our single source of truth across SQL, Python, and Power BI. This ensured 100% calculation parity across all tools."*

---

### Difficulty 2: Normalizing Wide Multi-Category CSV Data into a Star Schema

- **Problem**: The raw CSV contained 8 separate columns for drug categories (`M01AB` to `R06`), which prevented effective slicing and category attribute filtering in Power BI.
- **Why It Happened**: Wide flat files are convenient for tabular entry but violate relational star-schema design principles.
- **How I Identified It**: When attempting to build a single category slicer in Power BI, I realized wide columns required 8 separate slicers rather than 1 unified filter.
- **How I Solved It**: In SQL, I wrote a unpivoting query using `UNION ALL` to transform 2,106 wide rows into 16,848 normalized fact records in `fact_pharma_sales`, linking them to a standalone `dim_drug_category` dimension table.
- **What I Learned**: Proper data normalization at the database level drastically simplifies DAX measure creation and enables intuitive user slicing.
- **Verbal Interview Answer (45 sec)**:
  > *"The raw dataset came in a wide format with 8 separate columns for drug categories. In Power BI, this would have required 8 individual visual filters. I solved this in SQL by unpivoting the data using UNION ALL into a normalized fact table of 16,848 rows linked to a category dimension table. This allowed me to create a single, clean category slicer and write simple, reusable DAX measures."*

---

### Difficulty 3: Partial-Year Skew in YoY Growth Calculations (2019 Data)

- **Problem**: 2019 data concluded on October 8, 2019 (281 days), causing full-year 2019 sales to appear artificially down by -25.34% compared to full-year 2018.
- **Why It Happened**: Comparing 9 months of data in 2019 against 12 months in 2018 creates an unfair year-over-year comparison.
- **How I Identified It**: The annual sales chart showed a steep drop in 2019, which could be misconstrued as a business failure.
- **How I Solved It**: In DAX and SQL, I implemented `SAMEPERIODLASTYEAR()` and filtered prior year context to match exact YTD date ranges (Jan 1 - Oct 8), accurately showing true performance growth.
- **What I Learned**: Time-intelligence analysis must account for partial period boundaries to prevent misleading business conclusions.
- **Verbal Interview Answer (45 sec)**:
  > *"The 2019 dataset ended in early October, which initially made 2019 annual sales look like they dropped by 25%. To prevent misleading stakeholders, I modified my DAX measures using SAMEPERIODLASTYEAR so that 2019 performance was compared strictly against the matching Jan-to-Oct period in 2018. This revealed true underlying sales trends rather than artificial partial-year drops."*

---

### Difficulty 4: Handling Zero-Sales Days Without Skewing Daily Averages

- **Problem**: On certain days (e.g. July 7, 2014), store sales recorded `0.0` units across all categories due to store closures or holidays.
- **Why It Happened**: Including closure days in `AVERAGE()` calculations depresses daily average sales metrics.
- **How I Identified It**: Comparing `=AVERAGE(J2:J2107)` including zeros vs excluding zeros produced a variance of ~1.8 units/day.
- **How I Solved It**: I documented both metrics clearly: `60.59 units/day` across all calendar days, and `61.42 units/day` across active trading days, allowing business users to toggle context.
- **What I Learned**: Clearly define whether business metrics reflect total calendar days or active trading days when presenting averages.
- **Verbal Interview Answer (40 sec)**:
  > *"I noticed several zero-sales days caused by store closures. Standard average formulas included these zeros, slightly pulling down daily sales averages. I resolved this by documenting both total calendar averages and active-trading-day averages in DAX, allowing stakeholders to evaluate operational performance accurately."*

---

### Difficulty 5: Designing a Widescreen Dashboard That Balances High-Density Metrics with Visual Clarity

- **Problem**: Displaying 8 drug categories, monthly trends, weekday distributions, and executive KPIs on a single 16:9 canvas risked visual overload.
- **Why It Happened**: Attempting to display every granular detail simultaneously creates cognitive friction for business users.
- **How I Identified It**: Initial dashboard drafts appeared crowded and lacked a clear visual focal point.
- **How I Solved It**: I organized the layout into 4 structured visual zones: Top Slicers/Title, Executive KPI Cards, Core Trends (Monthly Line + Category Column), and Detailed Drilldown (Weekday Bar + Matrix Table). I also used color highlighting (Red for top seller N02BE, Navy Blue for secondary categories).
- **What I Learned**: Effective visual hierarchy and intentional color choices guide executive attention to critical insights effortlessly.
- **Verbal Interview Answer (45 sec)**:
  > *"With 8 drug categories and 5.5 years of daily data, initial dashboard layouts felt cluttered. I redesigned the canvas into a structured 4-tier hierarchy: top-level KPIs at the top, macro trends in the middle, and detailed weekday/matrix tables at the bottom. I also used conditional color coding to highlight Paracetamol as the key revenue driver. This made the dashboard executive-ready and easy to digest."*
