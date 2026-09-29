"""
analyzer.py
-----------
All the calculation logic for the Student Performance Analyzer.
This file has no GUI code, so the functions can be tested on their own.
"""

# The five subjects used in this project
SUBJECTS = ["Python", "Java", "DBMS", "Computer Networks", "Artificial Intelligence"]

MAX_MARKS_PER_SUBJECT = 100
PASS_MARK_PER_SUBJECT = 40   # a student must score at least 40 in every subject


def validate_name(name):
    """Return an error message if the name is invalid, otherwise None."""
    name = name.strip()
    if name == "":
        return "Please enter the student's name."
    # Allow letters, spaces and dots (e.g. "R. Kumar")
    for ch in name:
        if not (ch.isalpha() or ch == " " or ch == "."):
            return "Name should contain only letters, spaces and dots."
    return None


def validate_mark(subject, value):
    """
    Check one mark entered by the user.
    Returns (mark, error). If the mark is valid, error is None.
    """
    value = value.strip()
    if value == "":
        return None, f"Please enter marks for {subject}."

    try:
        mark = float(value)
    except ValueError:
        return None, f"Marks for {subject} must be a number."

    if mark < 0 or mark > MAX_MARKS_PER_SUBJECT:
        return None, f"Marks for {subject} must be between 0 and 100."

    return mark, None


def get_grade(percentage):
    """Return the grade for a given percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def get_result_status(marks, grade):
    """
    Pass only if:
      1. every subject is at least 40, and
      2. the overall grade is not F (percentage 50 or above)
    """
    for mark in marks.values():
        if mark < PASS_MARK_PER_SUBJECT:
            return "Fail"
    if grade == "F":
        return "Fail"
    return "Pass"


def get_highest_subjects(marks):
    """Return a list of subject(s) with the highest mark (handles ties)."""
    highest_mark = max(marks.values())
    top_subjects = []
    for subject, mark in marks.items():
        if mark == highest_mark:
            top_subjects.append(subject)
    return top_subjects, highest_mark


def get_performance_message(percentage, status):
    """Return a short message based on the percentage and pass/fail status."""
    if status == "Fail":
        return "Needs Improvement"
    elif percentage >= 80:
        return "Excellent Performance"
    elif percentage >= 60:
        return "Good Performance"
    else:
        return "Needs Improvement"


def analyze(name, marks):
    """
    Main function: takes the student name and a dictionary of marks,
    and returns a dictionary with all the results.
    """
    total = sum(marks.values())
    average = total / len(marks)
    max_total = MAX_MARKS_PER_SUBJECT * len(marks)
    percentage = (total / max_total) * 100

    grade = get_grade(percentage)
    status = get_result_status(marks, grade)
    top_subjects, top_mark = get_highest_subjects(marks)
    message = get_performance_message(percentage, status)

    # Subjects where the student scored below the pass mark
    weak_subjects = [s for s, m in marks.items() if m < PASS_MARK_PER_SUBJECT]

    return {
        "name": name.strip(),
        "total": total,
        "max_total": max_total,
        "average": average,
        "percentage": percentage,
        "grade": grade,
        "status": status,
        "top_subjects": top_subjects,
        "top_mark": top_mark,
        "message": message,
        "weak_subjects": weak_subjects,
    }


def format_number(value):
    """Show 85.0 as 85, but keep 85.5 as 85.5."""
    if value == int(value):
        return str(int(value))
    return f"{value:.2f}"
