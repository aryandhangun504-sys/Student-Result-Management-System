"""Central configuration. Change subjects, pass mark or grade cut-offs here."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SUBJECTS = ("Physics", "Maths", "Python", "Electronics", "English")
MAX_MARKS = 100          # maximum marks per subject
PASS_MARK = 40           # minimum marks required in EVERY subject
MAX_TOTAL = MAX_MARKS * len(SUBJECTS)

# (minimum percentage, grade) - checked from top to bottom
GRADE_SCALE = ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"))
FAIL_GRADE = "F"
ALL_GRADES = tuple(g for _, g in GRADE_SCALE) + (FAIL_GRADE,)

# File locations can be overridden with environment variables.
DATA_FILE = Path(os.environ.get("SRMS_DATA_FILE", BASE_DIR / "data" / "students.csv"))
LOG_FILE = Path(os.environ.get("SRMS_LOG_FILE", BASE_DIR / "logs" / "srms.log"))
