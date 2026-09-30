"""Input validation. Every function returns the cleaned value or raises ValidationError."""

from __future__ import annotations

from typing import Iterable, List

from .config import MAX_MARKS, SUBJECTS
from .exceptions import ValidationError

MAX_NAME_LEN = 50
MAX_ROLL_LEN = 20


def validate_name(raw: str) -> str:
    name = " ".join(str(raw).split())  # trim + collapse repeated spaces
    if not name:
        raise ValidationError("Name cannot be empty.")
    if len(name) > MAX_NAME_LEN:
        raise ValidationError(f"Name must be at most {MAX_NAME_LEN} characters.")
    if not name[0].isalpha() or not all(c.isalpha() or c in " .'-" for c in name):
        raise ValidationError("Name may contain only letters, spaces, '.', \"'\" and '-'.")
    return name


def validate_roll_no(raw: str) -> str:
    roll = str(raw).strip().upper()
    if not roll:
        raise ValidationError("Roll number cannot be empty.")
    if len(roll) > MAX_ROLL_LEN:
        raise ValidationError(f"Roll number must be at most {MAX_ROLL_LEN} characters.")
    if not all(c.isascii() and (c.isalnum() or c in "-_") for c in roll):
        raise ValidationError("Roll number may contain only letters, digits, '-' and '_'.")
    return roll


def validate_marks(raw) -> int:
    text = str(raw).strip()
    if not (text.isascii() and text.isdigit()):
        raise ValidationError(f"Marks must be a whole number between 0 and {MAX_MARKS}.")
    value = int(text)
    if value > MAX_MARKS:
        raise ValidationError(f"Marks must be between 0 and {MAX_MARKS}.")
    return value


def validate_marks_list(values: Iterable) -> List[int]:
    values = list(values)
    if len(values) != len(SUBJECTS):
        raise ValidationError(f"Expected marks for {len(SUBJECTS)} subjects, got {len(values)}.")
    return [validate_marks(v) for v in values]
