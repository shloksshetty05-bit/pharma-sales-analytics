import zipfile
import json
import os

def build_pbix():
    pbix_path = os.path.join('powerbi', 'Pharmaceutical_Sales_Analytics.pbix')

    content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="image/xml" />
  <Default Extension="json" ContentType="application/json" />
  <Override PartName="/DataModelSchema" ContentType="application/json" />
  <Override PartName="/Report/Layout" ContentType="application/json" />
</Types>"""

    data_model_schema = {
        "name": "Pharmaceutical_Sales_Analytics",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "tables": [
                {
                    "name": "Fact_PharmaSales",
                    "columns": [
                        {"name": "datum", "dataType": "dateTime", "sourceColumn": "datum"},
                        {"name": "Category_Code", "dataType": "string", "sourceColumn": "Category_Code"},
                        {"name": "Quantity", "dataType": "double", "sourceColumn": "Quantity"}
                    ],
                    "measures": [
                        {"name": "Total Units Sold", "expression": "SUM(Fact_PharmaSales[Quantity])"},
                        {"name": "Average Daily Sales", "expression": "AVERAGE(Fact_PharmaSales[Quantity])"},
                        {"name": "Total Days Analyzed", "expression": "DISTINCTCOUNT(Fact_PharmaSales[datum])"},
                        {"name": "Sales % Contribution", "expression": "DIVIDE([Total Units Sold], CALCULATE([Total Units Sold], ALL(Dim_Category)), 0)"}
                    ]
                },
                {
                    "name": "Dim_Category",
                    "columns": [
                        {"name": "Category_Code", "dataType": "string", "sourceColumn": "Category_Code"},
                        {"name": "Category_Name", "dataType": "string", "sourceColumn": "Category_Name"},
                        {"name": "Therapeutic_Group", "dataType": "string", "sourceColumn": "Therapeutic_Group"}
                    ]
                },
                {
                    "name": "Dim_Date",
                    "columns": [
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date"},
                        {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                        {"name": "Month_Name", "dataType": "string", "sourceColumn": "Month_Name"},
                        {"name": "Weekday_Name", "dataType": "string", "sourceColumn": "Weekday_Name"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "rel_date_fact",
                    "fromTable": "Fact_PharmaSales",
                    "fromColumn": "datum",
                    "toTable": "Dim_Date",
                    "toColumn": "Date"
                },
                {
                    "name": "rel_category_fact",
                    "fromTable": "Fact_PharmaSales",
                    "fromColumn": "Category_Code",
                    "toTable": "Dim_Category",
                    "toColumn": "Category_Code"
                }
            ]
        }
    }

    layout = {
        "id": 0,
        "name": "ReportSection",
        "displayName": "Pharma Sales Dashboard",
        "filters": "[]",
        "sections": [
            {
                "name": "ReportSection1",
                "displayName": "Executive Dashboard",
                "visualContainers": [
                    {"x": 20, "y": 20, "z": 1, "width": 280, "height": 100, "config": "{\"name\":\"KPI_Total_Units\",\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Fact_PharmaSales.Total Units Sold\"}]}}}"},
                    {"x": 320, "y": 20, "z": 2, "width": 280, "height": 100, "config": "{\"name\":\"KPI_Bestseller\",\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Dim_Category.Category_Code\"}]}}}"},
                    {"x": 620, "y": 20, "z": 3, "width": 280, "height": 100, "config": "{\"name\":\"KPI_Avg_Daily\",\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Fact_PharmaSales.Average Daily Sales\"}]}}}"},
                    {"x": 920, "y": 20, "z": 4, "width": 280, "height": 100, "config": "{\"name\":\"KPI_Days\",\"singleVisual\":{\"visualType\":\"card\",\"projections\":{\"Values\":[{\"queryRef\":\"Fact_PharmaSales.Total Days Analyzed\"}]}}}"},
                    {"x": 20, "y": 140, "z": 5, "width": 600, "height": 260, "config": "{\"name\":\"Monthly_Trend\",\"singleVisual\":{\"visualType\":\"lineChart\",\"projections\":{\"Category\":[{\"queryRef\":\"Dim_Date.Date\"}],\"Y\":[{\"queryRef\":\"Fact_PharmaSales.Total Units Sold\"}]}}}"},
                    {"x": 640, "y": 140, "z": 6, "width": 560, "height": 260, "config": "{\"name\":\"Category_Sales\",\"singleVisual\":{\"visualType\":\"columnChart\",\"projections\":{\"Category\":[{\"queryRef\":\"Dim_Category.Category_Code\"}],\"Y\":[{\"queryRef\":\"Fact_PharmaSales.Total Units Sold\"}]}}}"},
                    {"x": 20, "y": 420, "z": 7, "width": 600, "height": 260, "config": "{\"name\":\"Weekday_Sales\",\"singleVisual\":{\"visualType\":\"barChart\",\"projections\":{\"Category\":[{\"queryRef\":\"Dim_Date.Weekday_Name\"}],\"Y\":[{\"queryRef\":\"Fact_PharmaSales.Total Units Sold\"}]}}}"},
                    {"x": 640, "y": 420, "z": 8, "width": 560, "height": 260, "config": "{\"name\":\"Category_Matrix\",\"singleVisual\":{\"visualType\":\"matrix\",\"projections\":{\"Rows\":[{\"queryRef\":\"Dim_Category.Category_Code\"}],\"Columns\":[{\"queryRef\":\"Dim_Date.Year\"}],\"Values\":[{\"queryRef\":\"Fact_PharmaSales.Total Units Sold\"}]}}}"}
                ]
            }
        ]
    }

    os.makedirs('powerbi', exist_ok=True)
    with zipfile.ZipFile(pbix_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('DataModelSchema', json.dumps(data_model_schema, indent=2))
        z.writestr('Report/Layout', json.dumps(layout, indent=2))
        z.writestr('Version', '1.20')

    print(f"Successfully compiled {pbix_path} (Size: {os.path.getsize(pbix_path)} bytes)")

if __name__ == '__main__':
    build_pbix()
