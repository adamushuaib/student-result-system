"""
Student Result Management System
--------------------------------
Student Name : Adamu Shuaib Adamu
Matric No.   : 24/Sci01/002
Department   : Computer Science
Course       : Introduction to Python Programming

Entry point and main menu. Run with:  python main.py
"""
from datetime import datetime

import reports
from results import SUBJECTS, parse_score, average_score, assign_grade
from storage import load_students, save_students
from student import Student, validate_id, validate_date

MENU = """
==== STUDENT RESULT MANAGEMENT SYSTEM ====
 1. Add student
 2. View all students
 3. Search student (by ID or name)
 4. Update student information
 5. Delete student
 6. Record / update scores
 7. View report card
 8. Results sorted by average (highest first)
 9. Results sorted by name
10. Class statistics
11. Save text report to file
 0. Exit
"""


# ---------- helpers ----------

def ask(prompt):
    return input(prompt).strip()


def find_student(students, student_id):
    for s in students:
        if s.student_id.lower() == student_id.lower():
            return s
    return None


def pick_student(students):
    """Ask for an ID and return the matching student, or None."""
    sid = ask("Enter student ID: ")
    student = find_student(students, sid)
    if student is None:
        print("No student found with that ID.")
    return student


def save(students):
    """Convert all students to dictionaries and write them to the JSON file."""
    save_students([s.to_dict() for s in students])


# ---------- student management ----------

def add_student(students):
    print("\n-- Add New Student --")
    sid = ask("Student ID (e.g. ABU-2026-001): ")
    if not validate_id(sid):
        print("Invalid ID. Use 3-20 letters, digits, '/' or '-'.")
        return
    if find_student(students, sid):
        print("A student with this ID already exists.")
        return
    name = ask("Full name: ")
    if not name:
        print("Name cannot be empty.")
        return
    student_class = ask("Class/Form (e.g. SS1): ")
    gender = ask("Gender (M/F): ").upper()
    if gender not in ("M", "F"):
        print("Gender must be M or F.")
        return
    dob = ask("Date of birth (YYYY-MM-DD): ")
    if not validate_date(dob):
        print("Invalid date. Use YYYY-MM-DD.")
        return

    students.append(Student(sid, name, student_class, gender, dob))
    save(students)
    print(f"Student {name} added.")


def view_students(students):
    if not students:
        print("No students registered yet.")
        return
    print("\n-- All Students --")
    for s in students:
        print(f"{s.student_id:<14} {s.full_name:<25} {s.student_class:<8} {s.gender:<3} {s.dob}")


def search_student(students):
    term = ask("Search by ID or name: ").lower()
    matches = [s for s in students
               if term in s.student_id.lower() or term in s.full_name.lower()]
    if not matches:
        print("No matching students.")
    for s in matches:
        print(s)


def update_student(students):
    student = pick_student(students)
    if student is None:
        return
    print("Press Enter to keep the current value.")
    name = ask(f"Full name [{student.full_name}]: ")
    cls = ask(f"Class [{student.student_class}]: ")
    gender = ask(f"Gender [{student.gender}]: ").upper()
    dob = ask(f"Date of birth [{student.dob}]: ")

    if name:
        student.full_name = name
    if cls:
        student.student_class = cls
    if gender in ("M", "F"):
        student.gender = gender
    if dob:
        if validate_date(dob):
            student.dob = dob
        else:
            print("Invalid date - date not changed.")
    save(students)
    print("Student updated.")


def delete_student(students):
    student = pick_student(students)
    if student is None:
        return
    if ask(f"Delete {student.full_name}? (yes/no): ").lower() == "yes":
        students.remove(student)
        save(students)
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


# ---------- scores and results ----------

def record_scores(students):
    """Record scores for every subject. Press Enter to keep an existing score."""
    student = pick_student(students)
    if student is None:
        return
    print(f"Enter scores (0-100) for {student.full_name}. "
          "Press Enter to keep an existing score.")
    for subject in SUBJECTS:
        current = student.scores.get(subject)
        label = f"  {subject}" + (f" [{current}]" if current is not None else "") + ": "
        while True:
            text = ask(label)
            if text == "" and current is not None:
                break                       # keep the old score
            try:
                student.scores[subject] = parse_score(text)
                break
            except ValueError as error:
                print(f"  Invalid: {error}")
    student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    save(students)
    avg = average_score(student.scores)
    print(f"Scores saved. Average {avg:.2f} - Grade {assign_grade(avg)}.")


def view_report_card(students):
    student = pick_student(students)
    if student is None:
        return
    if not student.scores:
        print("No scores recorded for this student yet.")
        return
    print(reports.report_card(student))


def show_results(students, sort_by):
    if sort_by == "average":
        ordered = sorted(students, key=lambda s: average_score(s.scores), reverse=True)
    else:
        ordered = sorted(students, key=lambda s: s.full_name.lower())
    print(reports.results_table(ordered))


def save_text_report(students):
    text = "\n\n".join([
        reports.results_table(sorted(students,
                                     key=lambda s: average_score(s.scores),
                                     reverse=True)),
        reports.class_statistics(students),
    ])
    path = reports.save_report(text)
    print(f"Report saved to: {path}")


# ---------- main loop ----------

def load_all():
    students = []
    for record in load_students():
        try:
            students.append(Student.from_dict(record))
        except TypeError:
            print(f"Skipping malformed record: {record}")
    return students


def main():
    students = load_all()
    print(f"{len(students)} student(s) loaded.")

    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        try:
            if choice == "1":
                add_student(students)
            elif choice == "2":
                view_students(students)
            elif choice == "3":
                search_student(students)
            elif choice == "4":
                update_student(students)
            elif choice == "5":
                delete_student(students)
            elif choice == "6":
                record_scores(students)
            elif choice == "7":
                view_report_card(students)
            elif choice == "8":
                show_results(students, "average")
            elif choice == "9":
                show_results(students, "name")
            elif choice == "10":
                print(reports.class_statistics(students))
            elif choice == "11":
                save_text_report(students)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option, try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except Exception as error:          # last-resort safety net
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
