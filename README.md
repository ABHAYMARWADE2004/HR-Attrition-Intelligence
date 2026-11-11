# HR Attrition Intelligence

This is my project on employee attrition. I took HR data, cleaned it with SQL in Snowflake, looked at why people leave, trained a model to predict who might leave, and made a Streamlit app and a Power BI dashboard to show the results.

Live app: https://hr-attrition-intelligence-adzrfc9t4ztbjwglgojzvc.streamlit.app/

![Power BI overview](outputs/powerbi_executive_overview.png)

## The problem

The project is based on a case study. A company called TechNova has about 5,000 employees in 5 departments (Sales, Engineering, HR, Marketing, Finance). Attrition went up from 18% to 27% in two quarters. HR only found out why people left after they had already left, in exit interviews.

So I tried to answer these questions:

1. How many people leave, and which departments, roles and tenure groups are worst?
2. What is linked to people leaving (salary, overtime, distance, job satisfaction)?
3. Can we predict who is likely to leave?

## How the data flows

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
- **Python:** I made charts (`src/eda.py`) and trained the model (`src/train_model.py`).
- **Streamlit and Power BI:** these show the results.

**Note:** My Snowflake free trial ended, so the app now reads a CSV copy of the final table (`data/hr_attrition_final.csv`). The file `rebuild_data.py` makes the same table from the source CSVs using the same cleaning steps as the SQL.

## The data

The data is synthetic (not real). It has 4,700 employees. 1,359 of them left, which is about 29%.

Columns: EMP_ID, AGE, DEPARTMENT, JOB_ROLE, GENDER, MARITAL_STATUS, PERFORMANCE_RATING, OVERTIME, DISTANCE_FROM_HOME, ATTRITION, MONTHLY_INCOME, YEARS_AT_COMPANY, JOB_SATISFACTION.

## Streamlit app

Live app: https://hr-attrition-intelligence-adzrfc9t4ztbjwglgojzvc.streamlit.app/

It has two tabs:

- **Dashboard:** filter by department and tenure, see the main numbers and charts. Clicking a bar in the department chart filters the other charts.
- **Predict Attrition:** fill in an employee's details and the model gives a risk result.

![Streamlit dashboard](outputs/streamlit_dashboard.png)
![Streamlit predict](outputs/streamlit_predict.png)

## Power BI dashboard

I made a 3 page dashboard in Power BI. The file is `powerbi/HR_Attrition_Dashboard.pbix` (you need Power BI Desktop on Windows to open it).

1. **Executive Overview:** total employees, how many left, attrition rate, and attrition by department, job role and tenure.
2. **Attrition Drivers:** attrition rate by distance, income, age, performance, job satisfaction and overtime.
3. **Risk Analysis:** I made a simple risk score by counting risk factors (overtime, low income, long distance, new joiner, low satisfaction). It also lists current employees with 2 or more risk factors.

![Executive overview](outputs/powerbi_executive_overview.png)
![Attrition drivers](outputs/powerbi_attrition_drivers.png)
![Risk analysis](outputs/powerbi_risk_analysis.png)

The data is saved inside the .pbix file. Please don't click Refresh, because it was connected to Snowflake and my trial has ended.

## What I found

- Overall attrition is 28.9%.
- Overtime matters a lot. 41.6% of people who do overtime left, compared to 23.3% of people who don't.
- Low salary matters. 42.9% left when monthly income was below 45K.
- New joiners (0 to 1 years) left the most, at 40.2%.
- People living 21 km or more away left more (36.3%).
- Low job satisfaction (rating 1 or 2) had about 35 to 37% attrition. Rating 3 or 4 had about 22%.
- Age did not make much difference.
- More risk factors means more attrition. It goes from 10.8% with no risk factors to about 77% with four.
- HR has the highest attrition (33.4%) and Finance the lowest (24.7%).

## The model

I used a Random Forest. Only about 29% of employees left, so the classes are uneven. I used SMOTE on the training data to balance it, and tuned the model with GridSearchCV. I kept 20% of the data aside for testing.

| Result on test data (for people who left) | Value |
|---|---|
| Accuracy | 0.68 |
| Precision | 0.42 |
| Recall | 0.31 |
| F1 score | 0.35 |

The model is not very strong. It only catches about 31% of the people who actually left. I think this is because the data is synthetic and does not have a very clear pattern. I did not rely on accuracy, because a model that says "No" for everyone would also get around 71%.

Other things to know:

- Feature importance only shows what the model used the most. It does not prove what causes people to leave.
- The model uses age, gender and marital status. In a real HR system these should be checked or removed, because they can lead to unfair results.

## Folders

```
data/          CSV files (source files and hr_attrition_final.csv)
models/        trained model (attrition_model.pkl)
outputs/       charts and screenshots
powerbi/       Power BI file
sql/           pipeline.sql (Snowflake SQL)
src/           connect_snowflake.py, eda.py, train_model.py
app.py         Streamlit app
main.py        runs the EDA and model training
rebuild_data.py    makes hr_attrition_final.csv from the source CSVs
export_snapshot.py exported the final table from Snowflake
```

## How to run it

```
git clone https://github.com/ABHAYMARWADE2004/HR-Attrition-Intelligence.git
cd HR-Attrition-Intelligence

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python main.py
python -m streamlit run app.py
```

## Tools used

AWS S3, Snowflake, SQL, Python (pandas, scikit-learn, imbalanced-learn, matplotlib, seaborn), Plotly, Streamlit, Power BI, Git and GitHub
