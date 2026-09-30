# Testing

## How to run
```bash
python -m unittest discover -v
```
No extra packages are needed. (`pytest` also works if you have it: `pytest -v`.)

## Approach
- **Unit tests** for pure logic: grading rules, validators, reports.
- **Integration tests** for manager + storage using a temporary directory, so real data is never touched.
- **Scripted UI tests** (`test_cli.py`): the menu is driven with fake keyboard input to check prompts, re-prompting and messages end to end.
- **Boundary-value testing** for grades (89.99 / 90 / 79.9 / 80 ...), marks (-1, 0, 100, 101) and the 39/40 pass mark.
- **Negative testing** for corrupt CSV rows, unreadable files, unwritable folders, duplicate and missing students.

## Test inventory (40 tests)

| File | What it checks |
|------|----------------|
| `test_grading.py` | Grade boundaries, percentage, float-safe 57% case, pass mark 39 vs 40, total |
| `test_validators.py` | Name cleaning/rejection, roll-number normalisation, marks 0-100, non-numeric, decimal, unicode digits, list length |
| `test_storage.py` | Missing file, save/load round trip, parent folder creation, no leftover temp files, corrupt rows skipped, unreadable path, unwritable path |
| `test_manager.py` | Add/get, duplicates, invalid data leaves state unchanged, update recalculates result, delete, search, sorting, save + reload |
| `test_reports.py` | Rank ties (1,2,2,4), subject averages, grade distribution, class summary, empty class |
| `test_cli.py` | Re-prompt on bad marks, duplicate roll number, invalid menu choice, missing student, delete cancel/confirm, empty-database reports, class report output |

## Manual test checklist
- [ ] Run with no `data/students.csv` -> "Loaded 0 record(s)."
- [ ] Add a student, exit with `0`, restart -> the student is still there
- [ ] Press Ctrl+C after adding a student -> changes are auto-saved
- [ ] Edit the CSV by hand to break a row -> warning shown, other rows still load
- [ ] Set `SRMS_DATA_FILE` to a read-only folder and choose `0` -> error shown, program does not exit
