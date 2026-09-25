import datetime as dt
import os
import random
import smtplib
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv


load_dotenv()

MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("APP_PASSWORD")

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "birthdays.csv"
TEMPLATE_DIR = BASE_DIR / "letter_templates"


def load_templates() -> list[Path]:
    return sorted(TEMPLATE_DIR.glob("letter_*.txt"))


def send_birthdays(today: dt.date) -> str:
    if not MY_EMAIL or not PASSWORD:
        return "Email credentials are missing, so birthday emails were not sent."

    templates = load_templates()

    if not templates:
        return "No letter templates were found."

    if not CSV_FILE.exists():
        return "No birthdays.csv file found."

    data = pd.read_csv(CSV_FILE)

    for _, row in data.iterrows():
        try:
            month = int(row["month"])
            day = int(row["day"])
        except (TypeError, ValueError):
            continue

        if month != today.month or day != today.day:
            continue

        recipient_name = (
            str(row.get("name", "friend"))
            .strip()
            .title()
        )

        recipient_email = (
            str(row.get("email", ""))
            .strip()
            .lower()
        )

        if not recipient_email:
            continue

        template_path = random.choice(templates)

        message_body = template_path.read_text(
            encoding="utf-8"
        ).replace("[NAME]", recipient_name)

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(
                user=MY_EMAIL,
                password=PASSWORD
            )

            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=recipient_email,
                msg=f"Subject: Happy Birthday\n\n{message_body}"
            )

        return (
            f"Birthday email sent to {recipient_name} "
            f"<{recipient_email}> using {template_path.name}."
        )

    return "No birthdays today."


def main() -> str:
    return send_birthdays(dt.date.today())


if __name__ == "__main__":
    print(main())