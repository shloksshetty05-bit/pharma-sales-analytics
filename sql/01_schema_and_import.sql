-- ===============================================================================
-- PHARMACEUTICAL SALES ANALYTICS - SQL DATABASE SCHEMA & DATA IMPORT
-- ===============================================================================
-- Author: Portfolio Student Data Analyst
-- Description: Creates raw staging tables, normalized star-schema dimension & fact
--              tables for pharmaceutical sales analytics. Compatible with PostgreSQL,
--              MySQL, and SQLite.
-- ===============================================================================

-- 1. DROP EXISTING TABLES IF RE-RUNNING
DROP TABLE IF EXISTS fact_pharma_sales;
DROP TABLE IF EXISTS dim_drug_category;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS staging_pharma_daily_sales;

-- 2. CREATE STAGING TABLE FOR RAW CSV IMPORT
CREATE TABLE staging_pharma_daily_sales (
    datum VARCHAR(20),
    M01AB NUMERIC(10, 4),
    M01AE NUMERIC(10, 4),
    N02BA NUMERIC(10, 4),
    N02BE NUMERIC(10, 4),
    N05B  NUMERIC(10, 4),
    N05C  NUMERIC(10, 4),
    R03   NUMERIC(10, 4),
    R06   NUMERIC(10, 4),
    Year  INT,
    Month INT,
    Hour  INT,
    Weekday_Name VARCHAR(15)
);

-- Note: Import data from 'data/salesdaily.csv' using database-specific import commands:
-- PostgreSQL: COPY staging_pharma_daily_sales FROM '/path/to/data/salesdaily.csv' DELIMITER ',' CSV HEADER;
-- MySQL: LOAD DATA INFILE '/path/to/data/salesdaily.csv' INTO TABLE staging_pharma_daily_sales FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
-- SQLite: .mode csv
--         .import data/salesdaily.csv staging_pharma_daily_sales

-- 3. CREATE DIMENSION TABLE: DIM_DRUG_CATEGORY
CREATE TABLE dim_drug_category (
    category_id INT PRIMARY KEY,
    atc_code VARCHAR(10) UNIQUE NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    therapeutic_group VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

INSERT INTO dim_drug_category (category_id, atc_code, category_name, therapeutic_group, description) VALUES
(1, 'M01AB', 'Anti-Inflammatory Acetic', 'Anti-inflammatory and Antirheumatic', 'Acetic acid derivatives and related substances'),
(2, 'M01AE', 'Anti-Inflammatory Propionic', 'Anti-inflammatory and Antirheumatic', 'Propionic acid derivatives (Ibuprofen, Ketoprofen)'),
(3, 'N02BA', 'Analgesics Salicylic Acid', 'Analgesics & Antipyretics', 'Salicylic acid and derivatives (Aspirin)'),
(4, 'N02BE', 'Analgesics Paracetamol', 'Analgesics & Antipyretics', 'Anilides (Paracetamol / Acetaminophen)'),
(5, 'N05B',  'Psycholeptics Anxiolytics', 'Psycholeptics', 'Anxiolytics / Anti-anxiety medications'),
(6, 'N05C',  'Psycholeptics Hypnotics', 'Psycholeptics', 'Hypnotics and sedatives'),
(7, 'R03',   'Respiratory Airway Drugs', 'Respiratory System', 'Drugs for obstructive airway diseases (Asthma/COPD)'),
(8, 'R06',   'Respiratory Antihistamines', 'Respiratory System', 'Antihistamines for systemic use (Allergy relief)');

-- 4. CREATE DIMENSION TABLE: DIM_DATE
CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    quarter INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,
    weekday_name VARCHAR(15) NOT NULL,
    is_weekend INT NOT NULL
);

-- 5. CREATE NORMALIZED FACT TABLE: FACT_PHARMA_SALES
CREATE TABLE fact_pharma_sales (
    sales_id SERIAL PRIMARY KEY,
    date_key DATE NOT NULL,
    category_id INT NOT NULL,
    atc_code VARCHAR(10) NOT NULL,
    quantity_sold NUMERIC(10, 4) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (category_id) REFERENCES dim_drug_category(category_id)
);
