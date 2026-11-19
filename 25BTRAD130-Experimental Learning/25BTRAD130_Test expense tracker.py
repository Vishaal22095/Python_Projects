"""Unit tests for the SQLite expense tracker in Main.py."""

import tempfile
import unittest
from pathlib import Path

from Main import ExpenseManager


class TestExpenseTracker(unittest.TestCase):
    """Each test gets a separate temporary database."""

    def setUp(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        database_file = Path(self.temp_folder.name) / "expenses_test.db"
        self.tracker = ExpenseManager(database_file)

    def tearDown(self):
        # Main.ExpenseManager closes SQLite connections after every operation,
        # so Windows can safely remove this temporary database here.
        self.temp_folder.cleanup()

    def test_add_expense_is_saved(self):
        added = self.tracker.add_expense(
            42.75, "Food", "Lunch", "2026-11-18"
        )

        saved = self.tracker.list_expenses()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["id"], added["id"])
        self.assertEqual(saved[0]["date"], "2026-11-18")
        self.assertEqual(saved[0]["category"], "Food")
        self.assertEqual(saved[0]["description"], "Lunch")
        self.assertEqual(saved[0]["amount"], 42.75)

    def test_month_filter_and_totals(self):
        self.tracker.add_expense(100, "Food", expense_date="2026-11-01")
        self.tracker.add_expense(25.50, "Food", expense_date="2026-11-15")
        self.tracker.add_expense(80, "Travel", expense_date="2026-10-20")

        november = self.tracker.list_expenses("2026-11")
        self.assertEqual(len(november), 2)
        self.assertEqual(self.tracker.total("2026-11"), 125.50)
        self.assertEqual(self.tracker.category_totals("2026-11"), {"Food": 125.50})

    def test_delete_expense(self):
        item = self.tracker.add_expense(12, "Travel", expense_date="2026-11-18")

        self.assertTrue(self.tracker.delete_expense(item["id"]))
        self.assertFalse(self.tracker.delete_expense(item["id"]))
        self.assertEqual(self.tracker.list_expenses(), [])

    def test_invalid_amount_category_and_date_are_rejected(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense(0, "Food")
        with self.assertRaises(ValueError):
            self.tracker.add_expense(10, " ")
        with self.assertRaises(ValueError):
            self.tracker.add_expense(10, "Food", expense_date="18-11-2026")


if __name__ == "__main__":
    unittest.main(verbosity=2)
