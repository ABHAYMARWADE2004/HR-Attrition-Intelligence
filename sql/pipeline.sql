-- =====================================================================
-- HR Attrition Intelligence: Snowflake pipeline
-- raw tables -> clean tables -> hr_attrition_final
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Setup
-- ---------------------------------------------------------------------
CREATE DATABASE hr_attrition;
CREATE SCHEMA hr_attrition.raw;
CREATE WAREHOUSE hr_wh WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;

USE DATABASE hr_attrition;
USE SCHEMA raw;

CREATE OR REPLACE FILE FORMAT csv_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE OR REPLACE STAGE hr_stage
  FILE_FORMAT = csv_format;

LIST @hr_stage;

-- ---------------------------------------------------------------------
-- 2. Raw tables (exact copy of the source files, all STRING)
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE employee_info (
  EmployeeID STRING,
  Age STRING,
  Department STRING,
  JobRole STRING,
  Gender STRING,
  MaritalStatus STRING
);

COPY INTO employee_info
FROM @hr_stage/employee_info.csv
FILE_FORMAT = csv_format;

CREATE OR REPLACE TABLE salary_details (
  Employee_Id STRING,
  MonthlyIncome STRING,
  YearsAtCompany STRING,
  JobSatisfaction STRING
);

COPY INTO salary_details
FROM @hr_stage/salary_details.csv
FILE_FORMAT = csv_format;

CREATE OR REPLACE TABLE performance_attendance (
  emp_id STRING,
  PerformanceRating STRING,
  OverTime STRING,
  DistanceFromHome STRING,
  Attrition STRING
);

COPY INTO performance_attendance
FROM @hr_stage/performance_attendance.csv
FILE_FORMAT = csv_format;

-- ---------------------------------------------------------------------
-- 3. Clean tables (trim, type-cast, deduplicate, handle missing values)
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE employee_info_clean AS
SELECT DISTINCT
  TRIM(EmployeeID) AS emp_id,
  TRY_CAST(Age AS INT) AS age,
  TRIM(LOWER(Department)) AS department,
  JobRole AS job_role,
  Gender AS gender,
  COALESCE(MaritalStatus, 'Unknown') AS marital_status
FROM employee_info;

CREATE OR REPLACE TABLE performance_clean AS
SELECT DISTINCT
  UPPER(TRIM(emp_id)) AS emp_id,
  TRY_CAST(PerformanceRating AS INT) AS performance_rating,
  OverTime AS overtime,
  TRY_CAST(DistanceFromHome AS INT) AS distance_from_home,
  Attrition AS attrition
FROM performance_attendance;

CREATE OR REPLACE TABLE salary_clean AS
SELECT DISTINCT
  TRIM(Employee_Id) AS emp_id,
  TRY_CAST(MonthlyIncome AS INT) AS monthly_income,
  TRY_CAST(YearsAtCompany AS INT) AS years_at_company,
  COALESCE(TRY_CAST(JobSatisfaction AS INT), 3) AS job_satisfaction
FROM salary_details;

-- ---------------------------------------------------------------------
-- 4. Final analysis-ready table
-- ---------------------------------------------------------------------
CREATE OR REPLACE TABLE hr_attrition_final AS
SELECT
  e.emp_id,
  e.age,
  e.department,
  e.job_role,
  e.gender,
  e.marital_status,
  p.performance_rating,
  p.overtime,
  p.distance_from_home,
  p.attrition,
  s.monthly_income,
  s.years_at_company,
  s.job_satisfaction
FROM employee_info_clean e
JOIN performance_clean p ON e.emp_id = p.emp_id
JOIN salary_clean s ON e.emp_id = s.emp_id
WHERE e.age IS NOT NULL;

-- ---------------------------------------------------------------------
-- 5. Checks
-- ---------------------------------------------------------------------
SELECT COUNT(*) FROM hr_attrition_final;
SELECT * FROM hr_attrition_final LIMIT 10;
