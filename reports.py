"""Reporting and analytics over a list of students."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from .config import ALL_GRADES, SUBJECTS
from .models import Student


def rank_list(students: Sequence[Student]) -> List[Tuple[int, Student]]:
    """Rank by total marks (highest first). Ties share a rank: 1, 2, 2, 4 ..."""
    ordered = sorted(students, key=lambda s: (-s.total, s.name.lower()))
    ranked, prev_total, rank = [], None, 0
    for position, student in enumerate(ordered, start=1):
        if student.total != prev_total:
            rank, prev_total = position, student.total
        ranked.append((rank, student))
    return ranked


def subject_averages(students: Sequence[Student]) -> Dict[str, float]:
    if not students:
        return {}
    return {
        subject: sum(s.marks[i] for s in students) / len(students)
        for i, subject in enumerate(SUBJECTS)
    }


def grade_distribution(students: Sequence[Student]) -> Dict[str, int]:
    counts = {grade: 0 for grade in ALL_GRADES}
    for s in students:
        counts[s.grade] += 1
    return counts


def class_summary(students: Sequence[Student]) -> dict:
    """Headline numbers for the whole class."""
    if not students:
        return {"count": 0}
    passed = sum(1 for s in students if s.result == "PASS")
    return {
        "count": len(students),
        "passed": passed,
        "failed": len(students) - passed,
        "pass_percentage": passed * 100 / len(students),
        "class_average": sum(s.percentage for s in students) / len(students),
        "topper": max(students, key=lambda s: s.total),
        "lowest": min(students, key=lambda s: s.total),
    }
