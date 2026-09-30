"""CSV persistence with atomic writes and tolerance for corrupt rows."""

from __future__ import annotations

import csv
import logging
import os
import tempfile
from pathlib import Path
from typing import List

from .config import DATA_FILE, SUBJECTS
from .exceptions import StorageError, ValidationError
from .models import Student
from .validators import validate_marks_list, validate_name, validate_roll_no

log = logging.getLogger(__name__)

HEADER = ["roll_no", "name", *SUBJECTS]


class CSVStorage:
    def __init__(self, path: Path = DATA_FILE) -> None:
        self.path = Path(path)
        self.skipped_rows = 0  # corrupt rows ignored by the last load()

    def load(self) -> List[Student]:
        self.skipped_rows = 0
        if not self.path.exists():
            log.info("No data file at %s; starting empty", self.path)
            return []
        students: List[Student] = []
        try:
            with open(self.path, newline="", encoding="utf-8") as fh:
                for line_no, row in enumerate(csv.reader(fh), start=1):
                    if not row:
                        continue
                    if line_no == 1 and row[0].strip().lower() == "roll_no":
                        continue  # header
                    student = self._parse_row(row, line_no)
                    if student is None:
                        self.skipped_rows += 1
                    else:
                        students.append(student)
        except (OSError, csv.Error, UnicodeDecodeError) as exc:
            log.error("Failed to read %s: %s", self.path, exc)
            raise StorageError(f"Could not read '{self.path}': {exc}") from exc
        log.info("Loaded %d record(s), skipped %d", len(students), self.skipped_rows)
        return students

    def save(self, students: List[Student]) -> None:
        """Write to a temp file, then atomically replace the real file."""
        tmp_name = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                "w", newline="", encoding="utf-8", dir=self.path.parent, delete=False, suffix=".tmp"
            ) as fh:
                tmp_name = fh.name
                writer = csv.writer(fh)
                writer.writerow(HEADER)
                for s in students:
                    writer.writerow([s.roll_no, s.name, *s.marks])
            os.replace(tmp_name, self.path)
        except OSError as exc:
            log.error("Failed to write %s: %s", self.path, exc)
            if tmp_name and os.path.exists(tmp_name):
                os.remove(tmp_name)
            raise StorageError(f"Could not save to '{self.path}': {exc}") from exc
        log.info("Saved %d record(s) to %s", len(students), self.path)

    @staticmethod
    def _parse_row(row: List[str], line_no: int):
        if len(row) != 2 + len(SUBJECTS):
            log.warning("Line %d skipped: expected %d columns, got %d", line_no, 2 + len(SUBJECTS), len(row))
            return None
        try:
            return Student(
                roll_no=validate_roll_no(row[0]),
                name=validate_name(row[1]),
                marks=validate_marks_list(row[2:]),
            )
        except ValidationError as exc:
            log.warning("Line %d skipped: %s", line_no, exc)
            return None
