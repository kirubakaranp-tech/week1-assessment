# Task 3 - NumPy, Pandas and Matplotlib
# student marks with numpy, cleaning a messy employee file,
# department summary + joins, and four charts

import os
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHART_DIR = BASE_DIR / "output" / "charts"

# matplotlib sometimes can't write its cache in the user profile,
# so keep it inside the project folder
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def numpy_examples():
    # 4 students x 3 subjects
    marks = np.array([
        [78, 85, 92],
        [67, 74, 81],
        [88, 90, 84],
        [72, 68, 76],
    ])
    weights = np.array([0.30, 0.30, 0.40])

    print("Shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1))
    print("Subject averages:", marks.mean(axis=0))

    with_grace = marks + 5                    # broadcasting: +5 to every mark
    print("Weighted scores:", np.dot(with_grace, weights))


def pandas_examples(df):
    # info() prints a lot, so swallow its output
    with redirect_stdout(StringIO()):
        df.info()

    df.describe()
    df.loc[df["name"] == "Divya", ["name", "department", "salary"]]
    df.iloc[:2]
    df.loc[df["department"] == "IT", ["name", "salary"]]


def clean_employees():
    df = pd.read_csv(DATA_DIR / "employees_dirty.csv")

    # two salaries are missing - fill them with the median
    df["salary"] = df["salary"].fillna(df["salary"].median())
    # Suresh appears twice
    df = df.drop_duplicates()

    return df.astype({
        "id": "int64",
        "name": "string",
        "department": "string",
        "salary": "int64",
        "city": "string",
    })


def department_summary(df):
    departments = pd.read_csv(DATA_DIR / "departments.csv")

    summary = (
        df.groupby("department")
        .agg(
            headcount=("id", "count"),
            average_salary=("salary", "mean"),
            maximum_salary=("salary", "max"),
        )
        .reset_index()
    )

    inner = pd.merge(departments, summary, on="department", how="inner")
    left = pd.merge(departments, summary, on="department", how="left")
    outer = pd.merge(departments, summary, on="department", how="outer")

    hc = summary.set_index("department")["headcount"]
    print(f"Headcount: Sales {hc['Sales']} | HR {hc['HR']} | IT {hc['IT']} | Finance {hc['Finance']}")

    # departments with no employees show up as NaN in the outer join
    empty = outer.loc[outer["headcount"].isna(), "department"].tolist()
    print("Outer join: department with no employees:", ", ".join(empty))

    return summary


def save_chart(filename):
    plt.legend()
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename)


def create_charts(df, summary):
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 4))
    plt.bar(summary["department"], summary["headcount"], color="steelblue", label="Employees")
    plt.title("Employee Headcount by Department")
    plt.xlabel("Department")
    plt.ylabel("Headcount")
    save_chart("department_headcount.png")

    plt.figure(figsize=(7, 4))
    plt.hist(df["salary"], bins=5, color="seagreen", edgecolor="black", label="Salaries")
    plt.title("Salary Distribution")
    plt.xlabel("Salary")
    plt.ylabel("Number of Employees")
    save_chart("salary_histogram.png")

    plt.figure(figsize=(7, 4))
    plt.scatter(df["id"], df["salary"], color="darkorange", label="Employee salary")
    plt.title("Salary by Employee ID")
    plt.xlabel("Employee ID")
    plt.ylabel("Salary")
    save_chart("salary_scatter.png")

    by_id = df.sort_values("id")
    plt.figure(figsize=(7, 4))
    plt.plot(by_id["id"], by_id["salary"], marker="o", color="purple", label="Salary")
    plt.title("Salary Trend by Employee ID")
    plt.xlabel("Employee ID")
    plt.ylabel("Salary")
    save_chart("salary_line.png")

    # What the charts show:
    # - IT has the most people
    # - most salaries fall between 50k and 75k
    # - Karthik is the top earner
    # - salary doesn't really go up with employee ID
    plt.show()


def main():
    numpy_examples()

    employees = pd.read_csv(DATA_DIR / "employees.csv")
    pandas_examples(employees)

    cleaned = clean_employees()
    summary = department_summary(cleaned)
    create_charts(cleaned, summary)


if __name__ == "__main__":
    main()
