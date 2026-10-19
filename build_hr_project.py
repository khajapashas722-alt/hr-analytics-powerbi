import json
import zipfile
import os

def generate_hr_model():
    base_dir = r"C:/Users/shakj/Documents/data-analytics-portfolio/power-bi/hr-analytics-powerbi"
    data_file = f"{base_dir}/data/employee_attrition_dataset.csv".replace("\\", "/")
    
    tables = [
        {
            "name": "Fact_Employees",
            "columns": [
                {"name": "Employee_ID", "dataType": "int64", "sourceColumn": "Employee_ID", "isKey": True},
                {"name": "Age", "dataType": "int64", "sourceColumn": "Age"},
                {"name": "Gender", "dataType": "string", "sourceColumn": "Gender"},
                {"name": "Marital_Status", "dataType": "string", "sourceColumn": "Marital_Status"},
                {"name": "Department", "dataType": "string", "sourceColumn": "Department"},
                {"name": "Job_Role", "dataType": "string", "sourceColumn": "Job_Role"},
                {"name": "Job_Level", "dataType": "int64", "sourceColumn": "Job_Level"},
                {"name": "Monthly_Income", "dataType": "double", "sourceColumn": "Monthly_Income", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Hourly_Rate", "dataType": "double", "sourceColumn": "Hourly_Rate", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Years_at_Company", "dataType": "int64", "sourceColumn": "Years_at_Company"},
                {"name": "Years_in_Current_Role", "dataType": "int64", "sourceColumn": "Years_in_Current_Role"},
                {"name": "Years_Since_Last_Promotion", "dataType": "int64", "sourceColumn": "Years_Since_Last_Promotion"},
                {"name": "Work_Life_Balance", "dataType": "int64", "sourceColumn": "Work_Life_Balance"},
                {"name": "Job_Satisfaction", "dataType": "int64", "sourceColumn": "Job_Satisfaction"},
                {"name": "Performance_Rating", "dataType": "int64", "sourceColumn": "Performance_Rating"},
                {"name": "Training_Hours_Last_Year", "dataType": "int64", "sourceColumn": "Training_Hours_Last_Year"},
                {"name": "Overtime", "dataType": "string", "sourceColumn": "Overtime"},
                {"name": "Project_Count", "dataType": "int64", "sourceColumn": "Project_Count"},
                {"name": "Average_Hours_Worked_Per_Week", "dataType": "double", "sourceColumn": "Average_Hours_Worked_Per_Week"},
                {"name": "Absenteeism", "dataType": "int64", "sourceColumn": "Absenteeism"},
                {"name": "Work_Environment_Satisfaction", "dataType": "int64", "sourceColumn": "Work_Environment_Satisfaction"},
                {"name": "Relationship_with_Manager", "dataType": "int64", "sourceColumn": "Relationship_with_Manager"},
                {"name": "Job_Involvement", "dataType": "int64", "sourceColumn": "Job_Involvement"},
                {"name": "Distance_From_Home", "dataType": "int64", "sourceColumn": "Distance_From_Home"},
                {"name": "Number_of_Companies_Worked", "dataType": "int64", "sourceColumn": "Number_of_Companies_Worked"},
                {"name": "Attrition", "dataType": "string", "sourceColumn": "Attrition"},
                {"name": "Age Group", "dataType": "string", "sourceColumn": "Age Group"},
                {"name": "Tenure Cohort", "dataType": "string", "sourceColumn": "Tenure Cohort"},
                {"name": "Department_Role_Key", "dataType": "string", "sourceColumn": "Department_Role_Key"}
            ],
            "partitions": [
                {
                    "name": "Fact_Employees-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            f'    Source = Csv.Document(File.Contents("{data_file}"), [Delimiter=",", Columns=26, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                            '    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                            '    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {',
                            '        {"Employee_ID", Int64.Type},',
                            '        {"Age", Int64.Type},',
                            '        {"Gender", type text},',
                            '        {"Marital_Status", type text},',
                            '        {"Department", type text},',
                            '        {"Job_Role", type text},',
                            '        {"Job_Level", Int64.Type},',
                            '        {"Monthly_Income", type number},',
                            '        {"Hourly_Rate", type number},',
                            '        {"Years_at_Company", Int64.Type},',
                            '        {"Years_in_Current_Role", Int64.Type},',
                            '        {"Years_Since_Last_Promotion", Int64.Type},',
                            '        {"Work_Life_Balance", Int64.Type},',
                            '        {"Job_Satisfaction", Int64.Type},',
                            '        {"Performance_Rating", Int64.Type},',
                            '        {"Training_Hours_Last_Year", Int64.Type},',
                            '        {"Overtime", type text},',
                            '        {"Project_Count", Int64.Type},',
                            '        {"Average_Hours_Worked_Per_Week", type number},',
                            '        {"Absenteeism", Int64.Type},',
                            '        {"Work_Environment_Satisfaction", Int64.Type},',
                            '        {"Relationship_with_Manager", Int64.Type},',
                            '        {"Job_Involvement", Int64.Type},',
                            '        {"Distance_From_Home", Int64.Type},',
                            '        {"Number_of_Companies_Worked", Int64.Type},',
                            '        {"Attrition", type text}',
                            '    }),',
                            '    AddAgeGroup = Table.AddColumn(ChangeTypes, "Age Group", each if [Age] < 30 then "Under 30" else if [Age] <= 39 then "30 - 39" else if [Age] <= 49 then "40 - 49" else "50+", type text),',
                            '    AddTenureCohort = Table.AddColumn(AddAgeGroup, "Tenure Cohort", each if [Years_at_Company] < 2 then "0 - 1 Years" else if [Years_at_Company] <= 5 then "2 - 5 Years" else if [Years_at_Company] <= 10 then "6 - 10 Years" else "10+ Years", type text),',
                            '    AddDeptRoleKey = Table.AddColumn(AddTenureCohort, "Department_Role_Key", each [Department] & "-" & [Job_Role], type text)',
                            "in",
                            "    AddDeptRoleKey"
                        ]
                    }
                }
            ]
        },
        {
            "name": "_HR_Measures",
            "columns": [
                {"name": "RowKey", "dataType": "int64", "sourceColumn": "RowKey", "isHidden": True}
            ],
            "partitions": [
                {
                    "name": "_HR_Measures-Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": [
                            "let",
                            '    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [RowKey = _t]),',
                            '    ChangeTypes = Table.TransformColumnTypes(Source,{{"RowKey", Int64.Type}})',
                            "in",
                            "    ChangeTypes"
                        ]
                    }
                }
            ],
            "measures": [
                {"name": "Total Headcount", "expression": "COUNTROWS(Fact_Employees)", "formatString": "#,0"},
                {"name": "Departed Employees", "expression": "CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Attrition] = \"Yes\")", "formatString": "#,0"},
                {"name": "Active Headcount", "expression": "CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Attrition] = \"No\")", "formatString": "#,0"},
                {"name": "Retention Rate %", "expression": "DIVIDE([Active Headcount], [Total Headcount], 0)", "formatString": "0.00%"},
                {"name": "Attrition Rate %", "expression": "DIVIDE([Departed Employees], [Total Headcount], 0)", "formatString": "0.00%"},
                {"name": "Average Monthly Income", "expression": "AVERAGE(Fact_Employees[Monthly_Income])", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Median Monthly Income", "expression": "MEDIAN(Fact_Employees[Monthly_Income])", "formatString": "$#,0.00;($#,0.00);$#,0.00"},
                {"name": "Average Company Tenure (Years)", "expression": "AVERAGE(Fact_Employees[Years_at_Company])", "formatString": "0.0"},
                {"name": "Average Years in Current Role", "expression": "AVERAGE(Fact_Employees[Years_in_Current_Role])", "formatString": "0.0"},
                {"name": "Average Years Since Last Promotion", "expression": "AVERAGE(Fact_Employees[Years_Since_Last_Promotion])", "formatString": "0.0"},
                {"name": "Average Absenteeism Days", "expression": "AVERAGE(Fact_Employees[Absenteeism])", "formatString": "0.0"},
                {"name": "Average Job Satisfaction", "expression": "AVERAGE(Fact_Employees[Job_Satisfaction])", "formatString": "0.00"},
                {"name": "Average Work Life Balance", "expression": "AVERAGE(Fact_Employees[Work_Life_Balance])", "formatString": "0.00"},
                {"name": "Average Work Environment Satisfaction", "expression": "AVERAGE(Fact_Employees[Work_Environment_Satisfaction])", "formatString": "0.00"},
                {"name": "Low Satisfaction Headcount", "expression": "CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Job_Satisfaction] <= 2)", "formatString": "#,0"},
                {"name": "Overtime Attrition Rate %", "expression": "CALCULATE([Attrition Rate %], Fact_Employees[Overtime] = \"Yes\")", "formatString": "0.00%"},
                {"name": "Non-Overtime Attrition Rate %", "expression": "CALCULATE([Attrition Rate %], Fact_Employees[Overtime] = \"No\")", "formatString": "0.00%"},
                {"name": "High Performer Flight Risk Count", "expression": "CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Performance_Rating] >= 4, Fact_Employees[Job_Satisfaction] <= 2, Fact_Employees[Attrition] = \"No\")", "formatString": "#,0"},
                {"name": "Department Attrition Rank", "expression": "IF(HASONEVALUE(Fact_Employees[Department]), RANKX(ALL(Fact_Employees[Department]), [Attrition Rate %], , DESC, Dense), BLANK())", "formatString": "#,0"},
                {"name": "Attrition Status Color Hex", "expression": "VAR Rate = [Attrition Rate %] RETURN SWITCH(TRUE(), Rate <= 0.12, \"#2ECC71\", Rate <= 0.18, \"#F1C40F\", \"#E74C3C\")"}
            ]
        }
    ]
    
    model = {
        "name": "HRAnalyticsDataModel",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-US",
            "tables": tables,
            "relationships": []
        }
    }
    return model

