# Project Walkthrough: HR Analytics Dashboard in Power BI

## 1. High-Level Architecture & Modeling Workflow
```
Employee Master Records (1,000 Employees)
  ──> Power Query Transformations (Age Brackets, Tenure Cohorts)
  ──> Dimensional Schema Modeling (Fact_Employees)
  ──> Dedicated _HR_Measures Calculation Repository
  ──> Core Attrition & Headcount DAX Formulations
  ──> Departmental Stratification & Flight Risk Matrix
  ──> Executive Visual Dashboard & Slicer Configuration
```

---

## 2. Core DAX Formulations Explained

### Explicit Numerator & Denominator Turnover Rate
```dax
Attrition Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Attrition] = "Yes"), 
    COUNTROWS(Fact_Employees), 
    0
)
```
- By explicitly querying `Attrition = "Yes"` in the numerator and total rows in the denominator, this measure calculates dynamically across any department, gender, or tenure slicer on the canvas.

### Flight Risk Compound Logic
```dax
High Performer Flight Risk Count = 
CALCULATE(
    COUNTROWS(Fact_Employees), 
    Fact_Employees[Performance_Rating] >= 4,
    Fact_Employees[Job_Satisfaction] <= 2,
    Fact_Employees[Attrition] = "No"
)
```
- Combines three filter predicates: top performers ($ rating \ge 4$), low satisfaction ($\le 2$), and active status to flag employees at risk of leaving before resignation occurs.

---

## 3. Three Improvements You Can Personally Implement

1. **Implement Row-Level Security (RLS)**:
   - Go to **Modeling** -> **Manage Roles**.
   - Create a role `Sales_Director` with DAX filter `[Department] == "Sales"` so managers see only their departmental data.
2. **Key Influencers AI Visual**:
   - Add Power BI's built-in **Key Influencers** visual to evaluate what factors (Overtime, Years Since Promotion, Income) statistically drive `Attrition` to `"Yes"`.
3. **Automated Tenure Cohort Dynamic Tooltip**:
   - Create a hover tooltip page showing average monthly salary progression across tenure years when hovering over department bars.

---

## 4. Hands-On Practice Exercises
- **Exercise 1**: Write a DAX measure `[Tenure-Adjusted Turnover]` calculating attrition specifically for employees with less than 2 years of company service.
- **Exercise 2**: Write a DAX measure computing the Gender Pay Gap percentage: `DIVIDE([Male Avg Income] - [Female Avg Income], [Male Avg Income], 0)`.
- **Exercise 3**: Build a card visual that conditionally turns yellow when departmental attrition exceeds 20%.
