"""End-to-end style tests that drive the menu with scripted keyboard input."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from srms import cli
from srms.manager import StudentManager
from srms.storage import CSVStorage


class CLITests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = Path(self._tmp.name) / "students.csv"
        self.manager = StudentManager(CSVStorage(self.path))

    def drive(self, *keystrokes):
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=list(keystrokes)), contextlib.redirect_stdout(out):
            cli.main_loop(self.manager)
        return out.getvalue()

    def test_add_student_reprompts_on_bad_input_then_saves_on_exit(self):
        output = self.drive(
            "1", "Asha Rao", "21bce001",
            "abc", "150", "95", "88", "76", "90", "85",   # first two marks are rejected
            "0",
        )
        self.assertIn("Marks must be", output)
        self.assertIn("Student added!", output)
        self.assertIn("21BCE001", self.path.read_text())

    def test_duplicate_roll_number_is_reported_and_reprompted(self):
        self.manager.add("A1", "Existing", [50] * 5)
        output = self.drive("1", "New Person", "a1", "B2", *["60"] * 5, "0")
        self.assertIn("already exists", output)
        self.assertEqual(len(self.manager), 2)

    def test_invalid_menu_choice(self):
        self.assertIn("Invalid choice", self.drive("x", "0"))

    def test_search_missing_student_shows_error_not_crash(self):
        self.assertIn("No student with roll number", self.drive("3", "ZZZ", "0"))

    def test_delete_can_be_cancelled(self):
        self.manager.add("A1", "Asha", [50] * 5)
        self.drive("6", "A1", "n", "0")
        self.assertEqual(len(self.manager), 1)

    def test_delete_confirmed(self):
        self.manager.add("A1", "Asha", [50] * 5)
        self.drive("6", "A1", "y", "0")
        self.assertEqual(len(self.manager), 0)

    def test_reports_on_empty_database(self):
        output = self.drive("2", "7", "8", "0")
        self.assertEqual(output.count("No records yet."), 3)

    def test_class_report_and_rank_list(self):
        self.manager.add("A1", "Asha", [90] * 5)
        self.manager.add("B2", "Bela", [30, 90, 90, 90, 90])
        output = self.drive("7", "8", "0")
        self.assertIn("Pass percentage : 50.0%", output)
        self.assertIn("Topper          : Asha", output)


if __name__ == "__main__":
    unittest.main()
