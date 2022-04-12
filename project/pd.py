import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("bankly.sqlite")
df = pd.read_sql_query("SELECT * from Deposits", con)

# Verify that result of SQL query is stored in the dataframe
print(df.head())

df.to_csv("new.csv",index=False)

con.close()
