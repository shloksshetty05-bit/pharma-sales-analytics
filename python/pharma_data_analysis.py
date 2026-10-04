"""
===============================================================================
PHARMACEUTICAL SALES DATA ANALYTICS - PYTHON EXPLORATORY ANALYSIS
===============================================================================
Description:
    Processes daily pharmaceutical sales records (2,106 rows across 8 ATC drug categories),
    transforms wide category columns into a normalized long format, computes statistical
    aggregations (Yearly, Monthly, Weekday, Category level), and outputs key metrics
    and visual charts.
===============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def load_and_preprocess_data(file_path):
    """Loads daily sales dataset and prepares cleaned features."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at {file_path}")
        
    df = pd.read_csv(file_path)
    df['datum'] = pd.to_datetime(df['datum'])
    
    # Define the 8 ATC drug code columns
    drug_cols = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']
    
    # Calculate daily total quantity
    df['Total_Sales_Units'] = df[drug_cols].sum(axis=1)
    
    # Map drug codes to human-readable therapeutic names
    category_map = {
        'M01AB': 'M01AB (Anti-Inflammatory Acetic)',
        'M01AE': 'M01AE (Anti-Inflammatory Propionic)',
        'N02BA': 'N02BA (Analgesics Salicylic)',
        'N02BE': 'N02BE (Analgesics Paracetamol)',
        'N05B': 'N05B (Psycholeptics Anxiolytics)',
        'N05C': 'N05C (Psycholeptics Hypnotics)',
        'R03': 'R03 (Respiratory Airway)',
        'R06': 'R06 (Respiratory Antihistamines)'
    }
    
    return df, drug_cols, category_map

def melt_to_long_format(df, drug_cols, category_map):
    """Transforms wide format dataset into normalized long format for DAX/SQL parity."""
    long_df = pd.melt(
        df,
        id_vars=['datum', 'Year', 'Month', 'Hour', 'Weekday Name'],
        value_vars=drug_cols,
        var_name='Drug_Category_Code',
        value_name='Quantity_Sold'
    )
    long_df['Category_Name'] = long_df['Drug_Category_Code'].map(category_map)
    return long_df

def run_analytical_aggregations(df, long_df, drug_cols):
    """Computes core KPI metrics and summary aggregations."""
    print("=" * 70)
    print("PHARMACEUTICAL SALES ANALYTICS - EXECUTIVE SUMMARY")
    print("=" * 70)
    
    total_units = df['Total_Sales_Units'].sum()
    avg_daily_units = df['Total_Sales_Units'].mean()
    total_days = len(df)
    min_date = df['datum'].min().strftime('%Y-%m-%d')
    max_date = df['datum'].max().strftime('%Y-%m-%d')
    
    print(f"Date Range Analyzed     : {min_date} to {max_date} ({total_days:,} days)")
    print(f"Total Sales Units Sold : {total_units:,.2f} units")
    print(f"Average Daily Sales    : {avg_daily_units:,.2f} units/day")
    print("-" * 70)
    
    # 1. Sales by Category
    cat_summary = long_df.groupby(['Drug_Category_Code', 'Category_Name'])['Quantity_Sold'].agg(['sum', 'mean', 'std']).reset_index()
    cat_summary['Share_%'] = (cat_summary['sum'] / total_units) * 100
    cat_summary = cat_summary.sort_values(by='sum', ascending=False)
    
    print("\n--- 1. SALES PERFORMANCE BY DRUG CATEGORY ---")
    for _, row in cat_summary.iterrows():
        print(f"  {row['Drug_Category_Code']:<7} | {row['sum']:10,.2f} units | Share: {row['Share_%']:5.2f}% | Avg/Day: {row['mean']:5.2f}")
        
    # 2. Yearly Sales
    yearly = df.groupby('Year')['Total_Sales_Units'].agg(['sum', 'count']).reset_index()
    yearly['YoY_Growth_%'] = yearly['sum'].pct_change() * 100
    print("\n--- 2. ANNUAL SALES BREAKDOWN ---")
    for _, row in yearly.iterrows():
        growth_str = f"{row['YoY_Growth_%']:+.2f}%" if pd.notnull(row['YoY_Growth_%']) else "N/A (Base)"
        print(f"  Year {int(row['Year'])} : {row['sum']:10,.2f} units ({row['count']} days) | YoY Growth: {growth_str}")
        
    # 3. Monthly Aggregates
    monthly_all = df.groupby('Month')['Total_Sales_Units'].sum().reset_index()
    print("\n--- 3. MONTHLY AGGREGATE DEMAND (SEASONALITY) ---")
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_all['Month_Name'] = monthly_all['Month'].apply(lambda m: month_names[m-1])
    for _, row in monthly_all.iterrows():
        print(f"  Month {row['Month']:2d} ({row['Month_Name']}) : {row['Total_Sales_Units']:10,.2f} units")
        
    # 4. Weekday Analysis
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_sales = df.groupby('Weekday Name')['Total_Sales_Units'].sum().reindex(weekday_order).reset_index()
    print("\n--- 4. WEEKDAY SALES DISTRIBUTION ---")
    for _, row in weekday_sales.iterrows():
        print(f"  {row['Weekday Name']:<10} : {row['Total_Sales_Units']:10,.2f} units")
        
    return cat_summary, yearly, monthly_all, weekday_sales

