"""Report generation functions."""
import os
from datetime import datetime

from results import total_score, average_score, assign_grade

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
WIDTH = 60


def report_card(student):
    """Return a formatted report card for one student."""
    avg = average_score(student.scores)
    lines = [
        "=" * WIDTH,
        "STUDENT REPORT CARD".center(WIDTH),
        "=" * WIDTH,
        f"ID     : {student.student_id}",
        f"Name   : {student.full_name}",
        f"Class  : {student.student_class}",
        f"Gender : {student.gender}",
        f"DOB    : {student.dob}",
        f"Entered: {student.result_date or 'Not recorded'}",
        "-" * WIDTH,
        f"{'Subject':<30}{'Score':>10}",
    ]
    for subject, score in student.scores.items():
        lines.append(f"{subject:<30}{score:>10.1f}")
    lines += [
        "-" * WIDTH,
        f"Total   : {total_score(student.scores):.1f}",
        f"Average : {avg:.2f}",
        f"Grade   : {assign_grade(avg)}",
        "=" * WIDTH,
    ]
    return "\n".join(lines)


def results_table(students):
    """Return a table of every student's total, average and grade (in the order given)."""
    if not students:
        return "No students to display."
    header = f"{'ID':<14}{'Name':<22}{'Total':>8}{'Average':>10}{'Grade':>7}"
    lines = [header, "-" * len(header)]
    for s in students:
        avg = average_score(s.scores)
        lines.append(
            f"{s.student_id:<14}{s.full_name[:21]:<22}"
            f"{total_score(s.scores):>8.1f}{avg:>10.2f}{assign_grade(avg):>7}"
        )
    return "\n".join(lines)


def class_statistics(students):
    """Return highest, lowest and class average (based on student averages)."""
    graded = [s for s in students if s.scores]
    if not graded:
        return "No graded students yet."
    averages = [(average_score(s.scores), s.full_name) for s in graded]
    best = max(averages)
    worst = min(averages)
    class_avg = round(sum(a for a, _ in averages) / len(averages), 2)
    return "\n".join([
        "CLASS STATISTICS",
        "-" * WIDTH,
        f"Students graded : {len(graded)}",
        f"Highest average : {best[0]:.2f} ({best[1]})",
        f"Lowest average  : {worst[0]:.2f} ({worst[1]})",
        f"Class average   : {class_avg:.2f}",
    ])


def save_report(text, name_prefix="results"):
    """Save text to a timestamped file in the reports folder. Returns the file path."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(REPORTS_DIR, f"{name_prefix}_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return path
