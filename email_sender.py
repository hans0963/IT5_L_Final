import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self):
        self.credentials_path = "credentials.json"
        self.email = None
        self.password = None
        self.load_credentials()

    def load_credentials(self):
        """Load Gmail credentials from credentials.json"""
        if not os.path.exists(self.credentials_path):
            print("❌ ERROR: credentials.json not found.")
            return False

        try:
            with open(self.credentials_path, "r") as f:
                data = json.load(f)
                self.email = data.get("email", "")
                self.password = data.get("password", "")
                print("📧 Email credentials loaded.")
                return True

        except Exception as e:
            print("❌ Failed to read credentials.json:", e)
            return False

    def send_email(self, to_email, subject, body):
        """Send an email using Gmail SMTP. Safe even if credentials missing."""

        if not self.email or not self.password:
            print("⚠️ Email NOT sent — missing credentials.")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

            print(f"📨 Email sent to {to_email}")
            return True

        except Exception as e:
            print("❌ Email sending failed:", e)
            return False
