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

# ==============================================================================
# Visual Builder Helper Functions with Complete PrototypeQuery & Projections
# ==============================================================================

def make_textbox(name, x, y, width, height, z, text, font_size="15pt"):
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [{
                                "value": text,
                                "textStyle": {"fontFamily": "Segoe UI", "fontSize": font_size, "fontWeight": "bold", "color": "#1A365D"}
                            }]
                        }]
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_card(name, x, y, width, height, z, table_name, measure_name):
    q_ref = f"{table_name}.{measure_name}"
    alias = "m"
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{"queryRef": q_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": alias, "Entity": table_name, "Type": 0}],
                "Select": [{
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": alias}},
                        "Property": measure_name
                    },
                    "Name": q_ref
                }]
            },
            "objects": {
                "labels": [{
                    "properties": {
                        "fontSize": {"expr": {"Literal": {"Value": "20D"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryLabels": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "10D"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#64748B'"}}}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_slicer(name, x, y, width, height, z, table_name, col_name, title_text=None):
    q_ref = f"{table_name}.{col_name}"
    alias = "s"
    objects = {
        "data": [{
            "properties": {
                "mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}
            }
        }],
        "header": [{
            "properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
            }
        }],
        "items": [{
            "properties": {
                "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
            }
        }]
    }
    if title_text:
        objects["header"][0]["properties"]["titleText"] = {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [{"queryRef": q_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": alias, "Entity": table_name, "Type": 0}],
                "Select": [{
                    "Column": {
                        "Expression": {"SourceRef": {"Source": alias}},
                        "Property": col_name
                    },
                    "Name": q_ref
                }]
            },
            "objects": objects
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_bar_chart(name, x, y, width, height, z, cat_table, cat_col, measure_table, measures, title_text="Attrition Rate % by Department"):
    cat_ref = f"{cat_table}.{cat_col}"
    projections = {
        "Category": [{"queryRef": cat_ref, "active": True}],
        "Y": [{"queryRef": f"{measure_table}.{m}"} for m in measures]
    }
    select_items = [{
        "Column": {
            "Expression": {"SourceRef": {"Source": "c"}},
            "Property": cat_col
        },
        "Name": cat_ref
    }]
    for m in measures:
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": m
            },
            "Name": f"{measure_table}.{m}"
        })
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "clusteredBarChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "m", "Entity": measure_table, "Type": 0}
                ],
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryAxis": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
                    }
                }],
                "valueAxis": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_column_chart(name, x, y, width, height, z, cat_table, cat_col, measure_table, measures, title_text="Attrition Rate % by Tenure Cohort"):
    cat_ref = f"{cat_table}.{cat_col}"
    projections = {
        "Category": [{"queryRef": cat_ref, "active": True}],
        "Y": [{"queryRef": f"{measure_table}.{m}"} for m in measures]
    }
    select_items = [{
        "Column": {
            "Expression": {"SourceRef": {"Source": "c"}},
            "Property": cat_col
        },
        "Name": cat_ref
    }]
    for m in measures:
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": m
            },
            "Name": f"{measure_table}.{m}"
        })
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "clusteredColumnChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "m", "Entity": measure_table, "Type": 0}
                ],
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryAxis": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
                    }
                }],
                "valueAxis": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_donut_chart(name, x, y, width, height, z, cat_table, cat_col, measure_table, measure_name, title_text="Departed Employees by Overtime Requirement"):
    cat_ref = f"{cat_table}.{cat_col}"
    m_ref = f"{measure_table}.{measure_name}"
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "pieChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": m_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_table, "Type": 0},
                    {"Name": "m", "Entity": measure_table, "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": cat_col
                        },
                        "Name": cat_ref
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "m"}},
                            "Property": measure_name
                        },
                        "Name": m_ref
                    }
                ]
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "legend": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "position": {"expr": {"Literal": {"Value": "'Right'"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_table(name, x, y, width, height, z, from_tables, fields, title_text=None):
    from_map = {tbl: f"t{i}" for i, tbl in enumerate(from_tables)}
    from_list = [{"Name": alias, "Entity": tbl, "Type": 0} for tbl, alias in from_map.items()]
    projections = {
        "Values": [{"queryRef": f"{tbl}.{prop}"} for tbl, prop, is_m in fields]
    }
    select_items = []
    for tbl, prop, is_m in fields:
        alias = from_map[tbl]
        q_ref = f"{tbl}.{prop}"
        if is_m:
            select_items.append({
                "Measure": {
                    "Expression": {"SourceRef": {"Source": alias}},
                    "Property": prop
                },
                "Name": q_ref
            })
        else:
            select_items.append({
                "Column": {
                    "Expression": {"SourceRef": {"Source": alias}},
                    "Property": prop
                },
                "Name": q_ref
            })
    objects = {
        "stylePreset": [{
            "properties": {
                "name": {"expr": {"Literal": {"Value": "'Condensed'"}}}
            }
        }],
        "values": [{
            "properties": {
                "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
                "wordWrap": {"expr": {"Literal": {"Value": "true"}}}
            }
        }],
        "columnHeaders": [{
            "properties": {
                "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
                "wordWrap": {"expr": {"Literal": {"Value": "true"}}},
                "autoSizeColumnWidth": {"expr": {"Literal": {"Value": "true"}}}
            }
        }]
    }
    if title_text:
        objects["title"] = [{
            "properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
                "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
            }
        }]
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "tableEx",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_items
            },
            "objects": objects
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_matrix(name, x, y, width, height, z, row_fields, value_measures, title_text="Department & Job Role Attrition Matrix"):
    projections = {
        "Rows": [{"queryRef": f"{tbl}.{prop}"} for tbl, prop in row_fields],
        "Values": [{"queryRef": f"_HR_Measures.{m}"} for m in value_measures]
    }
    from_list = [
        {"Name": "e", "Entity": "Fact_Employees", "Type": 0},
        {"Name": "m", "Entity": "_HR_Measures", "Type": 0}
    ]
    select_items = []
    for tbl, prop in row_fields:
        select_items.append({
            "Column": {
                "Expression": {"SourceRef": {"Source": "e"}},
                "Property": prop
            },
            "Name": f"{tbl}.{prop}"
        })
    for m in value_measures:
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": m
            },
            "Name": f"_HR_Measures.{m}"
        })
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "pivotTable",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "rowHeaders": [{
                    "properties": {
                        "stepped": {"expr": {"Literal": {"Value": "false"}}},
                        "showExpandCollapseButtons": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }],
                "subTotals": [{
                    "properties": {
                        "rowSubtotals": {"expr": {"Literal": {"Value": "true"}}},
                        "perRowLevel": {"expr": {"Literal": {"Value": "true"}}},
                        "grandTotal": {"expr": {"Literal": {"Value": "true"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

def make_scatter(name, x, y, width, height, z, cat_table, cat_col, x_measure, y_measure, size_measure, title_text="Income vs. Job Satisfaction by Job Role"):
    projections = {
        "Category": [{"queryRef": f"{cat_table}.{cat_col}"}],
        "X": [{"queryRef": f"_HR_Measures.{x_measure}"}],
        "Y": [{"queryRef": f"_HR_Measures.{y_measure}"}],
        "Size": [{"queryRef": f"_HR_Measures.{size_measure}"}]
    }
    from_list = [
        {"Name": "e", "Entity": cat_table, "Type": 0},
        {"Name": "m", "Entity": "_HR_Measures", "Type": 0}
    ]
    select_items = [
        {
            "Column": {
                "Expression": {"SourceRef": {"Source": "e"}},
                "Property": cat_col
            },
            "Name": f"{cat_table}.{cat_col}"
        },
        {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": x_measure
            },
            "Name": f"_HR_Measures.{x_measure}"
        },
        {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": y_measure
            },
            "Name": f"_HR_Measures.{y_measure}"
        },
        {
            "Measure": {
                "Expression": {"SourceRef": {"Source": "m"}},
                "Property": size_measure
            },
            "Name": f"_HR_Measures.{size_measure}"
        }
    ]
    config = {
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": width, "height": height}}],
        "singleVisual": {
            "visualType": "scatterChart",
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": from_list,
                "Select": select_items
            },
            "objects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}},
                        "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1A365D'"}}}}}
                    }
                }],
                "categoryAxis": [{
                    "properties": {
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "axisTitle": {"expr": {"Literal": {"Value": f"'{x_measure}'"}}}
                    }
                }],
                "valueAxis": [{
                    "properties": {
                        "showAxisTitle": {"expr": {"Literal": {"Value": "true"}}},
                        "axisTitle": {"expr": {"Literal": {"Value": f"'{y_measure}'"}}}
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": z, "width": width, "height": height, "config": json.dumps(config), "filters": "[]"}

# ==============================================================================
# Complete Report Layout Generation with Non-Overlapping Geometry
# ==============================================================================

def generate_hr_report_layout():
    # Page 1 Visuals: Executive Workforce & Turnover Overview (Canvas: 1280 x 720)
    p1_visuals = [
        # Header (y: 8, h: 36)
        make_textbox("HeaderVisual_HR", 20, 8, 1240, 36, 1000, "Workforce Demographics & Attrition Executive Dashboard", "14pt"),
        
        # Slicers Row (y: 48, h: 70)
        make_slicer("Slicer_Department", 20, 48, 220, 70, 1500, "Fact_Employees", "Department", "Department"),
        make_slicer("Slicer_Gender", 260, 48, 200, 70, 1501, "Fact_Employees", "Gender", "Gender"),
        make_slicer("Slicer_JobRole", 480, 48, 260, 70, 1502, "Fact_Employees", "Job_Role", "Job Role"),
        make_slicer("Slicer_AgeGroup", 760, 48, 220, 70, 1503, "Fact_Employees", "Age Group", "Age Group"),
        
        # Executive KPI Cards (y: 130, h: 82, gap 12px from slicers)
        make_card("Card_TotalHeadcount", 20, 130, 236, 82, 2000, "_HR_Measures", "Total Headcount"),
        make_card("Card_ActiveHeadcount", 271, 130, 236, 82, 2001, "_HR_Measures", "Active Headcount"),
        make_card("Card_Departed", 522, 130, 236, 82, 2002, "_HR_Measures", "Departed Employees"),
        make_card("Card_AttritionRate", 773, 130, 236, 82, 2003, "_HR_Measures", "Attrition Rate %"),
        make_card("Card_AvgIncome", 1024, 130, 236, 82, 2004, "_HR_Measures", "Average Monthly Income"),
        
        # Charts Row 1 (y: 228, h: 224, gap 16px from KPIs)
        make_bar_chart("DeptAttritionBarChart", 20, 228, 600, 224, 3000, "Fact_Employees", "Department", "_HR_Measures", ["Attrition Rate %"], "Attrition Rate % by Department"),
        make_column_chart("TenureCohortColumnChart", 635, 228, 625, 224, 3001, "Fact_Employees", "Tenure Cohort", "_HR_Measures", ["Attrition Rate %"], "Attrition Rate % by Company Tenure Cohort"),
        
        # Charts Row 2 (y: 468, h: 236, gap 16px from Row 1)
        make_donut_chart("OvertimeDonutChart", 20, 468, 420, 236, 3002, "Fact_Employees", "Overtime", "_HR_Measures", "Departed Employees", "Departed Employees by Overtime Requirement"),
        make_table("DeptSummaryTable", 455, 468, 805, 236, 3003, ["Fact_Employees", "_HR_Measures"], [
            ("Fact_Employees", "Department", False),
            ("_HR_Measures", "Total Headcount", True),
            ("_HR_Measures", "Departed Employees", True),
            ("_HR_Measures", "Active Headcount", True),
            ("_HR_Measures", "Attrition Rate %", True),
            ("_HR_Measures", "Average Monthly Income", True),
            ("_HR_Measures", "Average Job Satisfaction", True)
        ], "Departmental Workforce & Turnover Summary")
    ]
    
    # Page 2 Visuals: Compensation & Flight Risk Deep Dive (Canvas: 1280 x 720)
    p2_visuals = [
        # Header (y: 10, h: 40)
        make_textbox("HeaderVisual_HR_P2", 20, 10, 1240, 40, 1000, "Workforce Compensation Benchmarking & Flight Risk Analysis", "15pt"),
        
        # KPI Cards (y: 60, h: 86)
        make_card("Card_FlightRisk", 20, 60, 295, 86, 2000, "_HR_Measures", "High Performer Flight Risk Count"),
        make_card("Card_OvertimeAttrition", 335, 60, 295, 86, 2001, "_HR_Measures", "Overtime Attrition Rate %"),
        make_card("Card_NonOvertimeAttrition", 650, 60, 295, 86, 2002, "_HR_Measures", "Non-Overtime Attrition Rate %"),
        make_card("Card_LowSatCount", 965, 60, 295, 86, 2003, "_HR_Measures", "Low Satisfaction Headcount"),
        
        # Middle Row (y: 162, h: 265, gap 16px from KPIs)
        make_matrix("RoleAttritionMatrix", 20, 162, 740, 265, 3000, [
            ("Fact_Employees", "Department"),
            ("Fact_Employees", "Job_Role")
        ], ["Total Headcount", "Departed Employees", "Attrition Rate %", "Average Monthly Income", "Average Job Satisfaction"], "Department & Job Role Attrition Matrix"),
        make_scatter("SalaryVsSatisfactionScatter", 780, 162, 480, 265, 3001, "Fact_Employees", "Job_Role", "Average Monthly Income", "Average Job Satisfaction", "Total Headcount", "Income vs. Job Satisfaction by Job Role"),
        
        # Bottom Row (y: 445, h: 260, gap 18px from Middle Row)
        make_table("HighRiskEmployeeTable", 20, 445, 1240, 260, 3002, ["Fact_Employees"], [
            ("Fact_Employees", "Employee_ID", False),
            ("Fact_Employees", "Department", False),
            ("Fact_Employees", "Job_Role", False),
            ("Fact_Employees", "Age", False),
            ("Fact_Employees", "Years_at_Company", False),
            ("Fact_Employees", "Monthly_Income", False),
            ("Fact_Employees", "Job_Satisfaction", False),
            ("Fact_Employees", "Performance_Rating", False),
            ("Fact_Employees", "Overtime", False),
            ("Fact_Employees", "Attrition", False)
        ], "High-Risk Talent Roster & Flight Risk Indicators")
    ]
    
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
                "visualContainers": p1_visuals,
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
                "visualContainers": p2_visuals,
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
