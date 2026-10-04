-- ===============================================================================
-- PHARMACEUTICAL SALES ANALYTICS - SQL DATA CLEANING & UNPIVOTING
-- ===============================================================================
-- Author: Portfolio Student Data Analyst
-- Description: Performs data validation, transforms wide daily records into normalized
--              fact rows, populates Dim_Date and Fact_PharmaSales tables.
-- ===============================================================================

-- 1. VALIDATION: CHECK FOR NULL VALUES OR INVALID DATES
SELECT 
    COUNT(*) AS total_records,
    SUM(CASE WHEN datum IS NULL THEN 1 ELSE 0 END) AS null_dates,
    SUM(CASE WHEN M01AB IS NULL THEN 1 ELSE 0 END) AS null_M01AB,
    SUM(CASE WHEN N02BE IS NULL THEN 1 ELSE 0 END) AS null_N02BE
FROM staging_pharma_daily_sales;

-- 2. POPULATE DIM_DATE DIMENSION
INSERT INTO dim_date (date_key, year, month, month_name, quarter, day_of_month, day_of_week, weekday_name, is_weekend)
SELECT DISTINCT
    CAST(datum AS DATE) AS date_key,
    Year,
    Month,
    CASE Month
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
        WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
    END AS month_name,
    ((Month - 1) / 3) + 1 AS quarter,
    EXTRACT(DAY FROM CAST(datum AS DATE)) AS day_of_month,
    EXTRACT(DOW FROM CAST(datum AS DATE)) AS day_of_week,
    Weekday_Name,
    CASE WHEN Weekday_Name IN ('Saturday', 'Sunday') THEN 1 ELSE 0 END AS is_weekend
FROM staging_pharma_daily_sales
ON CONFLICT (date_key) DO NOTHING;

-- 3. UNPIVOT WIDE COLUMNS AND POPULATE FACT_PHARMA_SALES
-- Unpivots 8 ATC drug columns (M01AB through R06) into long format rows
INSERT INTO fact_pharma_sales (date_key, category_id, atc_code, quantity_sold)
SELECT CAST(s.datum AS DATE), 1, 'M01AB', s.M01AB FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 2, 'M01AE', s.M01AE FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 3, 'N02BA', s.N02BA FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 4, 'N02BE', s.N02BE FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 5, 'N05B',  s.N05B  FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 6, 'N05C',  s.N05C  FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 7, 'R03',   s.R03   FROM staging_pharma_daily_sales s UNION ALL
SELECT CAST(s.datum AS DATE), 8, 'R06',   s.R06   FROM staging_pharma_daily_sales s;

-- 4. VERIFY FACT TABLE ROW COUNT & GRAND TOTAL
-- Expected: 2,106 daily records * 8 drug categories = 16,848 fact rows
SELECT 
    COUNT(*) AS total_fact_rows,
    SUM(quantity_sold) AS grand_total_units_sold,
    COUNT(DISTINCT date_key) AS unique_days_covered
FROM fact_pharma_sales;
