# Power BI Setup & Assembly Guide: HR Analytics Dashboard

This guide walks through opening, assembling, and publishing the Human Resources & Workforce Attrition dashboard in **Power BI Desktop**.

---

## Fast-Track: Open via Power BI Project (`.pbip`) or Template (`.pbit`)

Both native formats are pre-built and ready in this directory:
1. **Option A (Modern Power BI Project)**: Double-click `hr-analytics-dashboard.pbip`. Power BI Desktop loads the project, evaluates the Power Query steps against local CSVs, compiles the model into VertiPaq, and opens both report pages with full visual query bindings.
2. **Option B (Power BI Template)**: Double-click `hr-analytics-dashboard.pbit`. Power BI Desktop loads the template and evaluates queries.
3. **Save as `.pbix`**: In Power BI Desktop, click **File** -> **Save As** -> in the "Save as type" dropdown, explicitly select **Power BI file (*.pbix)** -> save as `hr-analytics-dashboard.pbix` in this project directory.
   > [!IMPORTANT]
   > Ensure "Save as type" is toggled from Power BI Project (*.pbip) to **Power BI file (*.pbix)** to produce a standalone single-file `.pbix` package.

---

## Manual Step-by-Step Scratch Build Instructions

### Step 1: Ingest Data via Power Query
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select `data/employee_attrition_dataset.csv`.
4. Click **Transform Data** to launch Power Query Editor.
5. In the Home ribbon, click **Advanced Editor**.
6. Replace the existing M query with the complete script from `power_query_transformations.m`.
7. Click **Done** -> **Close & Apply**.

---

### Step 2: Establish the Measures Table
1. On the Home ribbon, click **Enter Data**.
2. Name the table `_HR_Measures` and click **Load**.
3. Create each explicit DAX measure from `dax_measures.dax`:
   - Headcount: `Total Headcount`, `Departed Employees`, `Active Headcount`, `Attrition Rate %`, `Retention Rate %`.
   - Compensation & Tenure: `Average Monthly Income`, `Median Monthly Income`, `Average Company Tenure (Years)`, `Average Years in Current Role`, `Average Years Since Last Promotion`, `Average Absenteeism Days`.
   - Well-being & Risk: `Average Job Satisfaction`, `Average Work Life Balance`, `Average Work Environment Satisfaction`, `Low Satisfaction Headcount`, `Overtime Attrition Rate %`, `Non-Overtime Attrition Rate %`, `High Performer Flight Risk Count`, `Department Attrition Rank`, `Attrition Status Color Hex`.
4. Hide `RowKey` so that `_HR_Measures` displays the calculator icon at the top of the Data pane.

---

### Step 3: Configure Report Pages & Visual Layout

#### Page 1: Executive Workforce & Turnover Overview (Canvas: 1280 x 720)
- **Dashboard Header (Y: 8, Height: 36, Width: 1240)**:
  - Text: "Workforce Demographics & Attrition Executive Dashboard" (14pt bold, Segoe UI, `#1A365D`).
- **Top Slicer Bar (Y: 48, Height: 70, Mode: Dropdown)**:
  - Slicer 1: `Fact_Employees[Department]` (X: 20, Width: 220).
  - Slicer 2: `Fact_Employees[Gender]` (X: 260, Width: 200).
  - Slicer 3: `Fact_Employees[Job_Role]` (X: 480, Width: 260).
  - Slicer 4: `Fact_Employees[Age Group]` (X: 760, Width: 220).
- **Executive KPI Cards (Y: 130, Height: 82, Gap from Slicers: 12px)**:
  - Card 1: `_HR_Measures[Total Headcount]` (X: 20, Width: 236, Callout: 20pt, `#1A365D`, Value: 1,000).
  - Card 2: `_HR_Measures[Active Headcount]` (X: 271, Width: 236, Callout: 20pt, Value: 811).
  - Card 3: `_HR_Measures[Departed Employees]` (X: 522, Width: 236, Callout: 20pt, Value: 189).
  - Card 4: `_HR_Measures[Attrition Rate %]` (X: 773, Width: 236, Callout: 20pt, Value: 18.90%).
  - Card 5: `_HR_Measures[Average Monthly Income]` (X: 1024, Width: 236, Callout: 20pt, Value: $11,499.90).
