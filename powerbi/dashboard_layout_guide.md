# Power BI Dashboard Layout & Visual Design Guide

## 1. Executive Layout Architecture
The dashboard canvas is formatted in standard **16:9 widescreen layout** (1280 x 720 px) following standard enterprise visual hierarchy rules.

```text
+-----------------------------------------------------------------------------------------------+
| HEADER BAR: Title, Dynamic Subtitle, Slicers (Year, Month, Category, Weekday)                 |
+---------------------+---------------------+---------------------+-----------------------------+
| KPI CARD 1          | KPI CARD 2          | KPI CARD 3          | KPI CARD 4                  |
| Total Sales Units   | Top Bestseller      | Avg Daily Sales     | Total Days Analyzed         |
| [ 127,595.50 ]      | [ N02BE (49.4%) ]   | [ 60.59 / day ]     | [ 2,106 Days ]              |
+---------------------+---------------------+---------------------+-----------------------------+
| SECTION 1: MONTHLY SALES TREND (LINE CHART)             | SECTION 2: CATEGORY SALES (BAR)     |
| [Line chart displaying 2014-2019 monthly seasonality]   | [Column chart comparing 8 categories]|
+---------------------------------------------------------+-------------------------------------+
| SECTION 3: WEEKDAY DISTRIBUTION (BAR CHART)             | SECTION 4: DETAILED MATRIX TABLE    |
| [Horizontal bar chart: Saturday peak vs Thursday low]   | [Year x Category drilldown table]   |
+---------------------------------------------------------+-------------------------------------+
```

---

## 2. Visual Component Detailed Specifications

### Top Header & Filter Slicers Bar
- **Position**: Top row `(Y: 0px to 80px)`
- **Title Visual**: Text Box / Card with DAX Measure `[Dynamic Title]`. Font: Segoe UI Bold (20pt).
- **Slicers**:
  1. **Year Slicer**: Dropdown / Button Slicer connected to `Dim_Date[Year]`.
  2. **Month Slicer**: Dropdown Slicer connected to `Dim_Date[Month_Name]`.
  3. **Category Slicer**: Multi-select dropdown connected to `Dim_Category[Category_Name]`.
  4. **Weekday Slicer**: Dropdown connected to `Dim_Date[Weekday_Name]`.

### KPI Cards Row
- **Position**: Row 2 `(Y: 90px to 170px)`
- **KPI Card 1**: `Total Units Sold` -> Value: `127.59K`, Subtext: "Total Volume".
- **KPI Card 2**: `Top Selling Category` -> Value: `N02BE (Paracetamol)`, Subtext: "49.38% Portfolio Share".
- **KPI Card 3**: `Average Daily Sales` -> Value: `60.59`, Subtext: "Units / Day".
- **KPI Card 4**: `Total Days Analyzed` -> Value: `2,106`, Subtext: "2014 - 2019 Period".

### Visual Section 1: Monthly Sales Unit Trend (Line Chart)
- **Position**: Left Middle Canvas `(W: 60%, H: 240px)`
- **Visual Type**: Line Chart
- **X-Axis**: `Dim_Date[Year_Month]`
- **Y-Axis**: `[Total Units Sold]`
- **Tooltips**: `[Average Daily Sales]`, `[Prior Year Sales]`, `[YoY Growth %]`
- **Color Accent**: Deep Blue (`#1f77b4`)
- **Key Insight Shown**: Identifies autumn/winter seasonal surges (Jan & Oct peaks) driven by flu remedies.

### Visual Section 2: Sales Volume by Drug Category (Column Chart)
- **Position**: Right Middle Canvas `(W: 38%, H: 240px)`
- **Visual Type**: Clustered Column Chart
- **X-Axis**: `Dim_Category[Category_Code]`
- **Y-Axis**: `[Total Units Sold]`
- **Data Labels**: On (`#,#0` format)
- **Color Highlight**: Highlight `N02BE` in Red Accent (`#d62728`), remaining bars in Navy Blue.

### Visual Section 3: Day-of-Week Sales Distribution (Clustered Bar Chart)
- **Position**: Bottom Left Canvas `(W: 48%, H: 240px)`
- **Visual Type**: Clustered Horizontal Bar Chart
- **Y-Axis**: `Dim_Date[Weekday_Name]` (Sorted by `Day_of_Week`)
- **X-Axis**: `[Total Units Sold]`
- **Key Insight Shown**: Saturday achieves highest sales volume (`19,767.59` units), followed by Sunday (`18,401.44` units).

### Visual Section 4: Category Performance Matrix (Table / Matrix)
- **Position**: Bottom Right Canvas `(W: 50%, H: 240px)`
- **Visual Type**: Matrix Visual
- **Rows**: `Dim_Category[Category_Code]`, `Dim_Category[Category_Name]`
- **Columns**: `Dim_Date[Year]`
- **Values**: `[Total Units Sold]`, `[Sales % Contribution]`
- **Conditional Formatting**: Background color gradient (light blue to dark blue) applied to `[Total Units Sold]`.
