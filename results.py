"""Score calculation and grading logic."""

# The five subjects every student must have scores for.
SUBJECTS = ["Mathematics", "English Language", "Physics", "Chemistry", "Biology"]

# (minimum average, grade) pairs, checked from highest to lowest.
GRADE_BANDS = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]


def parse_score(text):
    """Convert user input to a float between 0 and 100. Raises ValueError if invalid."""
    value = float(text)                     # ValueError if not a number
    if not 0 <= value <= 100:
        raise ValueError("score must be between 0 and 100.")
    return value


def total_score(scores):
    """Sum of all subject scores."""
    return sum(scores.values())


def average_score(scores):
    """Average of all subject scores, rounded to 2 decimals (0.0 if no scores)."""
    if not scores:
        return 0.0
    return round(total_score(scores) / len(scores), 2)


def assign_grade(average):
    """Return the letter grade for an average."""
    for minimum, grade in GRADE_BANDS:
        if average >= minimum:
            return grade
    return "F"
