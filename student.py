"""Student class and related helper functions."""
import re
from datetime import datetime

ID_PATTERN = re.compile(r"^[A-Za-z0-9/-]{3,20}$")


class Student:
    """Holds one student's personal details and subject scores."""

    def __init__(self, student_id, full_name, student_class, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id
        self.full_name = full_name
        self.student_class = student_class
        self.gender = gender
        self.dob = dob                      # stored as "YYYY-MM-DD"
        self.scores = scores if scores is not None else {}
        self.result_date = result_date      # date/time the scores were entered

    def to_dict(self):
        """Convert the student into a dictionary so it can be saved as JSON."""
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Student from a dictionary loaded from JSON."""
        return cls(**data)

    def __str__(self):
        return f"{self.student_id} - {self.full_name} ({self.student_class})"


def validate_id(student_id):
    """Return True if the ID matches the allowed pattern (uses a regular expression)."""
    return bool(ID_PATTERN.match(student_id))


def validate_date(text):
    """Return True if text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False
