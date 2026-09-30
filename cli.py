"""Console user interface. All input()/print() lives in this module."""

from __future__ import annotations

import logging
from typing import Callable

from . import reports
from .config import DATA_FILE, MAX_MARKS, MAX_TOTAL, SUBJECTS
from .exceptions import DuplicateStudentError, SRMSError, StorageError
from .logger import setup_logging
from .manager import StudentManager
from .models import Student
from .storage import CSVStorage
from .validators import validate_marks, validate_name, validate_roll_no

log = logging.getLogger(__name__)

MENU = """
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
 0. Save and exit"""


# ---------- input helpers ----------------------------------------------
def prompt_valid(label: str, validator: Callable):
    """Keep asking until the validator accepts the input."""
    while True:
        try:
            return validator(input(f"{label}: "))
        except SRMSError as exc:
            print(f"  ! {exc}")


def ask_all_marks() -> list:
    return [prompt_valid(f"Marks in {s} (0-{MAX_MARKS})", validate_marks) for s in SUBJECTS]


# ---------- display helpers --------------------------------------------
def show_student(s: Student) -> None:
    print("\n--------------------------------")
    print(f"{'Name':<12}: {s.name}")
    print(f"{'Roll no':<12}: {s.roll_no}")
    for subject, mark in s.subject_marks().items():
        print(f"{subject:<12}: {mark}")
    print(f"{'Total':<12}: {s.total} / {MAX_TOTAL}")
    print(f"{'Percentage':<12}: {s.percentage:.2f}%")
    print(f"{'Grade':<12}: {s.grade}")
    print(f"{'Result':<12}: {s.result}")
    print("--------------------------------")


def show_table(students, ranks=None) -> None:
    rank_col = f"{'Rank':<6}" if ranks else ""
    print(f"\n{rank_col}{'Roll no':<12}{'Name':<24}{'Total':<8}{'Percent':<10}{'Grade':<7}Result")
    print("-" * (55 + (6 if ranks else 0) + 5))
    for i, s in enumerate(students):
        rank = f"{ranks[i]:<6}" if ranks else ""
        pct = f"{s.percentage:.2f}%"
        print(f"{rank}{s.roll_no:<12}{s.name:<24}{s.total:<8}{pct:<10}{s.grade:<7}{s.result}")


# ---------- menu actions -----------------------------------------------
def add_student(m: StudentManager) -> None:
    name = prompt_valid("Enter name", validate_name)
    while True:
        roll_no = prompt_valid("Enter roll number", validate_roll_no)
        if not m.exists(roll_no):
            break
        print(f"  ! Roll number '{roll_no}' already exists.")
    student = m.add(roll_no, name, ask_all_marks())
    print("Student added!")
    show_student(student)


def view_students(m: StudentManager) -> None:
    if not len(m):
        print("No records yet.")
        return
    show_table(m.all())


def search_by_roll(m: StudentManager) -> None:
    roll_no = prompt_valid("Enter roll number to search", validate_roll_no)
    show_student(m.get(roll_no))


def search_by_name(m: StudentManager) -> None:
    query = input("Enter (part of) name: ")
    found = m.search_by_name(query)
    if not found:
        print("No matching students.")
    else:
        show_table(found)


def update_student(m: StudentManager) -> None:
    roll_no = prompt_valid("Enter roll number to update", validate_roll_no)
    student = m.get(roll_no)
    print(f"Updating marks for {student.name}")
    show_student(m.update_marks(roll_no, ask_all_marks()))
    print("Updated!")


def delete_student(m: StudentManager) -> None:
    roll_no = prompt_valid("Enter roll number to delete", validate_roll_no)
    student = m.get(roll_no)
    confirm = input(f"Delete {student.name} ({student.roll_no})? (y/n): ").strip().lower()
    if confirm == "y":
        m.delete(roll_no)
        print("Student deleted.")
    else:
        print("Cancelled.")


def rank_list(m: StudentManager) -> None:
    if not len(m):
        print("No records yet.")
        return
    ranked = reports.rank_list(m.all())
    show_table([s for _, s in ranked], ranks=[r for r, _ in ranked])


def class_report(m: StudentManager) -> None:
    students = m.all()
    summary = reports.class_summary(students)
    if summary["count"] == 0:
        print("No records yet.")
        return
    print("\n----------- CLASS REPORT -----------")
    print(f"Students        : {summary['count']}")
    print(f"Passed / Failed : {summary['passed']} / {summary['failed']}")
    print(f"Pass percentage : {summary['pass_percentage']:.1f}%")
    print(f"Class average   : {summary['class_average']:.2f}%")
    print(f"Topper          : {summary['topper'].name} ({summary['topper'].total}/{MAX_TOTAL})")
    print(f"Lowest scorer   : {summary['lowest'].name} ({summary['lowest'].total}/{MAX_TOTAL})")
    print("\nSubject averages:")
    for subject, avg in reports.subject_averages(students).items():
        print(f"  {subject:<12}: {avg:.1f}")
    print("\nGrade distribution:")
    for grade, count in reports.grade_distribution(students).items():
        print(f"  {grade:<3}: {'#' * count} {count}")
    print("------------------------------------")


def save_records(m: StudentManager) -> bool:
    """Returns True if saved. Errors are shown to the user, never raised."""
    try:
        count = m.save()
    except StorageError as exc:
        print(f"Error: {exc}")
        return False
    print(f"{count} record(s) saved.")
    return True


# ---------- main loop ---------------------------------------------------
def main_loop(m: StudentManager) -> None:
    actions = {
        "1": add_student, "2": view_students, "3": search_by_roll,
        "4": search_by_name, "5": update_student, "6": delete_student,
        "7": rank_list, "8": class_report, "9": save_records,
    }
    while True:
        print(MENU)
        choice = input("Enter choice (0-9): ").strip()
        if choice == "0":
            if save_records(m):
                print("Thank you for using the Student Result Management System.")
                return
            print("Could not save, so the program will not exit. Fix the problem or try again.")
        elif choice in actions:
            try:
                actions[choice](m)
            except SRMSError as exc:
                print(f"Error: {exc}")
                log.warning("Action %s failed: %s", choice, exc)
            except Exception:  # last line of defence; the app must not crash mid-session
                log.exception("Unexpected error in action %s", choice)
                print("Something went wrong. Details were written to the log file.")
        else:
            print("Invalid choice. Please enter a number from 0 to 9.")


def run() -> int:
    setup_logging()
    log.info("Application started")
    manager = StudentManager(CSVStorage(DATA_FILE))
    try:
        count = manager.load()
    except StorageError as exc:
        print(f"Error: {exc}")
        return 1
    print(f"Loaded {count} record(s).")
    if manager.skipped_rows:
        print(f"Warning: {manager.skipped_rows} invalid row(s) were skipped (see logs/srms.log).")
    try:
        main_loop(manager)
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted.")
        if manager.dirty:
            print("Saving unsaved changes...")
            save_records(manager)
    log.info("Application stopped")
    return 0
