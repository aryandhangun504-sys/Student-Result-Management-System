# Student Result Management System

A modular, tested, console-based Python application for recording student marks, calculating grades and results automatically, and producing ranking and class reports.

> Built as a **VITyarthi - Build Your Own Project** submission (Python course).
> Author: **[Your Name]** | Reg. No: **[Your Reg No]**

## Overview
Teachers can add students with marks in five subjects and the system instantly works out the total, percentage, grade and PASS/FAIL status. Records are validated on entry, stored in a CSV file, and can be searched, updated, deleted, ranked and summarised. See [`statement.md`](statement.md) for the full problem statement, scope and target users.

## Features
- **Student management** - add, view, search (by roll number or name), update marks, delete (with confirmation)
- **Automatic results** - total /500, percentage, grade (A+ to F) and PASS/FAIL (needs 40+ in every subject)
- **Rank list** - ties share a rank (1, 2, 2, 4 ...)
- **Class report** - pass percentage, class average, topper, subject averages, grade distribution
- **Strict validation** - names, roll numbers (auto upper-cased), duplicates, marks 0-100; the program re-prompts instead of crashing
- **Safe persistence** - CSV storage with atomic saves; corrupt rows are skipped and reported
- **Logging** - rotating log file at `logs/srms.log`
- **Auto-save on Ctrl+C**, and the program refuses to exit if saving fails

## Technologies
- Python 3.8+ (standard library only: `csv`, `dataclasses`, `logging`, `pathlib`, `unittest`)
- Git / GitHub, GitHub Actions for CI

## Project Structure
```
student-result-management-system/
├── main.py                  # entry point
├── srms/                    # application package
│   ├── config.py            # subjects, pass mark, grade scale, file paths
│   ├── exceptions.py        # custom error types
│   ├── models.py            # Student dataclass
│   ├── grading.py           # total / percentage / grade / result rules
│   ├── validators.py        # input validation
│   ├── storage.py           # CSV load/save (atomic)
│   ├── manager.py           # CRUD business logic
│   ├── reports.py           # ranking and analytics
│   ├── logger.py            # logging setup
│   └── cli.py               # menus, prompts, output
├── tests/                   # 40 unit / integration tests
├── data/sample_students.csv # sample data
├── docs/                    # requirements, design diagrams, testing notes
├── statement.md
└── .github/workflows/tests.yml
```

## Installation and Running
```bash
git clone https://github.com/<your-username>/student-result-management-system.git
cd student-result-management-system

# optional: start with sample data
cp data/sample_students.csv data/students.csv      # Windows: copy data\sample_students.csv data\students.csv

python main.py                                     # use python3 on macOS/Linux
```
No packages need to be installed. Records are saved to `data/students.csv`.

### Using VS Code
Open the project folder (**File > Open Folder**), install the recommended Python extension, then:
- **Run:** press `F5` and choose *Run Student Result System* (it runs in the integrated terminal so keyboard input works)
- **Test:** open the Testing panel (beaker icon) and click Run, or use *Run all tests* in the Run and Debug panel

**Optional settings** (environment variables): `SRMS_DATA_FILE` and `SRMS_LOG_FILE` change where the data and log files live. Subjects, pass mark and grade cut-offs are in [`srms/config.py`](srms/config.py).

## Usage
```
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student
 2. View all students
 3. Search by roll number
 4. Search by name
 5. Update marks
 6. Delete student
 7. Rank list
 8. Class report
 9. Save records
 0. Save and exit
```

### Sample output

**View all students (option 2)**
```
Roll no     Name                    Total   Percent   Grade  Result
------------------------------------------------------------
21BCE001    Asha Rao                450     90.00%    A+     PASS
21BCE002    Ravi Kumar              369     73.80%    B      PASS
21BCE003    Meera Nair              263     52.60%    D      PASS
21BCE004    Arjun Singh             323     64.60%    C      FAIL
21BCE005    Sara Khan               435     87.00%    A      PASS
21BCE006    Dev Patel               285     57.00%    D      PASS
```
*Arjun Singh has 64.6% (grade C) but FAILs because he scored 35 in Physics, below the 40 minimum.*

**Adding a student with an invalid entry**
```
Enter name: Neha Iyer
Enter roll number: 21bce007
Marks in Physics (0-100): abc
  ! Marks must be a whole number between 0 and 100.
Marks in Physics (0-100): 85
...
Student added!

--------------------------------
Name        : Neha Iyer
Roll no     : 21BCE007
Physics     : 85
Maths       : 90
Python      : 88
Electronics : 76
English     : 92
Total       : 431 / 500
Percentage  : 86.20%
Grade       : A
Result      : PASS
--------------------------------
```

**Class report (option 8)**
```
----------- CLASS REPORT -----------
Students        : 7
Passed / Failed : 6 / 1
Pass percentage : 85.7%
Class average   : 73.03%
Topper          : Asha Rao (450/500)
Lowest scorer   : Meera Nair (263/500)

Subject averages:
  Physics     : 69.0
  Maths       : 75.7
  Python      : 76.4
  Electronics : 69.4
  English     : 74.6

Grade distribution:
  A+ : # 1
  A  : ## 2
  B  : # 1
  C  : # 1
  D  : ## 2
  F  :  0
------------------------------------
```

Add your own screenshots in [`docs/screenshots/`](docs/screenshots/).

## Testing
```bash
python -m unittest discover -v
```
40 tests cover grading boundaries, validation, storage (including corrupt files), the manager, reports and scripted menu sessions. Details: [`docs/testing.md`](docs/testing.md). Tests run automatically on every push through GitHub Actions.

## Documentation
| Document | Contents |
|----------|----------|
| [`statement.md`](statement.md) | Problem statement, scope, target users, high-level features |
| [`docs/requirements.md`](docs/requirements.md) | Functional and non-functional requirements |
| [`docs/design.md`](docs/design.md) | Architecture, use case, workflow, sequence, class and ER diagrams, design decisions |
| [`docs/testing.md`](docs/testing.md) | Test strategy, inventory, manual checklist |

## Future Enhancements
- Tkinter or web (Flask/Streamlit) interface
- SQLite storage instead of CSV
- Multiple classes/semesters and per-student report-card export (PDF)
- Login for teachers/students

## License
Released under the [MIT License](LICENSE).
