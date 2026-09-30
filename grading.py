"""Pure grading rules: totals, percentage, grade and pass/fail."""

from __future__ import annotations

from typing import Sequence

from .config import FAIL_GRADE, GRADE_SCALE, MAX_MARKS, PASS_MARK


def calculate_total(marks: Sequence[int]) -> int:
    return sum(marks)


def calculate_percentage(marks: Sequence[int]) -> float:
    """Percentage over all subjects. Integer maths first avoids float rounding at boundaries."""
    if not marks:
        return 0.0
    return sum(marks) * 100 / (len(marks) * MAX_MARKS)


def get_grade(percentage: float) -> str:
    for minimum, grade in GRADE_SCALE:
        if percentage >= minimum:
            return grade
    return FAIL_GRADE


def get_result(marks: Sequence[int]) -> str:
    """PASS only if the student scores at least PASS_MARK in every subject."""
    return "FAIL" if any(m < PASS_MARK for m in marks) else "PASS"
