import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

load_dotenv()
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)
df = pd.read_sql("SELECT * FROM hr_attrition_final;", conn)
conn.close()
os.makedirs("data", exist_ok=True)
df.to_csv("data/hr_attrition_final.csv", index=False)
print(df.shape)