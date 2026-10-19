"""
Unit & Parity Test Suite: HR Analytics & Workforce Attrition Data Model
Verifies 100% semantic and mathematical parity against the raw CSV and portfolio benchmarks.
"""

import csv
import os

def test_hr_data_and_benchmarks():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", "employee_attrition_dataset.csv")
    
    assert os.path.exists(csv_path), f"Dataset CSV missing at {csv_path}"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Loaded {len(rows)} employee records.")
    assert len(rows) == 1000, f"Expected 1,000 rows, found {len(rows)}"
    
    # 1. Total Headcount & Attrition
    total_headcount = len(rows)
    departed = [r for r in rows if r["Attrition"] == "Yes"]
    active = [r for r in rows if r["Attrition"] == "No"]
    
    departed_count = len(departed)
    active_count = len(active)
    attrition_rate = departed_count / total_headcount
    retention_rate = active_count / total_headcount
    
    print(f"Total Headcount: {total_headcount} (Expected: 1,000)")
    print(f"Departed Employees: {departed_count} (Expected: 189)")
    print(f"Active Headcount: {active_count} (Expected: 811)")
    print(f"Attrition Rate: {attrition_rate:.2%} (Expected: 18.90%)")
    print(f"Retention Rate: {retention_rate:.2%} (Expected: 81.10%)")
    
    assert total_headcount == 1000
    assert departed_count == 189
    assert active_count == 811
    assert round(attrition_rate, 4) == 0.1890
    assert round(retention_rate, 4) == 0.8110
    
    # 2. Compensation & Tenure
    incomes = [float(r["Monthly_Income"]) for r in rows]
    avg_income = sum(incomes) / len(incomes)
    tenures = [float(r["Years_at_Company"]) for r in rows]
    avg_tenure = sum(tenures) / len(tenures)
    sats = [float(r["Job_Satisfaction"]) for r in rows]
    avg_sat = sum(sats) / len(sats)
    
    print(f"Avg Monthly Income: ${avg_income:,.2f} (Expected: $11,499.90)")
    print(f"Avg Company Tenure: {avg_tenure:.2f} years (Expected: 14.92)")
    print(f"Avg Job Satisfaction: {avg_sat:.2f} (Expected: 3.15)")
    
    assert round(avg_income, 2) == 11499.90
    assert round(avg_tenure, 2) == 14.92
    assert round(avg_sat, 2) == 3.15
    
    # 3. Departmental Breakdown
    dept_benchmarks = {
        "IT": {"total": 174, "departed": 37, "rate": 0.2126},
        "HR": {"total": 211, "departed": 44, "rate": 0.2085},
        "Marketing": {"total": 198, "departed": 36, "rate": 0.1818},
        "Finance": {"total": 218, "departed": 38, "rate": 0.1743},
        "Sales": {"total": 199, "departed": 34, "rate": 0.1709}
    }
    
    for dept, exp in dept_benchmarks.items():
        dept_rows = [r for r in rows if r["Department"] == dept]
        dept_dep = [r for r in dept_rows if r["Attrition"] == "Yes"]
        d_rate = len(dept_dep) / len(dept_rows)
        print(f"Dept {dept}: Total={len(dept_rows)}, Departed={len(dept_dep)}, Rate={d_rate:.2%}")
        assert len(dept_rows) == exp["total"], f"Dept {dept} total mismatch"
        assert len(dept_dep) == exp["departed"], f"Dept {dept} departed mismatch"
        assert round(d_rate, 4) == exp["rate"], f"Dept {dept} rate mismatch"
        
    # 4. Flight Risk & Overtime
    flight_risk = [r for r in rows if int(r["Performance_Rating"]) >= 4 and int(r["Job_Satisfaction"]) <= 2 and r["Attrition"] == "No"]
    low_sat = [r for r in rows if int(r["Job_Satisfaction"]) <= 2]
    ot_yes = [r for r in rows if r["Overtime"] == "Yes"]
    ot_no = [r for r in rows if r["Overtime"] == "No"]
    ot_yes_attr = sum(1 for r in ot_yes if r["Attrition"] == "Yes") / len(ot_yes)
    ot_no_attr = sum(1 for r in ot_no if r["Attrition"] == "Yes") / len(ot_no)
    
    print(f"High Performer Flight Risk: {len(flight_risk)} (Expected: 76)")
    print(f"Low Satisfaction Headcount: {len(low_sat)} (Expected: 360)")
    print(f"Overtime Attrition: {ot_yes_attr:.2%} (Expected: 18.24%)")
    print(f"Non-Overtime Attrition: {ot_no_attr:.2%} (Expected: 19.53%)")
    
    assert len(flight_risk) == 76
    assert len(low_sat) == 360
    assert round(ot_yes_attr, 4) == 0.1824
    assert round(ot_no_attr, 4) == 0.1953
    
    print("\nALL BENCHMARKS VERIFIED SUCCESSFULLY WITH 100% PARITY!")

if __name__ == "__main__":
    test_hr_data_and_benchmarks()
