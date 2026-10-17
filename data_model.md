# Power BI Data Model Architecture: HR Analytics & Workforce Attrition

The HR Analytics dashboard is structured around an optimized **People Analytics Schema** designed for departmental drill-downs, turnover cohort analysis, and compensation benchmarking.

```mermaid
erDiagram
    DIM_DEPARTMENT_ROLE ||--o{ FACT_EMPLOYEES : categorizes
    DIM_DEMOGRAPHICS ||--o{ FACT_EMPLOYEES : profiles
    DIM_TENURE_COHORTS ||--o{ FACT_EMPLOYEES : groups

    FACT_EMPLOYEES {
        int Employee_ID PK
        string Department_Role_Key FK
        string Demographic_Key FK
        int Job_Level
        decimal Monthly_Income
        decimal Hourly_Rate
        int Years_at_Company
        int Years_in_Current_Role
        int Years_Since_Last_Promotion
        int Job_Satisfaction
        int Work_Life_Balance
        int Performance_Rating
        int Training_Hours_Last_Year
        string Overtime
        int Project_Count
        decimal Average_Hours_Worked_Per_Week
        int Absenteeism
        string Attrition
    }

    DIM_DEPARTMENT_ROLE {
        string Department_Role_Key PK
        string Department
        string Job_Role
    }

    DIM_DEMOGRAPHICS {
        string Demographic_Key PK
        string Gender
        string Marital_Status
        string Age_Group
    }

    DIM_TENURE_COHORTS {
        string Tenure_Band PK
        int Min_Years
        int Max_Years
    }
```

---

## Relationship Specifications
1. **`Dim_Department_Role[Department_Role_Key]` $\xrightarrow{1:M}$ `Fact_Employees[Department_Role_Key]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single
2. **`Dim_Demographics[Demographic_Key]` $\xrightarrow{1:M}$ `Fact_Employees[Demographic_Key]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single
3. **`Dim_Tenure_Cohorts[Tenure_Band]` $\xrightarrow{1:M}$ `Fact_Employees[Tenure_Band]`**
   - Cardinality: One-to-Many ($1:*$)
   - Cross-filter direction: Single
