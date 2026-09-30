"""Business logic: CRUD operations on students. No input()/print() here."""

from __future__ import annotations

import logging
from typing import Dict, Iterable, List

from .exceptions import DuplicateStudentError, StudentNotFoundError
from .models import Student
from .storage import CSVStorage
from .validators import validate_marks_list, validate_name, validate_roll_no

log = logging.getLogger(__name__)


class StudentManager:
    def __init__(self, storage: CSVStorage) -> None:
        self._storage = storage
        self._students: Dict[str, Student] = {}   # roll_no -> Student (O(1) lookup)
        self.dirty = False                         # True if there are unsaved changes

    # ---- persistence -------------------------------------------------
    def load(self) -> int:
        self._students = {s.roll_no: s for s in self._storage.load()}
        self.dirty = False
        return len(self._students)

    def save(self) -> int:
        self._storage.save(list(self._students.values()))
        self.dirty = False
        return len(self._students)

    @property
    def skipped_rows(self) -> int:
        return self._storage.skipped_rows

    # ---- CRUD --------------------------------------------------------
    def add(self, roll_no: str, name: str, marks: Iterable) -> Student:
        roll_no = validate_roll_no(roll_no)
        name = validate_name(name)
        marks = validate_marks_list(marks)
        if roll_no in self._students:
            raise DuplicateStudentError(f"Roll number '{roll_no}' already exists.")
        student = Student(roll_no, name, marks)
        self._students[roll_no] = student
        self.dirty = True
        log.info("Added student %s", roll_no)
        return student

    def exists(self, roll_no: str) -> bool:
        return validate_roll_no(roll_no) in self._students

    def get(self, roll_no: str) -> Student:
        roll_no = validate_roll_no(roll_no)
        try:
            return self._students[roll_no]
        except KeyError:
            raise StudentNotFoundError(f"No student with roll number '{roll_no}'.") from None

    def search_by_name(self, query: str) -> List[Student]:
        q = query.strip().lower()
        return [s for s in self.all() if q and q in s.name.lower()]

    def update_marks(self, roll_no: str, marks: Iterable) -> Student:
        student = self.get(roll_no)
        student.marks = validate_marks_list(marks)
        self.dirty = True
        log.info("Updated marks for %s", student.roll_no)
        return student

    def delete(self, roll_no: str) -> Student:
        student = self.get(roll_no)
        del self._students[student.roll_no]
        self.dirty = True
        log.info("Deleted student %s", student.roll_no)
        return student

    def all(self) -> List[Student]:
        return sorted(self._students.values(), key=lambda s: s.roll_no)

    def __len__(self) -> int:
        return len(self._students)
