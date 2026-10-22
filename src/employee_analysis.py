import pandas as pd

employees = pd.read_csv("../data/employees.csv")
employees.head()

%timeit employees["salary"].mean()

department_summary = employees.groupby("department")["salary"].agg(["count", "mean", "max"])
department_summary
