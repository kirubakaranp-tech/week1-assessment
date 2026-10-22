# Task 1 - Python basics with the employee list
# functions with *args / **kwargs, classes, custom exception,
# comprehensions, map/filter, loops with continue/break

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def bonus(salary, rate=0.1, *extras, **options):
    # salary * rate, plus any extra amounts. If a cap is given, don't go over it.
    total = salary * rate + sum(extras)

    cap = options.get("cap")
    if cap is not None and total > cap:
        return cap
    return total


class InvalidSalaryError(ValueError):
    pass


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        # reuse the parent text and just add the team size
        return f"{super().get_details()}, Team size: {self.team_size}"


def read_employees():
    employees = []
    with open(DATA_DIR / "employees.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["salary"] = int(row["salary"])
            employees.append(row)
    return employees


def main():
    employees = read_employees()

    # people earning more than 50k
    above_50k = [emp["name"] for emp in employees if emp["salary"] > 50000]

    # everyone's salary after a 10% hike
    hiked = list(map(lambda emp: emp["salary"] * 1.10, employees))

    # only the Chennai folks
    chennai = list(filter(lambda emp: emp["city"] == "Chennai", employees))
    chennai_names = [emp["name"] for emp in chennai]

    # skip zero salaries, stop at the first one above 85k
    for emp in employees:
        if emp["salary"] == 0:
            continue
        if emp["salary"] > 85000:
            break

    print(f"Above 50000: {above_50k}")
    print(f"Chennai: {chennai_names}")

    # negative salary should be rejected
    try:
        Employee("Invalid employee", -500)
    except InvalidSalaryError as err:
        print(f"Error: {err}")
    finally:
        print("Transaction finished")


if __name__ == "__main__":
    main()
