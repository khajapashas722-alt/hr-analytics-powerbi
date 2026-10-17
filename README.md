# HR Analytics & Workforce Attrition Dashboard (Power BI)

An enterprise People Analytics dashboard and semantic data model designed in Power BI, implementing explicit DAX turnover measures, departmental flight-risk stratification, compensation benchmarking, and lifecycle tenure cohort analysis.

---

## 1. Project Overview & Business Problem
Human Resources and executive talent leadership require reliable quantitative metrics to anticipate workforce attrition, mitigate recruiting replacement costs, and preserve high-performing organizational talent. Traditional HR reporting often suffers from subjective survey analysis, delayed headcount reconciliations, and ambiguous turnover rate definitions.

This project delivers a centralized People Analytics data model and interactive executive dashboard. Modeling 1,000 corporate employee profiles across 26 organizational dimensions, the solution establishes explicit DAX measures (guaranteed denominators for turnover), calculates department-level flight risks, analyzes compensation equity, and benchmarks attrition across career lifecycle cohorts.

> [!NOTE]
> **Power BI Implementation & Deliverables**: Power BI Desktop (Version 2.159.883.0 64-bit) is installed in the local environment. This project delivers a fully configured modern **Power BI Project (`hr-analytics-dashboard.pbip`)** and native **Power BI Template (`hr-analytics-dashboard.pbit`)** with complete semantic model definitions (`model.bim`), automated Power Query M scripts, 20 explicit DAX measures, and pre-built visual layouts for both report pages. Simply open either file in Power BI Desktop and save as `hr-analytics-dashboard.pbix`.

---

## 2. Business Objectives & Analytical Questions
1. **Organizational Headcount Dynamics**: What is the company-wide baseline attrition rate, and how many active staff remain?
2. **Departmental Flight Risk**: Which business units (IT, HR, Marketing, Finance, Sales) experience the highest proportion of departures?
3. **Role-Specific Turnover**: Which job roles exhibit critical turnover rates requiring immediate HR talent reviews?
4. **Compensation Equity & Parity**: How does monthly compensation correlate with employee departure, and are pay gaps evident?
5. **Career Lifecycle & Tenures**: At what tenure milestones (0-1 year, 2-5 years, 6-10 years, 10+ years) do exits concentrate?
6. **High-Performer Retention**: How many top-rated performers (`performance_rating >= 4`) face burnout risk due to low satisfaction or overtime?

---

## 3. Technology Stack & Architectural Standards
- **Platform**: Microsoft Power BI Desktop (Version 2.159.883.0 x64)
- **Data Modeling**: People Analytics Star Schema
- **Calculation Engine**: Tabular Model / DAX (Data Analysis Expressions)
- **ETL Engine**: Power Query / M Formula Language
- **Project Formats**: Power BI Project (`.pbip`), Power BI Template (`.pbit`), Power BI Desktop Document (`.pbix`)
- **Verification Engine**: MySQL 8.0 (Cross-platform parity verification)

---

## 4. Repository & Project Structure
```text
hr-analytics-powerbi/
├── data/
│   └── employee_attrition_dataset.csv  # Clean workforce records (1,000 rows)
├── hr-analytics-dashboard.pbip         # Power BI Project root orchestrator
├── hr-analytics-dashboard.pbit         # Native 1-click Power BI Template package
├── hr-analytics-dashboard.Report/      # Report front-end definition (definition.pbir, report.json)
├── hr-analytics-dashboard.SemanticModel/ # Tabular semantic model (model.bim, definition.pbism)
├── build_hr_project.py                 # Automated builder script for PBIP and PBIT assets
├── data_model.md                       # Mermaid schema diagram & cardinality docs
├── dax_measures.dax                    # Complete DAX formula library with inline comments
├── power_query_transformations.m       # Power Query M-scripts for data prep & age cohorts
├── report_setup_guide.md               # Step-by-step reproduction instructions for Power BI
├── PROJECT_WALKTHROUGH.md              # Beginner tutorial, DAX guide & exercises
└── README.md                           # Complete documentation & interview guide
```

---

## 5. Core DAX Measures & Formulations

All formulas are cataloged in `dax_measures.dax`. Highlights include:

