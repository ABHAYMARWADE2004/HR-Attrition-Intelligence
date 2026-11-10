import pandas as pd

emp = pd.read_csv("data/employee_info.csv", dtype=str)
sal = pd.read_csv("data/salary_details.csv", dtype=str)
perf = pd.read_csv("data/performance_attendance.csv", dtype=str)

# Snowflake me jo tables banayi thi, unhi ke column order se naam do
emp.columns = ["EmployeeID", "Age", "Department", "JobRole", "Gender", "MaritalStatus"]
sal.columns = ["Employee_Id", "MonthlyIncome", "YearsAtCompany", "JobSatisfaction"]
perf.columns = ["emp_id", "PerformanceRating", "OverTime", "DistanceFromHome", "Attrition"]

def num(s):
    return pd.to_numeric(s.str.strip(), errors="coerce")

e = pd.DataFrame({
    "EMP_ID": emp["EmployeeID"].str.strip(),
    "AGE": num(emp["Age"]),
    "DEPARTMENT": emp["Department"].str.strip().str.lower(),
    "JOB_ROLE": emp["JobRole"],
    "GENDER": emp["Gender"],
    "MARITAL_STATUS": emp["MaritalStatus"].fillna("Unknown"),
}).drop_duplicates()

p = pd.DataFrame({
    "EMP_ID": perf["emp_id"].str.strip().str.upper(),
    "PERFORMANCE_RATING": num(perf["PerformanceRating"]),
    "OVERTIME": perf["OverTime"],
    "DISTANCE_FROM_HOME": num(perf["DistanceFromHome"]),
    "ATTRITION": perf["Attrition"],
}).drop_duplicates()

s = pd.DataFrame({
    "EMP_ID": sal["Employee_Id"].str.strip(),
    "MONTHLY_INCOME": num(sal["MonthlyIncome"]),
    "YEARS_AT_COMPANY": num(sal["YearsAtCompany"]),
    "JOB_SATISFACTION": num(sal["JobSatisfaction"]).fillna(3),
}).drop_duplicates()

final = e.merge(p, on="EMP_ID").merge(s, on="EMP_ID")
final = final[final["AGE"].notna()]

final = final[["EMP_ID", "AGE", "DEPARTMENT", "JOB_ROLE", "GENDER", "MARITAL_STATUS",
               "PERFORMANCE_RATING", "OVERTIME", "DISTANCE_FROM_HOME", "ATTRITION",
               "MONTHLY_INCOME", "YEARS_AT_COMPANY", "JOB_SATISFACTION"]]

final.to_csv("data/hr_attrition_final.csv", index=False)
print(final.shape)
print(final["ATTRITION"].value_counts())
print(final["DEPARTMENT"].value_counts())