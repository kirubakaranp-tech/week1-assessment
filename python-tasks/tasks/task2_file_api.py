# Task 2 - reading/writing files and calling an API
# CSV -> JSON, filter high earners into a new CSV,
# fetch users from jsonplaceholder and handle timeouts / 404s

import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

USERS_URL = "https://jsonplaceholder.typicode.com/users"


def read_employees(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def write_high_earners(path, employees):
    columns = ["id", "name", "department", "salary", "city"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(employees)


def get_users():
    try:
        resp = requests.get(USERS_URL, timeout=5)
        resp.raise_for_status()

        users = []
        for user in resp.json():
            # city sits inside the nested "address" object
            city = user.get("address", {}).get("city", "Unknown")
            users.append({
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email"),
                "city": city,
            })

        write_json(OUTPUT_DIR / "users.json", users)

        for user in users[:3]:
            print(f"{user['id']} - {user['name']} - {user['email']}")

    except Timeout:
        print("The users request timed out.")
    except ConnectionError:
        print("Could not connect to the users API.")


def check_missing_user():
    # user 9999 doesn't exist, so we expect a 404 here
    try:
        resp = requests.get(f"{USERS_URL}/9999", timeout=5)
        if resp.status_code == 404:
            print("/users/9999 -> 404 Not found")
        else:
            resp.raise_for_status()

    except Timeout:
        print("The missing-user request timed out.")
    except ConnectionError:
        print("Could not connect to the users API.")


def main():
    load_dotenv(BASE_DIR / ".env")
    # jsonplaceholder doesn't need a key - just showing how we'd load one
    api_key = os.getenv("API_KEY")

    OUTPUT_DIR.mkdir(exist_ok=True)

    employees = read_employees(DATA_DIR / "employees.csv")
    high_earners = [emp for emp in employees if int(emp["salary"]) > 50000]

    write_json(OUTPUT_DIR / "employees.json", employees)
    write_high_earners(OUTPUT_DIR / "high_earners.csv", high_earners)

    print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")

    get_users()
    check_missing_user()


if __name__ == "__main__":
    main()
