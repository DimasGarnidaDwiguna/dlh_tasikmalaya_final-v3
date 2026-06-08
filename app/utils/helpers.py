from datetime import datetime
import re


def generate_ticket_number(last_id: int | None = None) -> str:
    number = (last_id or 0) + 1
    return f"DLH-{datetime.now().year}-{number:05d}"


def format_date(value):
    if not value:
        return "-"
    if isinstance(value, str):
        return value
    return value.strftime("%d %B %Y")


def only_digits(value: str, min_len: int = 1, max_len: int = 20) -> bool:
    value = (value or "").strip()
    return value.isdigit() and min_len <= len(value) <= max_len


def valid_year(value: str) -> bool:
    value = (value or "").strip()
    return bool(re.fullmatch(r"20[0-9]{2}|19[0-9]{2}", value))
