"""Student data model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from . import grading
from .config import SUBJECTS


@dataclass
class Student:
    roll_no: str
    name: str
    marks: List[int] = field(default_factory=list)

    @property
    def total(self) -> int:
        return grading.calculate_total(self.marks)

    @property
    def percentage(self) -> float:
        return grading.calculate_percentage(self.marks)

    @property
    def grade(self) -> str:
        return grading.get_grade(self.percentage)

    @property
    def result(self) -> str:
        return grading.get_result(self.marks)

    def subject_marks(self) -> Dict[str, int]:
        return dict(zip(SUBJECTS, self.marks))
