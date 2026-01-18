import pandas as pd
import numpy as np

applications_df = pd.read_csv("applications.csv")
applications_df.columns = applications_df.columns.str.strip()

print(applications_df.head())
print(applications_df.info())
print(applications_df.isnull().sum())
print(applications_df.nunique())
print(applications_df.value_counts())

# value counts for each column
for column in applications_df.columns:
    print(f"{column}: {applications_df[column].value_counts()}")

