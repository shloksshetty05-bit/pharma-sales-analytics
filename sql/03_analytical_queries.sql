-- ===============================================================================
-- PHARMACEUTICAL SALES ANALYTICS - SQL ANALYTICAL BUSINESS QUERIES
-- ===============================================================================
-- Author: Portfolio Student Data Analyst
-- Description: Core analytical SQL queries answering business questions, including
--              category revenue shares, monthly seasonality, YoY growth, peak days,
--              and window functions.
-- ===============================================================================

-- -------------------------------------------------------------------------------
-- QUERY 1: EXECUTIVE OVERALL KPI SUMMARY
-- Business Question: What are the total sales units, average daily sales, and date range?
-- -------------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT date_key) AS total_days_analyzed,
    SUM(quantity_sold) AS total_units_sold,
    ROUND(AVG(daily_sales), 2) AS avg_daily_sales,
    MIN(date_key) AS start_date,
    MAX(date_key) AS end_date
FROM (
    SELECT date_key, SUM(quantity_sold) AS daily_sales
    FROM fact_pharma_sales
    GROUP BY date_key
) daily_totals;

-- -------------------------------------------------------------------------------
-- QUERY 2: CATEGORY PERFORMANCE & share of total sales volume
-- Business Question: Which drug categories drive the highest sales volume?
-- -------------------------------------------------------------------------------
SELECT 
    d.atc_code,
    d.category_name,
    d.therapeutic_group,
    ROUND(SUM(f.quantity_sold), 2) AS total_units_sold,
    ROUND(AVG(f.quantity_sold), 2) AS avg_daily_units,
    ROUND(SUM(f.quantity_sold) * 100.0 / SUM(SUM(f.quantity_sold)) OVER (), 2) AS market_share_percentage
FROM fact_pharma_sales f
JOIN dim_drug_category d ON f.category_id = d.category_id
GROUP BY d.atc_code, d.category_name, d.therapeutic_group
ORDER BY total_units_sold DESC;

-- -------------------------------------------------------------------------------
-- QUERY 3: ANNUAL SALES & YEAR-OVER-YEAR (YoY) GROWTH
-- Business Question: How do annual sales compare across years?
-- Uses Window Function LAG() to compute YoY growth percentage.
-- -------------------------------------------------------------------------------
WITH yearly_sales AS (
    SELECT 
        dt.year,
        COUNT(DISTINCT dt.date_key) AS days_in_year,
        ROUND(SUM(f.quantity_sold), 2) AS annual_units_sold
    FROM fact_pharma_sales f
    JOIN dim_date dt ON f.date_key = dt.date_key
    GROUP BY dt.year
)
SELECT 
    year,
    days_in_year,
    annual_units_sold,
    LAG(annual_units_sold) OVER (ORDER BY year) AS prior_year_units,
    ROUND(
        (annual_units_sold - LAG(annual_units_sold) OVER (ORDER BY year)) * 100.0 
        / LAG(annual_units_sold) OVER (ORDER BY year), 
        2
    ) AS yoy_growth_percentage
FROM yearly_sales
ORDER BY year;

-- -------------------------------------------------------------------------------
-- QUERY 4: MONTHLY AGGREGATE DEMAND & SEASONALITY
-- Business Question: Which months experience peak drug consumption?
-- -------------------------------------------------------------------------------
SELECT 
    dt.month,
    dt.month_name,
    ROUND(SUM(f.quantity_sold), 2) AS total_units_sold,
    ROUND(AVG(f.quantity_sold), 2) AS avg_daily_units,
    RANK() OVER (ORDER BY SUM(f.quantity_sold) DESC) AS seasonality_rank
FROM fact_pharma_sales f
JOIN dim_date dt ON f.date_key = dt.date_key
GROUP BY dt.month, dt.month_name
ORDER BY dt.month;

-- -------------------------------------------------------------------------------
-- QUERY 5: WEEKDAY PURCHASING PATTERNS
-- Business Question: Do customers buy more medications on weekends or weekdays?
-- -------------------------------------------------------------------------------
SELECT 
    dt.weekday_name,
    ROUND(SUM(f.quantity_sold), 2) AS total_units_sold,
    ROUND(AVG(daily_units), 2) AS avg_daily_units,
    ROUND(SUM(f.quantity_sold) * 100.0 / SUM(SUM(f.quantity_sold)) OVER (), 2) AS percentage_share
FROM fact_pharma_sales f
JOIN dim_date dt ON f.date_key = dt.date_key
JOIN (
    SELECT date_key, SUM(quantity_sold) AS daily_units
    FROM fact_pharma_sales
    GROUP BY date_key
) d_sum ON f.date_key = d_sum.date_key
GROUP BY dt.weekday_name, dt.day_of_week
ORDER BY dt.day_of_week;

-- -------------------------------------------------------------------------------
-- QUERY 6: TOP 3 BESTSELLING CATEGORIES PER YEAR
-- Business Question: Which drug categories ranked #1, #2, #3 each year?
-- Uses CTE and ROW_NUMBER() Window Function.
-- -------------------------------------------------------------------------------
WITH category_annual_rank AS (
    SELECT 
        dt.year,
        d.atc_code,
        d.category_name,
        ROUND(SUM(f.quantity_sold), 2) AS total_units,
        ROW_NUMBER() OVER (PARTITION BY dt.year ORDER BY SUM(f.quantity_sold) DESC) AS category_rank
    FROM fact_pharma_sales f
    JOIN dim_date dt ON f.date_key = dt.date_key
    JOIN dim_drug_category d ON f.category_id = d.category_id
    GROUP BY dt.year, d.atc_code, d.category_name
)
SELECT year, category_rank, atc_code, category_name, total_units
FROM category_annual_rank
WHERE category_rank <= 3
ORDER BY year, category_rank;
