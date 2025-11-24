import re

def validate_name(name: str) -> bool:
    return bool(name.strip()) and name.replace(" ", "").isalpha()

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) == 11

def validate_not_empty(value: str) -> bool:
    return bool(value.strip())