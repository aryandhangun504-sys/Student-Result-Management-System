import tempfile
import unittest
from pathlib import Path

from srms.exceptions import (DuplicateStudentError, StudentNotFoundError,
                             ValidationError)
from srms.manager import StudentManager
from srms.storage import CSVStorage


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = Path(self._tmp.name) / "students.csv"
        self.m = StudentManager(CSVStorage(self.path))

    def test_add_and_get(self):
        s = self.m.add("21bce001", "  Asha  Rao ", ["90", "80", "70", "60", "50"])
        self.assertEqual((s.roll_no, s.name, s.marks), ("21BCE001", "Asha Rao", [90, 80, 70, 60, 50]))
        self.assertIs(self.m.get("21bce001"), s)
        self.assertTrue(self.m.dirty)

    def test_duplicate_roll_number_rejected(self):
        self.m.add("A1", "Asha", [50] * 5)
        with self.assertRaises(DuplicateStudentError):
            self.m.add("a1", "Someone Else", [60] * 5)
        self.assertEqual(len(self.m), 1)

    def test_invalid_data_rejected_and_nothing_added(self):
        with self.assertRaises(ValidationError):
            self.m.add("A1", "Asha", [50, 50, 50, 50, 101])
        self.assertEqual(len(self.m), 0)

    def test_update_recalculates_result(self):
        self.m.add("A1", "Asha", [30, 90, 90, 90, 90])
        self.assertEqual(self.m.get("A1").result, "FAIL")
        self.m.update_marks("A1", [60, 90, 90, 90, 90])
        self.assertEqual(self.m.get("A1").result, "PASS")

    def test_update_missing_student(self):
        with self.assertRaises(StudentNotFoundError):
            self.m.update_marks("NOPE", [1] * 5)

    def test_delete(self):
        self.m.add("A1", "Asha", [50] * 5)
        self.m.delete("A1")
        self.assertEqual(len(self.m), 0)
        with self.assertRaises(StudentNotFoundError):
            self.m.delete("A1")

    def test_search_by_name_is_case_insensitive_partial(self):
        self.m.add("A1", "Asha Rao", [50] * 5)
        self.m.add("B2", "Ravi Kumar", [50] * 5)
        self.assertEqual([s.roll_no for s in self.m.search_by_name("RAO")], ["A1"])
        self.assertEqual(self.m.search_by_name("zzz"), [])
        self.assertEqual(self.m.search_by_name("  "), [])

    def test_all_is_sorted_by_roll_number(self):
        for roll in ["C3", "A1", "B2"]:
            self.m.add(roll, "Name", [50] * 5)
        self.assertEqual([s.roll_no for s in self.m.all()], ["A1", "B2", "C3"])

    def test_save_and_reload(self):
        self.m.add("A1", "Asha", [90, 80, 70, 60, 50])
        self.m.save()
        self.assertFalse(self.m.dirty)
        fresh = StudentManager(CSVStorage(self.path))
        self.assertEqual(fresh.load(), 1)
        self.assertEqual(fresh.get("A1").marks, [90, 80, 70, 60, 50])


if __name__ == "__main__":
    unittest.main()
