
# Lab Exercise 12: Student Data Manager
# Using Python Data Structures
# Student Name: VISHAAL MS
# USN: 25BTRAD130


# Initialize student database
students = []


# Function to add student details
def add_student(usn, name, gpa):

    student = {
        "usn": usn,
        "name": name,
        "gpa": float(gpa)
    }

    students.append(student)

    print(f"Saved: {name} ({usn})")


# Function to search student using USN
def search_student(usn):

    for student in students:

        if student["usn"] == usn:

            return (
                f"USN: {student['usn']} | "
                f"Name: {student['name']} | "
                f"GPA: {student['gpa']:.2f}"
            )

    return "Student Not Found"


# Function to display all student records
def display_all():

    print("\n========== STUDENT DETAILS ==========")

    print(f"{'USN':<15} {'Name':<18} {'GPA':<5}")

    print("-" * 40)

    for student in students:

        print(
            f"{student['usn']:<15} "
            f"{student['name']:<18} "
            f"{student['gpa']:<5.2f}"
        )

    print("-" * 40)


# Main program
if __name__ == "__main__":

    print("=" * 45)
    print("       STUDENT DATA MANAGER")
    print("=" * 45)

    print("Student Name : VISHAAL MS")
    print("USN          : 25BTRAD130")

    # Adding student records
    print("\nAdding Student Records...")

    add_student("25BTRAD130", "VISHAAL MS", 9.45)

    add_student("25BTRAD131", "JOHN CENA", 8.80)

    add_student("25BTRAD132", "DAVID", 9.10)

    # Display all student records
    display_all()

    # Search student using USN
    print("\n========== SEARCH RESULT ==========")

    result = search_student("25BTRAD130")

    print(result)

    print("=" * 45)

    print("\nStudent Data Management Completed Successfully!")
