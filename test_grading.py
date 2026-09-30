import unittest

from srms import grading


class GradingTests(unittest.TestCase):
    def test_grade_boundaries(self):
        cases = {100: "A+", 90: "A+", 89.99: "A", 80: "A", 79.9: "B", 70: "B",
                 69: "C", 60: "C", 59: "D", 50: "D", 49.99: "F", 0: "F"}
        for pct, expected in cases.items():
            with self.subTest(pct=pct):
                self.assertEqual(grading.get_grade(pct), expected)

    def test_percentage(self):
        self.assertEqual(grading.calculate_percentage([90] * 5), 90.0)
        self.assertEqual(grading.calculate_percentage([100, 0, 100, 0, 100]), 60.0)
        self.assertEqual(grading.calculate_percentage([]), 0.0)

    def test_percentage_has_no_float_error_at_boundary(self):
        # 285/500 = 57% exactly; naive float maths gives 56.99999...
        self.assertEqual(grading.calculate_percentage([57] * 5), 57.0)

    def test_pass_requires_40_in_every_subject(self):
        self.assertEqual(grading.get_result([40, 40, 40, 40, 40]), "PASS")
        self.assertEqual(grading.get_result([100, 100, 100, 100, 39]), "FAIL")

    def test_total(self):
        self.assertEqual(grading.calculate_total([1, 2, 3]), 6)


if __name__ == "__main__":
    unittest.main()
