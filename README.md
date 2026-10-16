# Email Sender Bot 📧

## About the Project
Email Sender Bot is a Python-based automation project that sends personalized emails to multiple recipients using a CSV file. It uses Gmail SMTP to send messages and provides retry handling and logging to track email delivery attempts.

## Features
- Read recipient names and email addresses from a CSV file.
- Send personalized emails using Python.
- Customize email subject and message.
- Attach files to emails.
- Retry failed email-sending attempts up to three times.
- Log email activity and errors.
- Display successful and failed email counts.
- Validate recipient details before sending.

## Technologies Used
- Python
- SMTP (`smtplib`)
- `email` module
- CSV
- Logging
- SSL/TLS

## Project Structure

```text
Email_Sender_Bot/
├── email_bot.py
├── recipients.csv
├── README.md
└── email.log
```

*Note: `email.log` is generated when the program runs.*

## Requirements
- Python 3 installed
- A Gmail account
- Google 2-Step Verification enabled
- A Gmail App Password for SMTP authentication

## Installation

Install Python if it is not already installed. No third-party Python packages are required for the current implementation.

## Configuration

Set your Gmail credentials as environment variables in PowerShell:

```powershell
$env:EMAIL_ADDRESS="your-email@gmail.com"
$env:EMAIL_APP_PASSWORD="your-app-password"
```

Use a Gmail App Password, not your normal Gmail password. Never upload credentials to GitHub.

## CSV File Format

Create a file named `recipients.csv`:

```csv
name,email
Test User,recipient@example.com
```

Replace the sample address with an email address you are authorized to contact.

## How to Run

Run the bot using:

```bash
python email_bot.py
```

### Customize the Email

```bash
python email_bot.py --subject "Python Project Test" --body "Hello {name}, this is my email bot project."
```

### Send an Attachment

```bash
python email_bot.py --attachment "report.pdf"
```

The attachment path must point to an existing file.

## Logging and Error Handling
- Retries failed sending attempts up to three times.
- Records sending attempts and errors in `email.log`.
- Displays the number of successful and failed emails.
- Skips recipient rows with missing or invalid basic details.

## Security
- Credentials are read from environment variables.
- Never commit passwords or private credentials.
- Send emails only to intended recipients and avoid unsolicited bulk email.

## Learning Outcomes
This project demonstrates Python automation, CSV processing,