def generate_hr_report_layout():
    layout = {
        "id": 0,
        "resourcePackages": [],
        "sections": [
            {
                "id": 0,
                "name": "ReportSection_WorkforceOverview",
                "displayName": "Executive Workforce & Turnover Overview",
                "filters": "[]",
                "ordinal": 0,
                "visualContainers": [
                    {
                        "x": 20, "y": 15, "z": 1000, "width": 1240, "height": 45,
                        "config": json.dumps({
                            "name": "HeaderVisual_HR",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Workforce Headcount & Attrition Executive Dashboard",
                                                    "textStyle": {"fontFamily": "Segoe UI", "fontSize": "18pt", "fontWeight": "bold", "color": "#1A365D"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 70, "z": 2000, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "Card_TotalHeadcount",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Total Headcount"}]}
                            }
                        })
                    },
                    {
                        "x": 270, "y": 70, "z": 2001, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "Card_ActiveHeadcount",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Active Headcount"}]}
                            }
                        })
                    },
                    {
                        "x": 520, "y": 70, "z": 2002, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "Card_Departed",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Departed Employees"}]}
                            }
                        })
                    },
                    {
                        "x": 770, "y": 70, "z": 2003, "width": 230, "height": 95,
                        "config": json.dumps({
                            "name": "Card_AttritionRate",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Attrition Rate %"}]}
                            }
                        })
                    },
                    {
                        "x": 1020, "y": 70, "z": 2004, "width": 240, "height": 95,
                        "config": json.dumps({
                            "name": "Card_AvgIncome",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Average Monthly Income"}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 180, "z": 3000, "width": 600, "height": 270,
                        "config": json.dumps({
                            "name": "DeptAttritionBarChart",
                            "singleVisual": {
                                "visualType": "clusteredBarChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Employees.Department"}],
                                    "Y": [{"queryRef": "_HR_Measures.Attrition Rate %"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 640, "y": 180, "z": 3001, "width": 620, "height": 270,
                        "config": json.dumps({
                            "name": "TenureCohortColumnChart",
                            "singleVisual": {
                                "visualType": "clusteredColumnChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Employees.Tenure Cohort"}],
                                    "Y": [{"queryRef": "_HR_Measures.Attrition Rate %"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 465, "z": 3002, "width": 450, "height": 235,
                        "config": json.dumps({
                            "name": "OvertimeDonutChart",
                            "singleVisual": {
                                "visualType": "pieChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Employees.Overtime"}],
                                    "Y": [{"queryRef": "_HR_Measures.Departed Employees"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 490, "y": 465, "z": 3003, "width": 770, "height": 235,
                        "config": json.dumps({
                            "name": "DeptSummaryTable",
                            "singleVisual": {
                                "visualType": "tableEx",
                                "projections": {
                                    "Values": [
                                        {"queryRef": "Fact_Employees.Department"},
                                        {"queryRef": "_HR_Measures.Total Headcount"},
                                        {"queryRef": "_HR_Measures.Departed Employees"},
                                        {"queryRef": "_HR_Measures.Attrition Rate %"},
                                        {"queryRef": "_HR_Measures.Average Monthly Income"},
                                        {"queryRef": "_HR_Measures.Average Job Satisfaction"}
                                    ]
                                }
                            }
                        })
                    }
                ],
                "config": json.dumps({}),
                "width": 1280,
                "height": 720
            },
            {
                "id": 1,
                "name": "ReportSection_CompensationFlightRisk",
                "displayName": "Compensation & Flight Risk Deep Dive",
                "filters": "[]",
                "ordinal": 1,
                "visualContainers": [
                    {
                        "x": 20, "y": 15, "z": 1000, "width": 1240, "height": 45,
                        "config": json.dumps({
                            "name": "HeaderVisual_HR_P2",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Workforce Compensation Benchmarking & Flight Risk Analysis",
                                                    "textStyle": {"fontFamily": "Segoe UI", "fontSize": "18pt", "fontWeight": "bold", "color": "#1A365D"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20, "y": 70, "z": 2000, "width": 300, "height": 95,
                        "config": json.dumps({
                            "name": "Card_FlightRisk",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.High Performer Flight Risk Count"}]}
                            }
                        })
                    },
                    {
                        "x": 340, "y": 70, "z": 2001, "width": 300, "height": 95,
                        "config": json.dumps({
                            "name": "Card_OvertimeAttrition",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Overtime Attrition Rate %"}]}
                            }
                        })
                    },
                    {
                        "x": 660, "y": 70, "z": 2002, "width": 300, "height": 95,
                        "config": json.dumps({
                            "name": "Card_NonOvertimeAttrition",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Non-Overtime Attrition Rate %"}]}
                            }
                        })
                    },
                    {
                        "x": 980, "y": 70, "z": 2003, "width": 280, "height": 95,
                        "config": json.dumps({
                            "name": "Card_LowSatCount",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Fields": [{"queryRef": "_HR_Measures.Low Satisfaction Headcount"}]}
                            }
                        })
                    },
                    {
                        "x": 20, "y": 180, "z": 3000, "width": 750, "height": 520,
                        "config": json.dumps({
                            "name": "RoleAttritionMatrix",
                            "singleVisual": {
                                "visualType": "pivotTable",
                                "projections": {
                                    "Rows": [{"queryRef": "Fact_Employees.Department"}, {"queryRef": "Fact_Employees.Job_Role"}],
                                    "Values": [
                                        {"queryRef": "_HR_Measures.Total Headcount"},
                                        {"queryRef": "_HR_Measures.Departed Employees"},
                                        {"queryRef": "_HR_Measures.Attrition Rate %"},
                                        {"queryRef": "_HR_Measures.Average Monthly Income"},
                                        {"queryRef": "_HR_Measures.Average Job Satisfaction"}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 790, "y": 180, "z": 3001, "width": 470, "height": 520,
                        "config": json.dumps({
                            "name": "SalaryVsSatisfactionScatter",
                            "singleVisual": {
                                "visualType": "scatterChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Employees.Job_Role"}],
                                    "X": [{"queryRef": "_HR_Measures.Average Monthly Income"}],
                                    "Y": [{"queryRef": "_HR_Measures.Average Job Satisfaction"}],
                                    "Size": [{"queryRef": "_HR_Measures.Total Headcount"}]
                                }
                            }
                        })
                    }
                ],
                "config": json.dumps({}),
                "width": 1280,
                "height": 720
            }
        ],
        "config": json.dumps({"version": "5.50", "themeCollection": {"baseTheme": {"name": "CY24SU02", "version": "5.50"}}})
    }
    return layout

def main():
    base_dir = r"C:\Users\shakj\Documents\data-analytics-portfolio\power-bi\hr-analytics-powerbi"
    model = generate_hr_model()
    layout = generate_hr_report_layout()
    
    # 1. PBIP Structure
    pbip_file = os.path.join(base_dir, "hr-analytics-dashboard.pbip")
    sem_dir = os.path.join(base_dir, "hr-analytics-dashboard.SemanticModel")
    rep_dir = os.path.join(base_dir, "hr-analytics-dashboard.Report")
    
    os.makedirs(sem_dir, exist_ok=True)
    os.makedirs(rep_dir, exist_ok=True)
    
    pbip_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "hr-analytics-dashboard.Report"
                }
            }
        ],
        "settings": {
            "enableAutoRecovery": True
        }
    }
    with open(pbip_file, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
        
    pbir_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/1.0.0/schema.json",
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": "../hr-analytics-dashboard.SemanticModel"
            }
        }
    }
    with open(os.path.join(rep_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_content, f, indent=2)
        
    with open(os.path.join(rep_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)
        
    pbism_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "1.0"
    }
    with open(os.path.join(sem_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump(pbism_content, f, indent=2)
        
    with open(os.path.join(sem_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
        
    print(f"Created HR PBIP files at {pbip_file}")
    
    # 2. PBIT Template Structure
    pbit_file = os.path.join(base_dir, "hr-analytics-dashboard.pbit")
    
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="" />
  <Override PartName="/Version" ContentType="" />
  <Override PartName="/Settings" ContentType="" />
  <Override PartName="/DataModelSchema" ContentType="" />
  <Override PartName="/Report/Layout" ContentType="" />
</Types>"""

    with zipfile.ZipFile(pbit_file, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml.encode("utf-8"))
        z.writestr("Version", "1.28".encode("utf-16le"))
        z.writestr("Settings", json.dumps({"Version": 3}).encode("utf-16le"))
        z.writestr("DataModelSchema", json.dumps(model).encode("utf-16le"))
        z.writestr("Report/Layout", json.dumps(layout).encode("utf-16le"))
        
    print(f"Created HR PBIT template at {pbit_file}")

if __name__ == "__main__":
    main()