- **Charts Row 1 (Y: 228, Height: 224, Gap from KPIs: 16px)**:
  - **Clustered Bar Chart** (X: 20, Width: 600):
    - Category: `Fact_Employees[Department]`
    - Value: `_HR_Measures[Attrition Rate %]`
    - Title: "Attrition Rate % by Department"
  - **Clustered Column Chart** (X: 635, Width: 625):
    - Category: `Fact_Employees[Tenure Cohort]`
    - Value: `_HR_Measures[Attrition Rate %]`
    - Title: "Attrition Rate % by Company Tenure Cohort"
- **Charts Row 2 (Y: 468, Height: 236, Gap from Row 1: 16px)**:
  - **Donut Chart** (X: 20, Width: 420):
    - Category: `Fact_Employees[Overtime]`
    - Value: `_HR_Measures[Departed Employees]`
    - Legend: Right
    - Title: "Departed Employees by Overtime Requirement"
  - **Department Summary Table** (X: 455, Width: 805, Style: Condensed, Word Wrap: Enabled):
    - Columns: `Fact_Employees[Department]`, `[Total Headcount]`, `[Departed Employees]`, `[Active Headcount]`, `[Attrition Rate %]`, `[Average Monthly Income]`, `[Average Job Satisfaction]`.
    - Title: "Departmental Workforce & Turnover Summary"

#### Page 2: Compensation & Flight Risk Deep Dive (Canvas: 1280 x 720)
- **Header Visual (Y: 10, Height: 40, Width: 1240)**:
  - Text: "Workforce Compensation Benchmarking & Flight Risk Analysis" (15pt bold, `#1A365D`).
- **KPI Cards (Y: 60, Height: 86)**:
  - Card 1: `_HR_Measures[High Performer Flight Risk Count]` (X: 20, Width: 295, Value: 76).
  - Card 2: `_HR_Measures[Overtime Attrition Rate %]` (X: 335, Width: 295, Value: 18.24%).
  - Card 3: `_HR_Measures[Non-Overtime Attrition Rate %]` (X: 650, Width: 295, Value: 19.53%).
  - Card 4: `_HR_Measures[Low Satisfaction Headcount]` (X: 965, Width: 295, Value: 360).
- **Middle Row (Y: 162, Height: 265, Gap from KPIs: 16px)**:
  - **Department & Role Attrition Matrix** (X: 20, Width: 740, Stepped Layout: False, Subtotals: True, Grand Total: True):
    - Rows: `Fact_Employees[Department]`, `Fact_Employees[Job_Role]`
    - Values: `[Total Headcount]`, `[Departed Employees]`, `[Attrition Rate %]`, `[Average Monthly Income]`, `[Average Job Satisfaction]`
    - Title: "Department & Job Role Attrition Matrix"
  - **Scatter Plot (Salary vs. Satisfaction)** (X: 780, Width: 480):
    - Category: `Fact_Employees[Job_Role]`
    - X-Axis: `_HR_Measures[Average Monthly Income]`
    - Y-Axis: `_HR_Measures[Average Job Satisfaction]`
    - Size: `_HR_Measures[Total Headcount]`
    - Title: "Income vs. Job Satisfaction by Job Role"
- **Bottom Row (Y: 445, Height: 260, Gap from Middle Row: 18px)**:
  - **High-Risk Employee Detail Table** (X: 20, Width: 1240, Style: Condensed, Word Wrap: Enabled):
    - Columns: `Employee_ID`, `Department`, `Job_Role`, `Age`, `Years_at_Company`, `Monthly_Income`, `Job_Satisfaction`, `Performance_Rating`, `Overtime`, `Attrition`.
    - Title: "High-Risk Talent Roster & Flight Risk Indicators"

---

## Step 4: Verification Against MySQL 8.0 & Python Benchmark
Confirm semantic parity against our SQL database results:
- Unfiltered `[Total Headcount]` must display exactly **1,000**.
- `[Departed Employees]` must display **189**.
- `[Active Headcount]` must display **811**.
- `[Attrition Rate %]` must display **18.90%**.
- Filtering for Department = "IT" must yield **21.26%** attrition (37 departed staff).
- Filtering for Department = "HR" must yield **20.85%** attrition (44 departed staff).
- Filtering for Department = "Marketing" must yield **18.18%** attrition (36 departed staff).
- Filtering for Department = "Finance" must yield **17.43%** attrition (38 departed staff).
- Filtering for Department = "Sales" must yield **17.09%** attrition (34 departed staff).
This guarantees 100% statistical consistency between MySQL queries, Python tests, and Power BI visuals.
