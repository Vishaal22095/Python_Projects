
# Lab Exercise 13: CSV-Based Payroll Management System
# Student Name: VISHAAL MS
# USN: 25BTRAD130

import csv
import io


# Function to generate CSV data
def generate_csv():

    rows = [
        ["EmpID", "Name", "Dept", "Basic", "Allowance"],
        ["EMP101", "Vishaal MS", "Data Engg", 75000, 15000],
        ["EMP102", "John Cena", "AI Research", 68000, 12000],
        ["EMP103", "Roman Reigns", "IT Ops", 55000, 10000]
    ]

    # Create CSV data in memory
    csv_data = io.StringIO()

    writer = csv.writer(csv_data)
    writer.writerows(rows)

    return csv_data.getvalue()


# Function to process payroll
def process_payroll(csv_data):

    print("\n" + "=" * 75)
    print("             EMPLOYEE PAYROLL REPORT")
    print("=" * 75)

    print(
        f"{'EmpID':<10}"
        f"{'Name':<16}"
        f"{'Gross':<14}"
        f"{'Deductions':<15}"
        f"{'Net Salary':<12}"
    )

    print("-" * 75)

    # Read CSV data from memory
    csv_file = io.StringIO(csv_data)

    reader = csv.DictReader(csv_file)

    for employee in reader:

        basic = float(employee["Basic"])
        allowance = float(employee["Allowance"])

        # Calculate gross salary
        gross = basic + allowance

        # Calculate deductions
        deductions = (0.12 * basic) + (0.10 * gross)

        # Calculate net salary
        net_salary = gross - deductions

        # Display employee payroll details
        print(
            f"{employee['EmpID']:<10}"
            f"{employee['Name']:<16}"
            f"{gross:<14,.2f}"
            f"{deductions:<15,.2f}"
            f"{net_salary:<12,.2f}"
        )

    print("=" * 75)


# Main program
if __name__ == "__main__":

    print("=== CSV Payroll Management System ===")

    print("\nStudent Name : VISHAAL MS")
    print("USN          : 25BTRAD130")

    # Generate CSV data
    payroll_data = generate_csv()

    print("\nCSV employee data generated successfully!")

    # Process employee payroll
    process_payroll(payroll_data)

    print("\nPayroll processing completed successfully!")
