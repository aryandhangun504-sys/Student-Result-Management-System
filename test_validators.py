import unittest

from srms.exceptions import ValidationError
from srms.validators import (validate_marks, validate_marks_list,
                             validate_name, validate_roll_no)


class NameTests(unittest.TestCase):
    def test_valid_names_are_cleaned(self):
        self.assertEqual(validate_name("  Asha   Rao "), "Asha Rao")
        self.assertEqual(validate_name("Mary-Jane O'Neil"), "Mary-Jane O'Neil")

    def test_invalid_names(self):
        for bad in ["", "   ", "R2D2", "Robert,Jr", "9lives", "x" * 51]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                validate_name(bad)


class RollNoTests(unittest.TestCase):
    def test_normalised_to_upper_case(self):
        self.assertEqual(validate_roll_no(" 21bce001 "), "21BCE001")

    def test_invalid_roll_numbers(self):
        for bad in ["", "  ", "AB 12", "A,B", "x" * 21, "١٢٣"]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                validate_roll_no(bad)


class MarksTests(unittest.TestCase):
    def test_valid_marks(self):
        self.assertEqual(validate_marks("0"), 0)
        self.assertEqual(validate_marks(" 100 "), 100)
        self.assertEqual(validate_marks(55), 55)

    def test_invalid_marks(self):
        for bad in ["", "abc", "-1", "101", "12.5", "1e2", "²"]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                validate_marks(bad)

    def test_marks_list_needs_one_value_per_subject(self):
        self.assertEqual(validate_marks_list(["1", "2", "3", "4", "5"]), [1, 2, 3, 4, 5])
        with self.assertRaises(ValidationError):
            validate_marks_list([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
