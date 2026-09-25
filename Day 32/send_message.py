import os
import smtplib

from dotenv import load_dotenv


load_dotenv()

MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("APP_PASSWORD")

MY_NAME = "Tanishq"
WEBSITE = "https://100daysofcode.pythonanywhere.com/day-32"


def send_message() -> str:
    if not MY_EMAIL or not PASSWORD:
        return "Email credentials are missing."

    recipient_name = input("Enter recipient's name: ").strip()
    recipient_email = input("Enter recipient's email: ").strip().lower()
    sender_name = input("Enter sender's name: ").strip()
    subject = input("Enter email subject: ").strip()
    message = input("Enter the message to be sent: ").strip()

    while not recipient_name:
        print("Recipient name cannot be empty.")
        recipient_name = input("Enter recipient's name: ").strip()

    while not recipient_email:
        print("Recipient email cannot be empty.")
        recipient_email = input("Enter recipient's email: ").strip().lower()

    while not sender_name:
        print("Sender name cannot be empty.")
        sender_name = input("Enter sender's name: ").strip()

    while not subject:
        print("Subject cannot be empty.")
        subject = input("Enter email subject: ").strip()

    while not message:
        print("Message cannot be empty.")
        message = input("Enter the message to be sent: ").strip()

    message_body = f"""Hi {recipient_name},

{message}

This message was sent by {sender_name}
via {WEBSITE}

Created by {MY_NAME}
"""

    email_message = f"Subject: {subject}\n\n{message_body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(
            user=MY_EMAIL,
            password=PASSWORD
        )

        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=recipient_email,
            msg=email_message
        )

    return (
        f"Message successfully sent to "
        f"{recipient_name} <{recipient_email}>."
    )


def main() -> str:
    return send_message()


if __name__ == "__main__":
    print(main())