import unittest

from srms import reports
from srms.models import Student


def make(roll, name, marks):
    return Student(roll, name, marks)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.students = [
            make("A1", "Asha", [90, 90, 90, 90, 90]),   # 450, A+, PASS
            make("B2", "Bela", [80, 80, 80, 80, 80]),   # 400, A,  PASS
            make("C3", "Chen", [80, 80, 80, 80, 80]),   # 400 (tie with Bela)
            make("D4", "Dev",  [30, 90, 90, 90, 90]),   # 390 = 78% -> B, but FAIL (30 < 40)
        ]

    def test_rank_list_handles_ties(self):
        ranks = [(r, s.name) for r, s in reports.rank_list(self.students)]
        self.assertEqual(ranks, [(1, "Asha"), (2, "Bela"), (2, "Chen"), (4, "Dev")])

    def test_subject_averages(self):
        avgs = reports.subject_averages(self.students)
        self.assertEqual(avgs["Physics"], (90 + 80 + 80 + 30) / 4)
        self.assertEqual(list(avgs)[0], "Physics")

    def test_grade_distribution_includes_all_grades(self):
        dist = reports.grade_distribution(self.students)
        self.assertEqual(dist, {"A+": 1, "A": 2, "B": 1, "C": 0, "D": 0, "F": 0})

    def test_class_summary(self):
        s = reports.class_summary(self.students)
        self.assertEqual((s["count"], s["passed"], s["failed"]), (4, 3, 1))
        self.assertEqual(s["pass_percentage"], 75.0)
        self.assertEqual(s["topper"].name, "Asha")
        self.assertEqual(s["lowest"].name, "Dev")

    def test_empty_class(self):
        self.assertEqual(reports.class_summary([]), {"count": 0})
        self.assertEqual(reports.subject_averages([]), {})
        self.assertEqual(reports.rank_list([]), [])


if __name__ == "__main__":
    unittest.main()
