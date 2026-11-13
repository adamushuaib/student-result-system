# Student Result Management System

A console application written in Python for managing student records, subject scores, grades and reports. Data is saved to a JSON file so it persists between runs.
Author: Adamu Shuaib Adamu
Matric No: 24/SCI01/002
Department: Computer Science
GitHub: adamushuaib

## Requirements

- Python 3.8 or newer (no third-party packages needed)

## How to run

1. Open the `student_result_system` folder in VS Code.
2. Open a terminal (Terminal > New Terminal).
3. Run:

   ```bash
   python main.py
   ```

   On macOS/Linux you may need `python3 main.py`.

## Features

- **Student management:** add, view, search (by ID or name), update and delete students.
- **Scores:** record or update scores for five subjects (0-100); total, average and grade are calculated automatically.
- **Grading:** A (70+), B (60-69), C (50-59), D (40-49), F (below 40).
- **Reports:** individual report card, all results sorted by average or name, class statistics (highest, lowest, class average), and a text report saved to the `reports/` folder.
- **Persistence:** data is stored in `data/students.json` and loaded automatically on start. A missing or corrupted file is handled safely.

## Project structure

```
student_result_system/
├── main.py       # Entry point and main menu
├── student.py    # Student class and validation helpers
├── results.py    # Score calculation and grading logic
├── storage.py    # Load and save data (JSON)
├── reports.py    # Report generation and saving
├── data/
│   └── students.json   # Created automatically on first save
└── README.md
```

## Python concepts used

- Variables, data types and type conversion (`float()` for scores, `strptime` for dates)
- Flow control: `if/elif/else`, `for` and `while` loops
- Lists, tuples and dictionaries (student list, score dictionary, grade bands)
- Functions with parameters and return values
- Sorting with `sorted()` and `key=` lambdas
- Exception handling with `try / except / else / finally`
- File handling with JSON (`json.load`, `json.dump`) and `os`
- Modules: code split across several `.py` files and imported
- Object-oriented programming: the `Student` class with `to_dict` and `from_dict`
- Dates and times with `datetime`
- Regular expressions for validating Student IDs

## Repository

https://github.com/adamushuaib/student-result-system.git

## Author

Adamu Shuaib Adamu - 24/Sci01/002 - Computer Science
