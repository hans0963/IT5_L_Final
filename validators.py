# validators.py
import re
from datetime import datetime

# --------------------------
# Regex Patterns
# --------------------------

# Login & Registration
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{4,30}$")  # only letters, numbers, underscores

# Password must contain uppercase, lowercase, number; no special char required
PASSWORD_RE = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")

COMMON_WEAK_PASSWORDS = {
    "password", "12345678", "qwerty", "letmein", "admin", "11111111"
}

# Student fields
NAME_RE = re.compile(r"^[A-Za-z\s-]{2,50}$")  # letters, spaces, hyphens
PHONE_RE = re.compile(r"^[0-9]{11}$")  # Philippine standard mobile format

# Books
TITLE_RE = re.compile(r"^.{2,100}$")  # any characters, at least 2
AUTHOR_RE = NAME_RE
ISBN_RE = re.compile(r"^(97(8|9))?\d{9}(\d|X)$")  # ISBN-10 or ISBN-13
YEAR_RE = re.compile(r"^\d{4}$")


# --------------------------
# Validation Functions
# --------------------------

# ---- Login & Registration ----

def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.fullmatch(email))

def validate_username(username: str) -> bool:
    return bool(USERNAME_RE.fullmatch(username))

def validate_password(password: str) -> tuple[bool, str]:
    if password.lower() in COMMON_WEAK_PASSWORDS:
        return False, "Password is too common. Choose a stronger one."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not PASSWORD_RE.fullmatch(password):
        return False, (
            "Password must contain:\n"
            "- At least 1 uppercase letter\n"
            "- At least 1 lowercase letter\n"
            "- At least 1 number"
        )

    return True, ""


# ---- Student Fields ----

def validate_name(name: str) -> bool:
    return bool(NAME_RE.fullmatch(name.strip()))

def validate_phone(phone: str) -> bool:
    return bool(PHONE_RE.fullmatch(phone.strip()))

def validate_student_fields(first: str, last: str, email: str, phone: str) -> tuple[bool, str]:

    if not validate_name(first):
        return False, "First name must contain only letters and be at least 2 characters."

    if not validate_name(last):
        return False, "Last name must contain only letters and be at least 2 characters."

    if not validate_email(email):
        return False, "Invalid email format."

    # Change condition below depending on required or optional

    # OPTIONAL phone version:
    if phone and not validate_phone(phone):
        return False, "Phone number must be exactly 11 (numbers only)."

    return True, ""

# ---- Book Fields ----

def validate_book_fields(title: str, author: str, isbn: str, year: str) -> tuple[bool, str]:

    if not TITLE_RE.fullmatch(title.strip()):
        return False, "Book title must be at least 2 characters long."

    if not AUTHOR_RE.fullmatch(author.strip()):
        return False, "Author name must contain only letters and be at least 2 characters."

    if not ISBN_RE.fullmatch(isbn.strip()):
        return False, "ISBN must be a valid ISBN-10 or ISBN-13 format (numbers only)."

    if not YEAR_RE.fullmatch(year.strip()):
        return False, "Year must be a 4-digit number."

    current_year = datetime.now().year
    if not (1800 <= int(year) <= current_year):
        return False, f"Year must be between 1800 and {current_year}."

    return True, ""


# --------------------------
# Universal Helper
# --------------------------

def is_empty(*fields) -> bool:
    """Returns True if any given field is empty."""
    return any(not str(field).strip() for field in fields)
