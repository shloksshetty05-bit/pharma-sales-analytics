"""
===============================================================================
PHARMACEUTICAL SALES DATA ANALYTICS - PYTHON EXPLORATORY ANALYSIS
===============================================================================
Description:
    Processes daily pharmaceutical sales records (2,106 rows across 8 ATC drug categories),
    transforms wide category columns into a normalized long format, computes statistical
    aggregations (Yearly, Monthly, Weekday, Category level), and outputs key metrics
    and visual charts with explicit partial-month annotations.
===============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
        print(f"  {row['Drug_Category_Code']:<7} | {row['sum']:10,.2f} units | Share of total sales volume: {row['Share_%']:5.2f}% | Avg/Day: {row['mean']:5.2f}")
        
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
    """Generates analytical charts with strict date boundary and partial-month annotations."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Figure 1: Sales by Drug Category
    plt.figure(figsize=(10, 5), dpi=300)
    palette = ['#d62728' if code == 'N02BE' else '#1f77b4' for code in cat_summary['Drug_Category_Code']]
    sns.barplot(data=cat_summary, x='Drug_Category_Code', y='sum', palette=palette, hue='Drug_Category_Code', legend=False)
    plt.title('Total Sales Quantity by Drug Category (2014 - Oct 2019)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('ATC Drug Category Code', fontsize=10, fontweight='bold')
    plt.ylabel('Total Units Sold', fontsize=10, fontweight='bold')
    for idx, row in cat_summary.reset_index().iterrows():
        plt.text(idx, row['sum'] + 1000, f"{row['sum']:,.0f}\n({row['Share_%']:.1f}%)", ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_category_sales.png'), dpi=300)
    plt.close()
    
    # Figure 2: Monthly Sales Trend (Line Chart with Oct 2019 Annotation & Exact X-Axis Limit)
    monthly_trend = df.copy()
    monthly_trend['YearMonth'] = monthly_trend['datum'].dt.to_period('M').dt.to_timestamp()
    monthly_grouped = monthly_trend.groupby('YearMonth')['Total_Sales_Units'].sum().reset_index()
    
    plt.figure(figsize=(12, 5.5), dpi=300)
    plt.plot(monthly_grouped['YearMonth'], monthly_grouped['Total_Sales_Units'], color='#1f77b4', linewidth=2, marker='o', markersize=4)
    plt.title('Monthly Sales Unit Trend (Jan 2014 – Oct 2019)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Date (Year-Month)', fontsize=10, fontweight='bold')
    plt.ylabel('Total Monthly Units Sold', fontsize=10, fontweight='bold')
    
    # Strict X-Axis Bounds: Start Jan 2014, End Oct 2019 (No extension into 2020)
    plt.xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2019-10-31'))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xticks(rotation=30)
    
    # Annotate October 2019 Partial Month Drop
    oct_2019_date = pd.Timestamp('2019-10-01')
    oct_2019_val = monthly_grouped[monthly_grouped['YearMonth'] == oct_2019_date]['Total_Sales_Units'].values[0]
    
    plt.plot(oct_2019_date, oct_2019_val, marker='o', markersize=8, color='#dc2626')
    plt.annotate(
        'Oct 2019 is a partial month\n(data available thru Oct 8 only)',
        xy=(oct_2019_date, oct_2019_val),
        xytext=(pd.Timestamp('2018-09-01'), oct_2019_val + 700),
        arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.5, headwidth=6),
        fontsize=9,
        fontweight='bold',
        color='#dc2626',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.9)
    )
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_monthly_trend.png'), dpi=300)
    plt.close()
    
    # Figure 3: Weekday Sales Distribution
    plt.figure(figsize=(9, 4.5), dpi=300)
    sns.barplot(data=weekday_sales, x='Weekday Name', y='Total_Sales_Units', color='#2ca02c')
    plt.title('Total Sales Quantity by Day of Week', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Day of Week', fontsize=10, fontweight='bold')
    plt.ylabel('Total Units Sold', fontsize=10, fontweight='bold')
    for idx, row in weekday_sales.iterrows():
        plt.text(idx, row['Total_Sales_Units'] + 200, f"{row['Total_Sales_Units']:,.0f}", ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_weekday_sales.png'), dpi=300)
    plt.close()

    # Figure 4: Multi-panel Python Analytical Dashboard
    fig, axes = plt.subplots(2, 2, figsize=(15, 9), dpi=300)
    fig.suptitle('PYTHON ANALYTICAL DASHBOARD - PHARMACEUTICAL SALES ANALYTICS', fontsize=16, fontweight='bold', color='#0f172a', y=0.98)
    
    # Subplot 1: Category volume
    sns.barplot(ax=axes[0, 0], data=cat_summary, x='Drug_Category_Code', y='sum', palette=palette, hue='Drug_Category_Code', legend=False)
    axes[0, 0].set_title('Category Sales Volume (N02BE Paracetamol Lead)', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Units Sold', fontsize=9)
    
    # Subplot 2: Monthly trend with annotation
    axes[0, 1].plot(monthly_grouped['YearMonth'], monthly_grouped['Total_Sales_Units'], color='#1f77b4', linewidth=2, marker='o', markersize=3)
    axes[0, 1].set_title('Monthly Sales Unit Trend (Jan 2014 – Oct 2019)', fontsize=11, fontweight='bold')
    axes[0, 1].set_xlim(pd.Timestamp('2014-01-01'), pd.Timestamp('2019-10-31'))
    axes[0, 1].plot(oct_2019_date, oct_2019_val, marker='o', color='#dc2626', markersize=6)
    axes[0, 1].text(pd.Timestamp('2017-06-01'), oct_2019_val + 500, 'Oct 2019 Partial Month (thru Oct 8)', color='#dc2626', fontweight='bold', fontsize=8)
    
    # Subplot 3: Weekday sales
    sns.barplot(ax=axes[1, 0], data=weekday_sales, x='Weekday Name', y='Total_Sales_Units', color='#059669')
    axes[1, 0].set_title('Day-of-Week Distribution (Saturday Peak)', fontsize=11, fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=15, labelsize=8)
    
    # Subplot 4: Annual sales
    sns.barplot(ax=axes[1, 1], data=yearly, x='Year', y='sum', color='#6366f1')
    axes[1, 1].set_title('Annual Sales Volume (2016 Peak Year)', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Units Sold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dashboard_overview_python.png'), dpi=300)
    plt.close()

    print(f"\n[INFO] Analytical charts successfully saved to '{output_dir}/'")

def main():
    data_path = os.path.join('data', 'salesdaily.csv')
    output_dir = 'screenshots'
    
    df, drug_cols, category_map = load_and_preprocess_data(data_path)
    long_df = melt_to_long_format(df, drug_cols, category_map)
    cat_summary, yearly, monthly_all, weekday_sales = run_analytical_aggregations(df, long_df, drug_cols)
    generate_visualizations(df, long_df, cat_summary, yearly, monthly_all, weekday_sales, output_dir)

if __name__ == '__main__':
    main()
