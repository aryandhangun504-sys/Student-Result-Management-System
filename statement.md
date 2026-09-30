# Project Statement

## Problem Statement
Colleges and coaching centres often record student marks on paper or in loose spreadsheets. Totals, percentages, grades and pass/fail decisions are calculated by hand, which is slow and error-prone. Duplicate roll numbers, out-of-range marks and typing mistakes go unnoticed, and there is no quick way to see class-level results such as the topper or the pass percentage.

This project provides a small, reliable console application that stores student marks, validates every input, calculates results automatically using a fixed grading policy, and produces ranking and class-level reports.

## Scope
**In scope**
- Managing student records (add, view, search, update, delete)
- Automatic calculation of total, percentage, grade and PASS/FAIL
- Ranking and class analytics (pass percentage, averages, grade distribution)
- Persistent storage in a CSV file, with logging and input validation
- Single-user, offline, command-line use on Windows, macOS or Linux (Python 3.8+)

**Out of scope**
- Graphical or web interface
- Multi-user access, login and role management
- Multiple classes/semesters or per-subject credit weighting

## Target Users
- Teachers or class coordinators who need to record and review results for one class
- Students learning Python, who can read the code as an example of a modular, tested application

## High-Level Features
1. **Student management** - add, view, search (by roll number or name), update marks, delete with confirmation
2. **Result processing** - total, percentage, grade (A+ to F) and PASS/FAIL (40 marks needed in every subject)
3. **Reports and analytics** - rank list with tie handling, topper, pass percentage, subject averages, grade distribution
4. **Persistence** - automatic loading on start, atomic saving to CSV, tolerance for corrupt rows
5. **Safety** - strict input validation, custom error handling, rotating log file
