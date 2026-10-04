# Power BI Data Model & Star Schema Specification

## 1. Overview
The Power BI data model follows a **Star Schema** architectural pattern designed for high-performance DAX evaluations and clean filter propagation.

```text
       +--------------------+          +-----------------------+
       |     Dim_Date       |          |     Dim_Category      |
       +--------------------+          +-----------------------+
       | Date (PK)          |          | Category_Code (PK)    |
       | Year               |          | Category_Name         |
       | Month              |          | Therapeutic_Group     |
       | Weekday_Name       |          +-----------+-----------+
       +---------+----------+                      |
                 | 1                               | 1
                 |                                 |
                 | *                               | *
       +---------+---------------------------------+-----------+
       |                    Fact_PharmaSales                   |
       +-------------------------------------------------------+
       | Date (FK)                                             |
       | Category_Code (FK)                                    |
       | Quantity                                              |
       +-------------------------------------------------------+
```

---

## 2. Table Specifications

### Fact Table: `Fact_PharmaSales`
- **Granularity**: 1 record per date per drug category.
- **Total Rows**: `16,848` rows (`2,106` days * `8` categories).
- **Columns**:
  - `Date` (Date) -> Connects to `Dim_Date[Date]`
  - `Category_Code` (Text) -> Connects to `Dim_Category[Category_Code]`
  - `Quantity` (Decimal) -> Units sold for that specific category on that day.

### Dimension Table 1: `Dim_Date`
- **Granularity**: 1 row per calendar day (`2,106` rows from `2014-01-02` to `2019-10-08`).
- **Marked as Date Table**: Yes (`Date` column).
- **Columns**:
  - `Date` (Date, Primary Key)
  - `Year` (Integer, `2014` - `2019`)
  - `Month` (Integer, `1` - `12`)
  - `Month_Name` (Text, `January` - `December`)
  - `Year_Month` (Text, `2014-01`)
  - `Day_of_Week` (Integer, `1` - `7`)
  - `Weekday_Name` (Text, `Monday` - `Sunday`)

### Dimension Table 2: `Dim_Category`
- **Granularity**: 1 row per ATC Drug Category (`8` rows).
- **Columns**:
  - `Category_Code` (Text, Primary Key): `M01AB`, `M01AE`, `N02BA`, `N02BE`, `N05B`, `N05C`, `R03`, `R06`.
  - `Category_Name` (Text): Human-readable category title.
  - `Therapeutic_Group` (Text): Medical classification group.

---

## 3. Relationships & Directionality
1. **`Dim_Date[Date]` -> `Fact_PharmaSales[Date]`**:
   - Cardinality: **One-to-Many (1:*)**
   - Cross Filter Direction: **Single** (`Dim_Date` filters `Fact_PharmaSales`)
2. **`Dim_Category[Category_Code]` -> `Fact_PharmaSales[Category_Code]`**:
   - Cardinality: **One-to-Many (1:*)**
   - Cross Filter Direction: **Single** (`Dim_Category` filters `Fact_PharmaSales`)

---

## 4. DAX Best Practices Applied
- **Explicit Measures**: No implicit column aggregations are used in report visuals. All visuals consume defined DAX measures.
- **Star Schema Integrity**: Filtering flows unidirectionally from single-side dimensions to the many-side fact table.
- **Date Intelligence**: Time Intelligence measures (`TOTALYTD`, `SAMEPERIODLASTYEAR`) leverage a contiguous `Dim_Date` table marked as a Date Table.
