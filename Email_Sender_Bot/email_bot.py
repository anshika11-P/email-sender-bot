
import csv
import os
import ssl
import smtplib
import logging
import time
import argparse
from email.message import EmailMessage

# Save activity and errors in email.log
logging.basicConfig(
    filename="email.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_email(name, recipient, subject, body, attachment=None):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender or not password:
        logging.error("Email credentials are not configured.")
        print("Set EMAIL_ADDRESS and EMAIL_APP_PASSWORD first.")
        return False

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body.replace("{name}", name))

    # Optional attachment
    if attachment:
        try:
            with open(attachment, "rb") as file:
                message.add_attachment(
                    file.read(),
                    maintype="application",
                    subtype="octet-stream",
                    filename=os.path.basename(attachment)
                )
        except OSError as error:
            logging.error(f"Attachment error: {error}")
            print(f"Attachment could not be opened: {error}")
            return False

    # Retry up to 3 times
    for attempt in range(1, 4):
        try:
            context = ssl.create_default_context()

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender, password)
                server.send_message(message)

            logging.info("Email sent to %s", recipient)
            print(f"Email sent successfully to {recipient}")
            return True

        except (smtplib.SMTPException, OSError) as error:
            logging.warning(
                "Attempt %s failed for %s: %s",
                attempt, recipient, error
            )
            if attempt < 3:
                time.sleep(2)

    print(f"Failed to send email to {recipient}")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Send personalized emails from a CSV file."
    )
    parser.add_argument(
        "--csv", default="recipients.csv",
        help="CSV file containing name and email columns"
    )
    parser.add_argument(
        "--subject", default="Hello from Python",
        help="Email subject"
    )
    parser.add_argument(
        "--body", default="Hello {name}, this is a test email sent using Python.",
        help="Email body; use {name} for personalization"
    )
    parser.add_argument(
        "--attachment", default=None,
        help="Optional file path to attach"
    )
    args = parser.parse_args()

    try:
        with open(args.csv, newline="", encoding="utf-8-sig") as file:
            recipients = list(csv.DictReader(file))
    except OSError as error:
        print(f"Could not read CSV: {error}")
        return

    if not recipients:
        print("No recipients found in the CSV file.")
        return

    successful = 0
    failed = 0

    for recipient in recipients:
        name = (recipient.get("name") or "").strip()
        email = (recipient.get("email") or "").strip()

        if not name or not email or "@" not in email:
            logging.warning("Skipping invalid recipient row.")
            print("Skipping a row with missing or invalid details.")
            failed += 1
            continue

        if send_email(
            name, email, args.subject,
            args.body, args.attachment
        ):
            successful += 1
        else:
            failed += 1

    print("\nEmail process completed!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("Check email.log for activity details.")


if __name__ == "__main__":
    main()
