# Requirements

## Functional Requirements

The system is organised into three major functional modules plus a persistence layer.

### Module 1 - Student Management (`manager.py`, `validators.py`)
| ID | Requirement |
|----|-------------|
| FR-1 | Add a student with name, unique roll number and marks in 5 subjects |
| FR-2 | View all students in a table sorted by roll number |
| FR-3 | Search a student by roll number (full detail) or by part of the name |
| FR-4 | Update a student's marks; derived values are recalculated automatically |
| FR-5 | Delete a student after a yes/no confirmation |
| FR-6 | Reject invalid names, roll numbers, duplicates and marks outside 0-100 |

### Module 2 - Result Processing (`grading.py`, `models.py`)
| ID | Requirement |
|----|-------------|
| FR-7 | Calculate total (out of 500) and percentage |
| FR-8 | Assign grade: A+ (>=90), A (>=80), B (>=70), C (>=60), D (>=50), F (<50) |
| FR-9 | Declare PASS only if the student scores at least 40 in **every** subject |

### Module 3 - Reports and Analytics (`reports.py`)
| ID | Requirement |
|----|-------------|
| FR-10 | Rank list by total marks; equal totals share a rank (1, 2, 2, 4 ...) |
| FR-11 | Class report: number of students, passed/failed, pass %, class average, topper, lowest scorer |
| FR-12 | Subject-wise averages and grade distribution |

### Persistence (`storage.py`)
| ID | Requirement |
|----|-------------|
| FR-13 | Load records from CSV at start-up; start empty if no file exists |
| FR-14 | Save records on request and automatically on exit |

### Input / Output structure
- **Input:** menu choice (0-9), text and numeric prompts from the keyboard, CSV data file
- **Output:** formatted tables and reports on the console, CSV data file, log file

### User workflow
Start -> load records -> show menu -> user picks an action -> input is validated (re-prompted on error) -> action runs -> result displayed -> back to menu -> "Save and exit" writes the CSV and ends.

## Non-Functional Requirements

| ID | Category | Requirement | How it is met |
|----|----------|-------------|---------------|
| NFR-1 | Reliability | A crash or full disk must never destroy existing data | `storage.save()` writes to a temp file and uses `os.replace()` (atomic); the app refuses to exit if saving fails |
| NFR-2 | Reliability | Corrupt data rows must not stop start-up | Bad rows are skipped, counted, warned about and logged |
| NFR-3 | Usability | Invalid input must produce a clear message and a re-prompt, never a crash | `prompt_valid()` loops on `ValidationError`; all messages state the accepted range/format |
| NFR-4 | Security / Data integrity | All input is validated and normalised before use; no `eval`/`exec`; CSV parsing via `csv` module | `validators.py`; names restricted to letters, roll numbers to `A-Z 0-9 - _` |
| NFR-5 | Error handling | Every expected failure has a named exception; unexpected ones are caught at the menu boundary | `exceptions.py`, `cli.main_loop()` |
| NFR-6 | Logging | Significant events and errors are recorded for troubleshooting | Rotating log `logs/srms.log` (1 MB x 3 files) |
| NFR-7 | Maintainability | Small single-purpose modules; UI separate from logic; settings in one file | `config.py`; no `print`/`input` outside `cli.py` |
| NFR-8 | Performance | Look-ups are O(1); typical class sizes (<= 1000 students) respond instantly | Dictionary keyed by roll number |
| NFR-9 | Portability | Runs on Windows/macOS/Linux with Python 3.8+ and no third-party packages | Standard library only; `pathlib` for paths |
| NFR-10 | Scalability | Subjects, pass mark and grade cut-offs can change without touching the logic | `SUBJECTS`, `PASS_MARK`, `GRADE_SCALE` in `config.py` |