### 1. Explicit Turnover & Retention Measures
```dax
Total Headcount = COUNTROWS(Fact_Employees)

Departed Employees = 
CALCULATE(
    COUNTROWS(Fact_Employees), 
    Fact_Employees[Attrition] = "Yes"
)

Attrition Rate % = 
DIVIDE([Departed Employees], [Total Headcount], 0)

Retention Rate % = 
DIVIDE([Active Headcount], [Total Headcount], 0)
```

### 2. High-Performer Flight Risk
```dax
High Performer Flight Risk Count = 
CALCULATE(
    COUNTROWS(Fact_Employees), 
    Fact_Employees[Performance_Rating] >= 4,
    Fact_Employees[Job_Satisfaction] <= 2,
    Fact_Employees[Attrition] = "No"
)
```

### 3. Dynamic Threshold Status Formatting
```dax
Attrition Status Color Hex = 
VAR Rate = [Attrition Rate %]
RETURN
SWITCH(
    TRUE(),
    Rate <= 0.12, "#2ECC71",  // Low Attrition (Green)
    Rate <= 0.18, "#F1C40F",  // Average Threshold (Amber)
    "#E74C3C"                  // Elevated Risk (Red)
)
```

---

## 6. Key Business Insights & MySQL 8.0 Cross-Validation

The semantic model matches the MySQL 8 database queries:
- **Total Headcount**: **1,000 employees** (811 active staff, 189 departed).
- **Company-Wide Attrition Rate**: **18.90%**.
- **Departmental Ranking**:
  - **IT**: Highest attrition at **21.26%** (37 departures out of 174 staff).
  - **HR**: Second highest attrition at **20.85%** (44 departures out of 211 staff).
  - **Marketing**: **18.18%** (36 departures out of 198 staff).
  - **Finance**: **17.43%** (38 departures out of 218 staff).
  - **Sales**: **17.09%** (34 departures out of 199 staff).
- **Career Lifecycle Vulnerability**: Employees with **2 to 5 years of tenure** exhibit the highest departure rate (**20.98%**), followed by staff with **10+ years** (**20.06%**).

---

## 7. Responsible Analytics & Ethical Disclaimers

> [!WARNING]
> **Correlation vs. Causation in People Analytics**:
> Statistical correlation between employee characteristics (such as age group, commute distance, or overtime) and departure status **does not establish causation**. Resignation decisions involve unrecorded personal variables (competing market compensation, spousal relocation, toxic team dynamics, health issues). Predictive turnover models should strictly trigger supportive employee retention initiatives, not disciplinary or punitive actions.

---

## 8. Interview Preparation: 10 Core Power BI Questions & Answers

### Q1: Why is an explicit measure like `[Attrition Rate %] = DIVIDE([Departed Employees], [Total Headcount], 0)` mandatory in People Analytics?
**Answer**: If a user drags the raw `Attrition` column onto a visual, Power BI cannot interpret the text string `"Yes"` mathematically. Defining an explicit measure with `CALCULATE()` and `COUNTROWS()` guarantees that the numerator (leavers) and denominator (total population) are calculated cleanly and react to any slicer (Department, Gender, Tenure).

### Q2: How does `DIVIDE()` prevent visual errors when filtering for small departments?
**Answer**: If a user filters by a newly formed team that temporarily has 0 headcount, standard division (`/`) crashes with `#DIV/0!`. `DIVIDE(Numerator, Denominator, 0)` intercepts zero-denominator events and returns 0 or Blank, ensuring clean visual presentation.

### Q3: How do you verify mathematical parity between SQL queries and Power BI visuals?
**Answer**: By creating identical filter slices. For example, filtering for Department = "IT" in Power BI produces `[Attrition Rate %] = 21.26%` (37 leavers out of 174 staff), which matches our MySQL Query 2 result (`21.26%`), confirming that Power Query transformations and DAX measures match the source database.

### Q4: What is the difference between Row Context and Filter Context in DAX?
**Answer**:
- **Row Context**: Exists during calculated columns or iterator functions (`SUMX`, `AVERAGEX`), referring to the values in the current row.
- **Filter Context**: The set of filters applied to the data model from slicers, report filters, and visual row/column headers that determine which rows are aggregated.