def generate_visualizations(df, long_df, cat_summary, yearly, monthly_all, weekday_sales, output_dir):
    """Generates clean dashboard-aligned visualization figures."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Figure 1: Sales by Drug Category
    plt.figure(figsize=(10, 5))
    palette = ['#1f77b4' if code != 'N02BE' else '#d62728' for code in cat_summary['Drug_Category_Code']]
    sns.barplot(data=cat_summary, x='Drug_Category_Code', y='sum', palette=palette)
    plt.title('Total Sales Quantity by Drug Category (2014-2019)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('ATC Drug Category Code', fontsize=11, fontweight='bold')
    plt.ylabel('Total Units Sold', fontsize=11, fontweight='bold')
    for idx, row in cat_summary.reset_index().iterrows():
        plt.text(idx, row['sum'] + 1000, f"{row['sum']:,.0f}\n({row['Share_%']:.1f}%)", ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_category_sales.png'), dpi=300)
    plt.close()
    
    # Figure 2: Monthly Sales Trend (Line Chart)
    monthly_trend = df.copy()
    monthly_trend['YearMonth'] = monthly_trend['datum'].dt.to_period('M').dt.to_timestamp()
    monthly_grouped = monthly_trend.groupby('YearMonth')['Total_Sales_Units'].sum().reset_index()
    
    plt.figure(figsize=(12, 5))
    plt.plot(monthly_grouped['YearMonth'], monthly_grouped['Total_Sales_Units'], color='#1f77b4', linewidth=2, marker='o', markersize=4)
    plt.title('Monthly Sales Unit Trend (2014 - 2019)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date (Year-Month)', fontsize=11, fontweight='bold')
    plt.ylabel('Total Monthly Units Sold', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_monthly_trend.png'), dpi=300)
    plt.close()
    
    # Figure 3: Weekday Sales Distribution
    plt.figure(figsize=(9, 4.5))
    sns.barplot(data=weekday_sales, x='Weekday Name', y='Total_Sales_Units', color='#2ca02c')
    plt.title('Total Sales Quantity by Day of Week', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Day of Week', fontsize=11, fontweight='bold')
    plt.ylabel('Total Units Sold', fontsize=11, fontweight='bold')
    for idx, row in weekday_sales.iterrows():
        plt.text(idx, row['Total_Sales_Units'] + 200, f"{row['Total_Sales_Units']:,.0f}", ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_weekday_sales.png'), dpi=300)
    plt.close()

    print(f"\n[INFO] Dashboard chart images successfully saved to '{output_dir}/'")

def main():
    data_path = os.path.join('data', 'salesdaily.csv')
    output_dir = 'screenshots'
    
    df, drug_cols, category_map = load_and_preprocess_data(data_path)
    long_df = melt_to_long_format(df, drug_cols, category_map)
    cat_summary, yearly, monthly_all, weekday_sales = run_analytical_aggregations(df, long_df, drug_cols)
    generate_visualizations(df, long_df, cat_summary, yearly, monthly_all, weekday_sales, output_dir)

if __name__ == '__main__':
    main()
