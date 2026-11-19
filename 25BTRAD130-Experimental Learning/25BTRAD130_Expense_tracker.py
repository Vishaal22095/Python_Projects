"""SQLite-backed expense tracking logic."""

import sqlite3
from datetime import date, datetime
from pathlib import Path


class ExpenseManager:
    def __init__(self, database_path="expenses.db"):
        self.database_path = Path(database_path)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _create_table(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
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

    @staticmethod
    def _as_dict(row):
        return {
            "id": row[0],
            "date": row[1],
            "category": row[2],
            "description": row[3],
            "amount": row[4] / 100,
        }

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
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO expenses (expense_date, category, description, amount_cents) "
                "VALUES (?, ?, ?, ?)",
                (expense_date, category, description.strip(), cents),
            )
            expense_id = cursor.lastrowid
        return {"id": expense_id, "date": expense_date, "category": category,
                "description": description.strip(), "amount": cents / 100}

    def list_expenses(self, month=None):
        query = "SELECT id, expense_date, category, description, amount_cents FROM expenses"
        parameters = ()
        if month is not None:
            datetime.strptime(month, "%Y-%m")
            query += " WHERE expense_date LIKE ?"
            parameters = (month + "-%",)
        query += " ORDER BY expense_date DESC, id DESC"
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._as_dict(row) for row in rows]

    def category_totals(self, month=None):
        query = "SELECT category, SUM(amount_cents) FROM expenses"
        parameters = ()
        if month is not None:
            datetime.strptime(month, "%Y-%m")
            query += " WHERE expense_date LIKE ?"
            parameters = (month + "-%",)
        query += " GROUP BY category ORDER BY category COLLATE NOCASE"
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return {category: cents / 100 for category, cents in rows}

    def total(self, month=None):
        query = "SELECT COALESCE(SUM(amount_cents), 0) FROM expenses"
        parameters = ()
        if month is not None:
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
            return connection.execute("SELECT EXISTS(SELECT 1 FROM expenses)").fetchone()[0] == 1
