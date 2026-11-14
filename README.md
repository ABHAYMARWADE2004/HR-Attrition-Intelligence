# 📊 HR Attrition Intelligence

An end-to-end HR analytics project. I cleaned HR data with SQL in Snowflake, found out why employees leave, trained a model to predict who might leave, and showed the results in a live Streamlit app and a 3-page Power BI dashboard.

🔗 **Live app:** https://hr-attrition-intelligence-adzrfc9t4ztbjwglgojzvc.streamlit.app/

---

## 🎯 Project Objective

This project is based on a class case study. The company, TechNova, is made up. It has about 5,000 employees in 5 departments (Sales, Engineering, HR, Marketing, Finance). In the case study, attrition went from 18% to 27% in two quarters, and HR only learned why people left after they had left.

I built this project to find out why employees leave and to see if a model can predict who is likely to leave.

---

## 🛠️ Tools & Technologies

| Area | Tools |
|---|---|
| Cloud storage | AWS S3 |
| Data warehouse | Snowflake, SQL |
| Data analysis | Python, pandas, numpy |
| Machine learning | scikit-learn (Random Forest), imbalanced-learn (SMOTE) |
| Charts | matplotlib, seaborn, Plotly |
| App | Streamlit |
| Dashboard | Power BI, DAX |
| Version control | Git, GitHub |

---

## 🏗️ Project Flow

```
Source CSV files (employee info, performance, salary)
        |
        v
AWS S3 (raw/ folder)
        |
        v
Snowflake: raw tables -> clean tables -> hr_attrition_final
        |
        v
Python: EDA charts + Random Forest model
        |
        +--> Streamlit app
        +--> Power BI dashboard
```

- **AWS S3:** I uploaded the source CSV files to a bucket, in a `raw/` folder.
- **Snowflake:** I made an external stage that points to the S3 folder and loaded the 3 main files (employee info, performance, salary) into 3 raw tables with `COPY INTO`. Then I cleaned them with SQL (trim spaces, change types, remove duplicates, fill missing job satisfaction with 3) and joined them into one table called `hr_attrition_final`. All the SQL is in `sql/pipeline.sql`.
- **Python:** `src/eda.py` makes the charts and `src/train_model.py` trains the model.
- **Streamlit and Power BI:** these show the results.

> **Note:** My Snowflake free trial ended, so the app now reads a CSV copy of the final table (`data/hr_attrition_final.csv`). The file `rebuild_data.py` makes the same table from the source CSVs, using the same cleaning steps as the SQL.

---

## 📌 Key KPIs

| Metric | Value |
|---|---|
| Total employees | 4,700 |
| Employees left | 1,359 |
| Attrition rate | 28.9% |
| Average monthly income | ₹61,279 |
| Current employees with 2+ risk factors | 1,118 |

The data is synthetic (not real).

Columns: EMP_ID, AGE, DEPARTMENT, JOB_ROLE, GENDER, MARITAL_STATUS, PERFORMANCE_RATING, OVERTIME, DISTANCE_FROM_HOME, ATTRITION, MONTHLY_INCOME, YEARS_AT_COMPANY, JOB_SATISFACTION.

---

## 📈 Power BI Dashboard

I made a 3-page dashboard. The file is `powerbi/HR_Attrition_Dashboard.pbix` (open it with Power BI Desktop on Windows).

### 1. Executive Overview
Total employees, employees left, attrition rate, average income, high-risk employees, and attrition by department, job role and tenure. It also has a decomposition tree.

![Executive overview](outputs/powerbi_executive_overview.png)

### 2. Attrition Drivers
Attrition rate by distance, income, age, performance, job satisfaction and overtime, plus a Key Influencers chart.

![Attrition drivers](outputs/powerbi_attrition_drivers.png)

### 3. Risk Analysis
A simple risk score made by counting risk factors: overtime, low income, long distance, short tenure and low job satisfaction. Employees with 2 or more risk factors are marked high-risk. The page also shows a list of those employees.

![Risk analysis](outputs/powerbi_risk_analysis.png)

**Dashboard features:** slicers (department, job role, overtime, age group, gender, marital status), KPI cards, decomposition tree, key influencers, and charts that filter each other when you click.

### 🧮 DAX used

