# Power BI Setup & Assembly Guide: HR Analytics Dashboard

This guide walks through opening, assembling, and publishing the Human Resources & Workforce Attrition dashboard in **Power BI Desktop**.

---

## Fast-Track: Open via Power BI Project (`.pbip`) or Template (`.pbit`)

Both native formats are pre-built and ready in this directory:
1. **Option A (Modern Power BI Project)**: Double-click `hr-analytics-dashboard.pbip`. Power BI Desktop loads the project, evaluates the Power Query steps against local CSVs, compiles the model into VertiPaq, and opens both report pages.
2. **Option B (Power BI Template)**: Double-click `hr-analytics-dashboard.pbit`. Power BI Desktop loads the template and evaluates queries.
3. **Save as `.pbix`**: In Power BI Desktop, click **File** -> **Save As** -> select **Power BI Desktop Document (*.pbix)** -> save as `hr-analytics-dashboard.pbix`.

---

## Manual Step-by-Step Scratch Build Instructions

## Step 1: Ingest Data via Power Query
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select `data/employee_attrition_dataset.csv`.
4. Click **Transform Data** to launch Power Query Editor.
5. In the Home ribbon, click **Advanced Editor**.
6. Replace the existing M query with the complete script from `power_query_transformations.m`.
7. Click **Done** -> **Close & Apply**.

---

## Step 2: Establish the Measures Table
1. On the Home ribbon, click **Enter Data**.
2. Name the table `_HR_Measures` and click **Load**.
3. Create each explicit DAX measure from `dax_measures.dax`:
   - `Total Headcount`, `Departed Employees`, `Active Headcount`, `Attrition Rate %`, `Retention Rate %`.
   - `Average Monthly Income`, `Average Company Tenure (Years)`, `Average Job Satisfaction`.
   - `High Performer Flight Risk Count`, `Department Attrition Rank`.
4. Delete the empty `Column1` so that `_HR_Measures` displays the calculator icon at the top of the Data pane.

---

## Step 3: Configure Report Pages & Visual Layout

### Page 1: Executive Workforce & Turnover Overview (Canvas: 16:9 Standard)
- **Top Slicer Bar (Y: 10, Height: 50)**:
  - Slicer 1: `Fact_Employees[Department]` (Horizontal Tile / Dropdown).
  - Slicer 2: `Fact_Employees[Gender]` (Tile).
  - Slicer 3: `Fact_Employees[Age Group]` (Dropdown).
- **Executive KPI Cards (Y: 70, Height: 90)**:
  - Card 1: `[Total Headcount]` (Formatted as Integer `#,#00`, e.g. `1,000`).
  - Card 2: `[Active Headcount]` (e.g. `811`).
  - Card 3: `[Departed Employees]` (e.g. `189`).
  - Card 4: `[Attrition Rate %]` (e.g. `18.9%`).
  - Card 5: `[Average Monthly Income]` (e.g. `$11,500`).
- **Main Visual Area (Left Side)**:
  - **Clustered Bar Chart**: `[Attrition Rate %]` by `Fact_Employees[Department]`.
    - Data Labels: Enabled (Formatted as `0.0%`).
    - Tooltips: `[Total Headcount]`, `[Departed Employees]`.
- **Main Visual Area (Right Side)**:
  - **Clustered Column Chart**: `[Attrition Rate %]` by `Fact_Employees[Tenure Cohort]` (`0-1 Years`, `2-5 Years`, `6-10 Years`, `10+ Years`).
  - **Donut Chart**: `[Departed Employees]` by `Fact_Employees[Overtime]` (`Yes`, `No`).

### Page 2: Compensation & Flight Risk Deep Dive
- **Matrix Visual**:
  - Rows: `Fact_Employees[Department]`, `Fact_Employees[Job_Role]`
  - Values: `[Total Headcount]`, `[Departed Employees]`, `[Attrition Rate %]`, `[Average Monthly Income]`, `[Average Job Satisfaction]`
  - Conditional Formatting: Background color on `[Attrition Rate %]` using Rules (Red for $> 25\%$, Green for $< 15\%$).
- **Scatter Plot (Salary vs. Satisfaction)**:
  - X-Axis: `Fact_Employees[Monthly_Income]`
  - Y-Axis: `Fact_Employees[Job_Satisfaction]`
  - Legend: `Fact_Employees[Attrition]` (Red = Yes, Green = No)
- **Flight Risk KPI Card**:
  - Card: `[High Performer Flight Risk Count]` displaying top performers with low satisfaction.

---

## Step 4: Verification Against MySQL 8.0 Benchmark
Confirm semantic parity against our SQL database results:
- Unfiltered `[Total Headcount]` must display exactly **1,000**.
- `[Departed Employees]` must display **189**.
- `[Attrition Rate %]` must display **18.90%**.
- Filtering for Department = "IT" must yield **21.26%** attrition (37 departed staff).
- Filtering for Department = "HR" must yield **20.85%** attrition (44 departed staff).
This guarantees 100% statistical consistency between MySQL queries and Power BI visuals.
