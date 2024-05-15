import unittest
from unittest.mock import patch
import os
from io import StringIO
from decimal import Decimal

from financial_manager import FinancialManager


class TestFinancialManager(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_finances.txt"
        self.financial_manager = FinancialManager(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_read_records(self):
        # Create a test file with some records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": "1000.00",
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": "500.00",
                "Описание": "Test expense 1",
            },
        ]
        with open(self.test_filename, "w") as file:
            for record in test_records:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")

        # Test reading records from the file
        records = self.financial_manager.read_records()
        self.assertEqual(records, test_records)

    def test_write_records(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Write records to the file
        self.financial_manager.write_records()

        # Read records from the file to verify
        with open(self.test_filename, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 12)  # Each record has 4 lines + 2 blank lines

    def test_add_expense(self):
        # Test adding a new expense record
        self.financial_manager.add_expense(
            "2024-05-10", Decimal("200.00"), "Test expense"
        )
        self.assertEqual(len(self.financial_manager.records), 1)

    def test_add_income(self):
        # Test adding a new income record
        self.financial_manager.add_income(
            "2024-05-10", Decimal("500.00"), "Test income"
        )
        self.assertEqual(len(self.financial_manager.records), 1)

    def test_search_by_category(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test searching by category
        category_results = self.financial_manager.search_by_category("Доход")
        self.assertEqual(len(category_results), 1)

    def test_search_by_description(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test searching by description
        description_results = self.financial_manager.search_by_description(
            "Test income"
        )
        self.assertEqual(len(description_results), 1)

    def test_search_by_date(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test searching by date
        date_results = self.financial_manager.search_by_date("2024-01-01")
        self.assertEqual(len(date_results), 1)

    def test_search_by_amount(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test searching by amount
        amount_results = self.financial_manager.search_by_amount(Decimal("1000.00"))
        self.assertEqual(len(amount_results), 1)

    def test_edit_record(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1001.20"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("542.10"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test editing a record
        self.financial_manager.edit_record(
            "1", "2024-01-01", Decimal("1543.30"), "Updated income 1"
        )
        edited_record = self.financial_manager.records[0]
        edited_amount = Decimal(edited_record["Сумма"])  # Convert to Decimal
        self.assertEqual(edited_amount, Decimal("1543.30"))
        self.assertEqual(edited_record["Описание"], "Updated income 1")

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_balance(self, mock_stdout):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test displaying balance
        self.financial_manager.display_balance()
        output = mock_stdout.getvalue()
        self.assertIn("Текущий баланс", output)

    def test_get_last_id(self):
        # Prepare test records
        test_records = [
            {
                "ID": "1",
                "Дата": "2024-01-01",
                "Категория": "Доход",
                "Сумма": Decimal("1000.00"),
                "Описание": "Test income 1",
            },
            {
                "ID": "2",
                "Дата": "2024-01-02",
                "Категория": "Расход",
                "Сумма": Decimal("500.00"),
                "Описание": "Test expense 1",
            },
        ]
        self.financial_manager.records = test_records

        # Test getting last ID
        last_id = self.financial_manager.get_last_id()
        self.assertEqual(last_id, 2)


if __name__ == "__main__":
    unittest.main()
