import datetime as dt
import re
from pathlib import Path

import pandas as pd

from main import main


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "birthdays.csv"


def prompt_for_name() -> str:
    name = input("Enter your name: ").strip()

    while not name:
        print("Name cannot be empty. Please try again.")
        name = input("Enter your name: ").strip()

    return name.title()


def prompt_for_email() -> str:
    email = input("Enter your email: ").strip()

    while not email:
        print("Email cannot be empty. Please try again.")
        email = input("Enter your email: ").strip()

    return email.lower()


def prompt_for_dob() -> dt.date:
    dob_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    while True:
        dob_text = input(
            "Enter your date of birth (dd-mm-yyyy): "
        ).strip()

        if not dob_pattern.fullmatch(dob_text):
            print("Invalid format. Please use dd-mm-yyyy.")
            continue

        try:
            parsed_dob = dt.datetime.strptime(
                dob_text,
                "%d-%m-%Y"
            )

            return dt.date(
                parsed_dob.year,
                parsed_dob.month,
                parsed_dob.day
            )

        except ValueError:
            print("That date is not valid. Please try again.")

    raise RuntimeError("DOB prompt loop exited unexpectedly.")


def save_contact(name: str, email: str, dob: dt.date) -> None:
    if CSV_FILE.exists():
        data = pd.read_csv(CSV_FILE)
    else:
        data = pd.DataFrame(
            columns=["name", "email", "year", "month", "day"]
        )

    new_contact = pd.DataFrame([{
        "name": name,
        "email": email,
        "year": dob.year,
        "month": dob.month,
        "day": dob.day
    }])

    data = pd.concat(
        [data, new_contact],
        ignore_index=True
    )

    data.to_csv(CSV_FILE, index=False)


def start() -> None:
    name = prompt_for_name()
    email = prompt_for_email()
    dob = prompt_for_dob()

    save_contact(name, email, dob)

    print("Contact saved successfully.")

    message = main()
    print(message)


if __name__ == "__main__":
    start()