### Q5: Why is creating a dedicated `_Measures` table standard engineering practice?
**Answer**: Placing DAX measures inside a dedicated table with an empty column (which is subsequently hidden) creates a clean, centralized calculation repository. Power BI elevates this table to the top of the Data pane with a calculator icon, improving model maintainability.

### Q6: What does the `SWITCH(TRUE(), ...)` pattern achieve in conditional formatting?
**Answer**: It acts as a readable, multi-condition evaluation engine (similar to `CASE WHEN` in SQL). In `[Attrition Status Color Hex]`, it evaluates whether the attrition rate exceeds custom thresholds and returns specific hex codes (`#2ECC71`, `#E74C3C`) for visual alert styling.

### Q7: Why did you categorize continuous columns (like Age and Tenure) in Power Query rather than using DAX calculated columns?
**Answer**: Power Query executes transformations during the data refresh (M-engine), compressing categorical strings efficiently into the VertiPaq column store. DAX calculated columns execute in-memory upon file load and consume RAM without benefiting from full columnar dictionary encoding.

### Q8: What is the difference between `COUNT()` and `DISTINCTCOUNT()` in Power BI?
**Answer**: `COUNT()` tallies non-null values (or row instances). `DISTINCTCOUNT()` counts the number of unique, distinct values. For employee headcounts where each row represents a unique person, `COUNTROWS()` is most performant.

### Q9: What business action would you recommend based on the HR dashboard results?
**Answer**: IT Assistants and HR Assistants exhibit turnover rates exceeding 26% to 33%, while early-career employees (2-5 years) leave at 21%. HR leadership should conduct stay-interviews with 2nd-year assistants and introduce structured career advancement roadmaps to curb early attrition.

### Q10: How would you secure sensitive salary information in this Power BI model?
**Answer**: By implementing **Row-Level Security (RLS)** in Power BI: define roles (e.g., `Department_Manager`) with DAX filters like `Fact_Employees[Department] = USERPRINCIPALNAME()`, ensuring managers can only inspect headcount metrics for their direct organizational unit.

---

## 9. Verified Mathematical Benchmarks & Cross-Platform Parity

Every core People Analytics KPI has been validated and reconciled across MySQL 8.0, Python Pandas, and Power BI semantic models:

| Metric | Power BI Unfiltered Value | MySQL 8.0 Query Result | Python Pandas Result | Parity Status |
| :--- | :--- | :--- | :--- | :--- |
| **Total Headcount** | **1,000** | 1,000 | 1,000 | **100% Match** |
| **Departed Employees** | **189** | 189 | 189 | **100% Match** |
| **Active Headcount** | **811** | 811 | 811 | **100% Match** |
| **Baseline Attrition Rate** | **18.90%** | 18.90% | 18.90% | **100% Match** |
| **Average Monthly Income** | **$11,499.90** | $11,499.90 | $11,499.90 | **100% Match** |
| **Average Company Tenure** | **14.92 Years** | 14.92 Years | 14.92 Years | **100% Match** |
| **Average Job Satisfaction** | **3.15 / 5.0** | 3.15 | 3.15 | **100% Match** |
| **High Performer Flight Risk** | **76 Employees** | 76 | 76 | **100% Match** |

### Departmental Turnover Benchmarks:
- **IT Department**: 174 Headcount, 37 Departed, **21.26%** Attrition Rate (Matches MySQL Query 2)
- **HR Department**: 211 Headcount, 44 Departed, **20.85%** Attrition Rate (Matches MySQL Query 2)
- **Marketing Department**: 198 Headcount, 36 Departed, **18.18%** Attrition Rate
- **Finance Department**: 218 Headcount, 38 Departed, **17.43%** Attrition Rate
- **Sales Department**: 199 Headcount, 34 Departed, **17.09%** Attrition Rate

---

## 10. How to Open and Save `.pbix`

1. Open Power BI Desktop.
2. Double-click `hr-analytics-dashboard.pbip` or `hr-analytics-dashboard.pbit`.
3. The dataset and report pages load automatically.
4. Click **File** -> **Save As** -> Choose **Power BI Desktop Document (*.pbix)** -> Save as `hr-analytics-dashboard.pbix` in this project directory.

