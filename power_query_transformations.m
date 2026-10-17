// =============================================================================
// Power Query (M) Scripts: HR Analytics & Workforce Attrition Data Model
// Target: Power BI Desktop Advanced Editor
// =============================================================================

// -----------------------------------------------------------------------------
// SCRIPT 1: Fact_Employees Ingestion & Clean Type Assignment
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("data/employee_attrition_dataset.csv"), [Delimiter=",", Columns=26, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"Employee_ID", Int64.Type}, 
        {"Age", Int64.Type}, 
        {"Gender", type text}, 
        {"Marital_Status", type text}, 
        {"Department", type text}, 
        {"Job_Role", type text}, 
        {"Job_Level", Int64.Type}, 
        {"Monthly_Income", type number}, 
        {"Hourly_Rate", type number}, 
        {"Years_at_Company", Int64.Type}, 
        {"Years_in_Current_Role", Int64.Type}, 
        {"Years_Since_Last_Promotion", Int64.Type}, 
        {"Work_Life_Balance", Int64.Type}, 
        {"Job_Satisfaction", Int64.Type}, 
        {"Performance_Rating", Int64.Type}, 
        {"Training_Hours_Last_Year", Int64.Type}, 
        {"Overtime", type text}, 
        {"Project_Count", Int64.Type}, 
        {"Average_Hours_Worked_Per_Week", type number}, 
        {"Absenteeism", Int64.Type}, 
        {"Work_Environment_Satisfaction", Int64.Type}, 
        {"Relationship_with_Manager", Int64.Type}, 
        {"Job_Involvement", Int64.Type}, 
        {"Distance_From_Home", Int64.Type}, 
        {"Number_of_Companies_Worked", Int64.Type}, 
        {"Attrition", type text}
    }),
    
    // Add Categorical Age Bracket
    AddAgeGroup = Table.AddColumn(ChangeTypes, "Age Group", each 
        if [Age] < 30 then "Under 30"
        else if [Age] <= 39 then "30 - 39"
        else if [Age] <= 49 then "40 - 49"
        else "50+", type text),

    // Add Tenure Cohort
    AddTenureCohort = Table.AddColumn(AddAgeGroup, "Tenure Cohort", each 
        if [Years_at_Company] < 2 then "0 - 1 Years"
        else if [Years_at_Company] <= 5 then "2 - 5 Years"
        else if [Years_at_Company] <= 10 then "6 - 10 Years"
        else "10+ Years", type text),

    // Add Surrogate Keys for Dimension Linking
    AddDeptRoleKey = Table.AddColumn(AddTenureCohort, "Department_Role_Key", each [Department] & "-" & [Job_Role], type text)
in
    AddDeptRoleKey
