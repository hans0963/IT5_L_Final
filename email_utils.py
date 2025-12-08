from email_sender import EmailSender

mailer = EmailSender()


# ---------------- Reservation Email ----------------
def generate_reservation_email(student_name, book_title):
    subject = "📚 Reservation Confirmed"
    body = (
        f"Hello {student_name},\n\n"
        f"Your reservation for the book:\n"
        f"📖 {book_title}\n\n"
        f"has been successfully placed.\n"
        f"You can pick it up within 7 days.\n\n"
        f"Thank you!"
    )
    return subject, body


# ---------------- Ready for Pickup Email ----------------
def generate_ready_email(student_name, book_title):
    subject = "📗 Your Reserved Book is READY for Pickup!"
    body = (
        f"Hello {student_name},\n\n"
        f"The book you reserved is now available:\n"
        f"📖 {book_title}\n\n"
        f"Please claim it at the library front desk.\n\n"
        f"Thank you!"
    )
    return subject, body


# ---------------- Reminder Email ----------------
def send_gmail_reminder(to_email, student_name, book_title, due_date):
    subject = "🔔 Book Return Reminder"
    body = (
        f"Hello {student_name},\n\n"
        f"This is a reminder that the book:\n"
        f"📖 {book_title}\n\n"
        f"is due on: {due_date}\n\n"
        f"Please return it on time to avoid penalties.\n"
        f"\nThank you!"
    )
    return mailer.send_email(to_email, subject, body)


# ---------------- Book Available Notification ----------------
def send_book_available_notification(to_email, student_name, book_title):
    subject = "📕 Book Now Available"
    body = (
        f"Hello {student_name},\n\n"
        f"The book you were waiting for is now available:\n"
        f"📖 {book_title}\n\n"
        f"You may reserve or borrow it anytime.\n\n"
        f"Thank you!"
    )
    return mailer.send_email(to_email, subject, body)
