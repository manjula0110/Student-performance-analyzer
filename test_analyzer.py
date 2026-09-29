"""
test_analyzer.py
----------------
Basic tests for the calculation logic.
Run with:  python -m unittest test_analyzer.py
"""

import unittest
from analyzer import get_grade, validate_mark, validate_name, analyze


class TestAnalyzer(unittest.TestCase):

    def test_grades(self):
        self.assertEqual(get_grade(95), "A+")
        self.assertEqual(get_grade(90), "A+")
        self.assertEqual(get_grade(89.8), "A")
        self.assertEqual(get_grade(80), "A")
        self.assertEqual(get_grade(75), "B")
        self.assertEqual(get_grade(65), "C")
        self.assertEqual(get_grade(50), "D")
        self.assertEqual(get_grade(49.9), "F")

    def test_mark_validation(self):
        self.assertEqual(validate_mark("Java", "85"), (85.0, None))
        self.assertIsNotNone(validate_mark("Java", "")[1])
        self.assertIsNotNone(validate_mark("Java", "abc")[1])
        self.assertIsNotNone(validate_mark("Java", "-5")[1])
        self.assertIsNotNone(validate_mark("Java", "101")[1])

    def test_name_validation(self):
        self.assertIsNone(validate_name("Ravi Kumar"))
        self.assertIsNone(validate_name("R. Priya"))
        self.assertIsNotNone(validate_name("   "))
        self.assertIsNotNone(validate_name("Ravi123"))

    def test_excellent_student(self):
        marks = {"Python": 95, "Java": 88, "DBMS": 92,
                 "Computer Networks": 85, "Artificial Intelligence": 90}
        r = analyze("Ananya", marks)
        self.assertEqual(r["total"], 450)
        self.assertEqual(r["percentage"], 90)
        self.assertEqual(r["grade"], "A+")
        self.assertEqual(r["status"], "Pass")
        self.assertEqual(r["top_subjects"], ["Python"])
        self.assertEqual(r["message"], "Excellent Performance")

    def test_fail_in_one_subject(self):
        marks = {"Python": 80, "Java": 35, "DBMS": 75,
                 "Computer Networks": 70, "Artificial Intelligence": 72}
        r = analyze("Kiran", marks)
        self.assertEqual(r["grade"], "C")
        self.assertEqual(r["status"], "Fail")
        self.assertEqual(r["weak_subjects"], ["Java"])
        self.assertEqual(r["message"], "Needs Improvement")

    def test_tie_for_highest(self):
        marks = {"Python": 90, "Java": 90, "DBMS": 60,
                 "Computer Networks": 70, "Artificial Intelligence": 65}
        r = analyze("Sneha", marks)
        self.assertEqual(r["top_subjects"], ["Python", "Java"])


if __name__ == "__main__":
    unittest.main()
