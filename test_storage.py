import tempfile
import unittest
from pathlib import Path

from srms.exceptions import StorageError
from srms.models import Student
from srms.storage import CSVStorage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = Path(self._tmp.name) / "sub" / "students.csv"
        self.storage = CSVStorage(self.path)

    def test_missing_file_loads_empty(self):
        self.assertEqual(self.storage.load(), [])

    def test_round_trip(self):
        original = [Student("A1", "Asha Rao", [90, 80, 70, 60, 50]),
                    Student("B2", "O'Neil Jr", [1, 2, 3, 4, 5])]
        self.storage.save(original)
        loaded = self.storage.load()
        self.assertEqual([(s.roll_no, s.name, s.marks) for s in loaded],
                         [(s.roll_no, s.name, s.marks) for s in original])

    def test_save_creates_parent_folder_and_leaves_no_temp_files(self):
        self.storage.save([])
        self.assertTrue(self.path.exists())
        self.assertEqual([p.name for p in self.path.parent.iterdir()], ["students.csv"])

    def test_corrupt_rows_are_skipped_not_fatal(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text(
            "roll_no,name,Physics,Maths,Python,Electronics,English\n"
            "A1,Asha,90,80,70,60,50\n"
            "B2,Bad Marks,abc,80,70,60,50\n"     # non-numeric
            "C3,Too Few,1,2\n"                   # wrong column count
            "D4,Over,101,0,0,0,0\n"              # out of range
            "\n"                                 # blank line
            "E5,Eve,40,40,40,40,40\n",
            encoding="utf-8",
        )
        loaded = self.storage.load()
        self.assertEqual([s.roll_no for s in loaded], ["A1", "E5"])
        self.assertEqual(self.storage.skipped_rows, 3)

    def test_unreadable_path_raises_storage_error(self):
        # A directory where the file should be -> cannot be read as a file
        self.path.mkdir(parents=True)
        with self.assertRaises(StorageError):
            self.storage.load()

    def test_save_failure_raises_storage_error(self):
        blocker = Path(self._tmp.name) / "blocker"
        blocker.write_text("i am a file")
        with self.assertRaises(StorageError):
            CSVStorage(blocker / "students.csv").save([])


if __name__ == "__main__":
    unittest.main()