- **Measures:** Total Employees, Employees Left, Attrition Rate, Avg Monthly Income, Avg Tenure, Avg Job Satisfaction, Overtime %, High-Risk Employees
- **Calculated columns:** Age Group, Income Band, Tenure Band, Distance Band, Risk Factors (counts how many of the 5 risk factors an employee has)

> The data is saved inside the .pbix file. Please don't click Refresh, because it was connected to Snowflake and my trial has ended.

---

## 🖥️ Streamlit App

🔗 https://hr-attrition-intelligence-adzrfc9t4ztbjwglgojzvc.streamlit.app/

- **Dashboard tab:** filter by department and tenure, see the main numbers and charts. Clicking a bar in the department chart filters the other charts.
- **Predict Attrition tab:** enter an employee's details and the model gives a risk result.

![Streamlit dashboard](outputs/streamlit_dashboard.png)
![Streamlit predict](outputs/streamlit_predict.png)

---

## 🔍 Key Insights

- Overall attrition is **28.9%**.
- **Overtime** matters a lot. 41.6% of people who do overtime left, compared to 23.3% of people who don't.
- **Low salary:** 42.9% left when monthly income was below 45K.
- **New joiners** (0 to 1 years) left the most, at 40.2%.
- **Long distance:** people living 21 km or more away left more (36.3%).
- **Job satisfaction:** ratings 1 and 2 had about 35 to 37% attrition. Ratings 3 and 4 had about 22%.
- **Age** did not make much difference (about 28 to 30% in every age group).
- **Risk factors stack up.** Attrition goes from 10.8% with no risk factors to about 77% with four.
- **HR** has the highest attrition (33.4%) and **Finance** the lowest (24.7%).

These show what is linked to attrition. They do not prove what causes it.

---

## 🤖 Machine Learning Model

I used a Random Forest. Only about 29% of employees left, so the classes are uneven. I used SMOTE on the training data to balance it, and tuned the model with GridSearchCV. I kept 20% of the data aside for testing.

| Result on test data (people who left) | Value |
|---|---|
| Accuracy | 0.68 |
| Precision | 0.42 |
| Recall | 0.31 |
| F1 score | 0.35 |

**What this means:** the model is not very strong. It catches about 31% of the people who actually left. I think this is because the data is synthetic and does not have a very clear pattern. I did not rely on accuracy, because a model that says "No" for everyone would also get around 71%.

Things to know:

- Feature importance shows what the model used the most. It does not prove what causes people to leave.
- The model uses age, gender and marital status. In a real HR system these should be checked or removed, because they can lead to unfair results.

---

## 📁 Project Structure

```
HR-Attrition-Intelligence/
├── .devcontainer/
│   └── devcontainer.json
├── data/
│   ├── employee_info.csv
│   ├── performance_attendance.csv
│   ├── salary_details.csv
│   └── hr_attrition_final.csv
├── models/
│   └── attrition_model.pkl
├── outputs/
│   ├── attrition_by_department.png
│   ├── attrition_by_overtime.png
│   ├── salary_vs_attrition.png
│   ├── powerbi_executive_overview.png
│   ├── powerbi_attrition_drivers.png
│   ├── powerbi_risk_analysis.png
│   ├── streamlit_dashboard.png
│   └── streamlit_predict.png
├── powerbi/
│   └── HR_Attrition_Dashboard.pbix
├── sql/
│   └── pipeline.sql
├── src/
│   ├── connect_snowflake.py
│   ├── eda.py
│   └── train_model.py
├── .gitignore
├── app.py
├── export_snapshot.py
├── main.py
├── rebuild_data.py
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

```
git clone https://github.com/ABHAYMARWADE2004/HR-Attrition-Intelligence.git
cd HR-Attrition-Intelligence

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python main.py
python -m streamlit run app.py
```

---

## 🚀 Future Improvements

- Improve the model so it catches more of the people who leave (a higher recall)
- Take age, gender and marital status out of the model

---

## 👨‍💻 Author

**Abhay Marwade**
Aspiring Data Analyst | Data Science & AI Enthusiast

- GitHub: https://github.com/ABHAYMARWADE2004
- LinkedIn: https://www.linkedin.com/in/abhay-marwade-681108295

⭐ If you found this project interesting, feel free to give it a star.
