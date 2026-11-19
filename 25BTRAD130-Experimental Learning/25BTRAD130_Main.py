#!/usr/bin/env python3
"""Interactive, SQLite-backed command line expense tracker."""

import sqlite3
from datetime import date, datetime
from pathlib import Path


class ExpenseManager:
    def __init__(self, database_path="expenses.db"):
        self.database_path = Path(database_path)
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expense_date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0)
                )
            """)

    def _connect(self):
        return sqlite3.connect(self.database_path)

    @staticmethod
    def _convert(row):
        return {"id": row[0], "date": row[1], "category": row[2],
                "description": row[3], "amount": row[4] / 100}

    def add_expense(self, amount, category, description="", expense_date=None):
        amount = round(float(amount), 2)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        category = category.strip()
        if not category:
            raise ValueError("Category cannot be empty.")
        expense_date = expense_date or date.today().isoformat()
        datetime.strptime(expense_date, "%Y-%m-%d")
        cents = round(amount * 100)
        description = description.strip()
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO expenses (expense_date, category, description, amount_cents) "
                "VALUES (?, ?, ?, ?)",
                (expense_date, category, description, cents),
            )
            expense_id = cursor.lastrowid
        return {"id": expense_id, "date": expense_date, "category": category,
                "description": description, "amount": cents / 100}

    def list_expenses(self, month=None):
        query = "SELECT id, expense_date, category, description, amount_cents FROM expenses"
        parameters = ()
        if month:
            datetime.strptime(month, "%Y-%m")
            query += " WHERE expense_date LIKE ?"
            parameters = (month + "-%",)
        query += " ORDER BY expense_date DESC, id DESC"
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._convert(row) for row in rows]

    def category_totals(self, month):
        datetime.strptime(month, "%Y-%m")
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT category, SUM(amount_cents) FROM expenses "
                "WHERE expense_date LIKE ? GROUP BY category ORDER BY category COLLATE NOCASE",
                (month + "-%",),
            ).fetchall()
        return {category: cents / 100 for category, cents in rows}

    def total(self, month=None):
        query = "SELECT COALESCE(SUM(amount_cents), 0) FROM expenses"
        parameters = ()
        if month:
            datetime.strptime(month, "%Y-%m")
            query += " WHERE expense_date LIKE ?"
            parameters = (month + "-%",)
        with self._connect() as connection:
            cents = connection.execute(query, parameters).fetchone()[0]
        return cents / 100

    def delete_expense(self, expense_id):
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cursor.rowcount > 0

    def has_expenses(self):
        with self._connect() as connection:
            return connection.execute("SELECT EXISTS(SELECT 1 FROM expenses)").fetchone()[0]


def print_banner():
    print("=" * 52)
    print("                 EXPENSE TRACKER")
    print("=" * 52)


def print_menu():
    print("\n[1] Add expense")
    print("[2] List expenses")
    print("[3] Monthly summary")
    print("[4] Delete expense")
    print("[5] Exit")


def add_expense(manager):
    print("\n--- Add Expense ---")
    amount = float(input("Amount: "))
    category = input("Category (food, travel, etc.): ")
    description = input("Description (optional): ")
    date_text = input("Date YYYY-MM-DD (Enter for today): ").strip() or None
    item = manager.add_expense(amount, category, description, date_text)
    print(f"Saved expense #{item['id']} for {item['amount']:.2f}.")


def list_expenses(manager):
    expenses = manager.list_expenses()
    if not expenses:
        print("No expenses saved yet.")
        return
    print(f"\n{'ID':<5}{'Date':<13}{'Category':<18}{'Description':<25}{'Amount':>10}")
    print("-" * 71)
    for item in expenses:
        print(f"{item['id']:<5}{item['date']:<13}{item['category'][:16]:<18}"
              f"{item['description'][:23]:<25}{item['amount']:>10.2f}")
    print("-" * 71)
    print(f"Total: {manager.total():.2f}")


def monthly_summary(manager):
    month = input("Month (YYYY-MM): ").strip()
    items = manager.list_expenses(month)
    print(f"\nSummary for {month}")
    if not items:
        print("No expenses recorded for this month.")
        return
    for category, amount in sorted(manager.category_totals(month).items()):
        print(f"{category:<20}{amount:>10.2f}")
    print(f"{'Total':<20}{manager.total(month):>10.2f}")
    print(f"Transactions: {len(items)}")


def delete_expense(manager):
    list_expenses(manager)
    if not manager.has_expenses():
        return
    expense_id = int(input("Enter the ID to delete: "))
    if manager.delete_expense(expense_id):
        print("Expense deleted.")
    else:
        print("No expense has that ID.")


def main():
    try:
        manager = ExpenseManager()
    except ValueError as error:
        print(f"Could not open expense data: {error}")
        return
    print_banner()
    actions = {"1": add_expense, "2": list_expenses,
               "3": monthly_summary, "4": delete_expense}
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Choose a number from 1 to 5.")
            continue
        try:
            action(manager)
        except ValueError as error:
            print(f"Invalid input: {error}")
        except OSError as error:
            print(f"Could not save the expense: {error}")


if __name__ == "__main__":
    main()
