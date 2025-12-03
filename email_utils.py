import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_gmail_reminder(to_email, student_name, book_title, due_date):
    sender_email = "your_gmail@gmail.com"
    app_password = "your_app_password"  # Use Gmail App Password
    subject = "Library Overdue Book Reminder"
    body = f"Dear {student_name},\n\nThis is a reminder that your borrowed book '{book_title}' was due on {due_date}. Please return it as soon as possible to avoid further penalties.\n\nThank you."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

def send_book_available_notification(to_email, student_name, book_title):
    sender_email = "your_gmail@gmail.com"
    app_password = "your_app_password"  # Use Gmail App Password
    subject = "Library Book Now Available"
    body = f"Dear {student_name},\n\nThe book you reserved, '{book_title}', is now available for pickup. Please visit the library to collect it.\n\nThank you."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)