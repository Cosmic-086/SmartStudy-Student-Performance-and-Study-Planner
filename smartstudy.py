# SmartStudy - Student Performance & Study Planner
# Course: 2026CSAE100 - Computational Thinking and Programming
# A beginner-friendly menu-driven Python project.

import csv
import os

FILE_NAME = "students.csv"
SUBJECTS = ["Mathematics", "Python", "Digital Design", "Electrical", "English"]
FIELDS = ["Name", "Roll Number"] + SUBJECTS


def load_students():
    """Read student records from the CSV file."""
    students = []
    if not os.path.exists(FILE_NAME):
        return students

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = {
                    "name": row["Name"],
                    "roll": row["Roll Number"],
                    "marks": {}
                }
                for subject in SUBJECTS:
                    student["marks"][subject] = float(row[subject])
                students.append(student)
    except (ValueError, KeyError, OSError):
        print("Could not read the student file. Please check students.csv.")

    return students


def save_students(students):
    """Save all student records in CSV format."""
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

        for student in students:
            row = {
                "Name": student["name"],
                "Roll Number": student["roll"]
            }
            for subject in SUBJECTS:
                row[subject] = student["marks"][subject]
            writer.writerow(row)


def get_valid_marks(subject):
    """Ask until the user enters marks between 0 and 100."""
    while True:
        try:
            marks = float(input("Enter marks in " + subject + " (0-100): "))
            if 0 <= marks <= 100:
                return marks
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a number, for example 78 or 85.5.")


def add_student(students):
    print("\n--- Add Student ---")
    name = input("Enter student name: ").strip()
    roll = input("Enter roll number: ").strip()

    if name == "" or roll == "":
        print("Name and roll number cannot be empty.")
        return

    for student in students:
        if student["roll"].lower() == roll.lower():
            print("This roll number already exists.")
            return

    marks = {}
    for subject in SUBJECTS:
        marks[subject] = get_valid_marks(subject)

    students.append({"name": name, "roll": roll, "marks": marks})
    save_students(students)
    print("Student record saved successfully.")


def display_students(students):
    print("\n--- Student Records ---")
    if len(students) == 0:
        print("No student records found.")
        return

    for student in students:
        print("\nName:", student["name"])
        print("Roll Number:", student["roll"])
        for subject in SUBJECTS:
            print(subject + ":", student["marks"][subject])


def calculate_average(student):
    total = 0
    for subject in SUBJECTS:
        total = total + student["marks"][subject]
    return total / len(SUBJECTS)


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "Needs Improvement"


def analyze_student(students):
    print("\n--- Performance Analysis ---")
    roll = input("Enter roll number: ").strip()

    for student in students:
        if student["roll"].lower() == roll.lower():
            average = calculate_average(student)
            highest_subject = max(student["marks"], key=student["marks"].get)
            lowest_subject = min(student["marks"], key=student["marks"].get)

            print("\nStudent:", student["name"])
            print("Average:", round(average, 2))
            print("Grade:", calculate_grade(average))
            print("Highest subject:", highest_subject,
                  "(", student["marks"][highest_subject], ")")
            print("Lowest subject:", lowest_subject,
                  "(", student["marks"][lowest_subject], ")")
            return

    print("Student not found.")


def show_ranking(students):
    print("\n--- Class Ranking ---")
    if len(students) == 0:
        print("No student records available.")
        return

    ranked_students = sorted(students, key=calculate_average, reverse=True)
    for position, student in enumerate(ranked_students, start=1):
        average = calculate_average(student)
        print(str(position) + ".", student["name"],
              "| Average:", round(average, 2),
              "| Grade:", calculate_grade(average))


def study_recommendations(students):
    print("\n--- Study Recommendations ---")
    roll = input("Enter roll number: ").strip()

    for student in students:
        if student["roll"].lower() == roll.lower():
            print("Student:", student["name"])
            for subject in SUBJECTS:
                marks = student["marks"][subject]
                if marks < 50:
                    priority = "HIGH - Focus first"
                elif marks < 70:
                    priority = "MEDIUM - Revise regularly"
                else:
                    priority = "LOW - Maintain revision"

                print(subject + ":", marks, "->", priority)
            return

    print("Student not found.")


def generate_class_report(students):
    """Create a simple text summary of the class."""
    if len(students) == 0:
        print("No records available to create a report.")
        return

    with open("class_report.txt", "w") as file:
        file.write("SMARTSTUDY - CLASS PERFORMANCE REPORT\n")
        file.write("-------------------------------------\n")
        file.write("Total students: " + str(len(students)) + "\n\n")

        ranked_students = sorted(students, key=calculate_average, reverse=True)
        for position, student in enumerate(ranked_students, start=1):
            file.write(
                str(position) + ". " + student["name"] +
                " (" + student["roll"] + ") - Average: " +
                str(round(calculate_average(student), 2)) +
                ", Grade: " + calculate_grade(calculate_average(student)) + "\n"
            )

    print("Class report generated as class_report.txt.")


def main():
    students = load_students()

    while True:
        print("\n========== SMARTSTUDY ==========")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Analyze a Student")
        print("4. Show Class Ranking")
        print("5. Study Recommendations")
        print("6. Generate Class Report")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            analyze_student(students)
        elif choice == "4":
            show_ranking(students)
        elif choice == "5":
            study_recommendations(students)
        elif choice == "6":
            generate_class_report(students)
        elif choice == "7":
            print("Thank you for using SmartStudy!")
            break
        else:
            print("Invalid choice. Please select from 1 to 7.")


if __name__ == "__main__":
    main()
