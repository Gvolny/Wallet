import argparse
import os
import sys
from decimal import Decimal
from typing import List, Dict


class FinancialRecord:
    """
    Represents a single financial record.

    Attributes:
        record_id (str): The unique identifier of the record.
        date (str): The date of the financial transaction.
        category (str): The category of the transaction (e.g., "Доход", "Расход").
        amount (Decimal): The amount of money involved in the transaction.
        description (str): A description of the transaction.
    """

    def __init__(
        self,
        record_id: str,
        date: str,
        category: str,
        amount: Decimal,
        description: str,
    ):
        self.record_id = record_id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class FinancialManager:
    """
    Manages financial records and operations.

    Attributes:
        filename (str): The name of the file to store financial records.
        records (List[Dict[str, str]]): A list of financial records.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.records = self.read_records()

    def read_records(self) -> List[Dict[str, str]]:
        """
        Reads financial records from a file.

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing financial records.
        """
        records = []
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                record = {}
                for line in file:
                    line = line.strip()
                    if not line:
                        records.append(record)
                        record = {}
                    else:
                        key, value = line.split(": ")
                        record[key] = value
        return records

    def write_records(self):
        """
        Writes financial records to a file.
        """
        with open(self.filename, "w") as file:
            for record in self.records:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")

    def edit_record(
        self, record_id: str, new_date: str, new_amount: Decimal, new_description: str
    ):
        """
        Edits an existing financial record.

        Args:
            record_id (str): The ID of the record to be edited.
            new_date (str): The new date for the record.
            new_amount (Decimal): The new amount for the record.
            new_description (str): The new description for the record.
        """
        for record in self.records:
            if record["ID"] == record_id:
                record["Дата"] = new_date
                record["Сумма"] = str(new_amount)
                record["Описание"] = new_description
                break

    def display_balance(self):
        """
        Displays the current balance.
        """
        total_income = sum(
            Decimal(record["Сумма"])
            for record in self.records
            if record["Категория"] == "Доход"
        )
        total_expense = sum(
            Decimal(record["Сумма"])
            for record in self.records
            if record["Категория"] == "Расход"
        )
        balance = total_income - total_expense
        print(f"Текущий баланс: {balance:.2f}")
        print(f"Доходы: {total_income:.2f}")
        print(f"Расходы: {total_expense:.2f}")

    def add_expense(self, date: str, amount: Decimal, description: str, last_id: int):
        """
        Adds a new expense record.

        Args:
            date (str): The date of the expense.
            amount (Decimal): The amount of the expense.
            description (str): The description of the expense.
            last_id (int): The ID of the last record.
        """
        new_record = {
            "ID": str(last_id + 1),
            "Дата": date,
            "Категория": "Расход",
            "Сумма": f"{amount:.2f}",
            "Описание": description,
        }
        self.records.append(new_record)

    def add_income(self, date: str, amount: Decimal, description: str, last_id: int):
        """
        Adds a new income record.

        Args:
            date (str): The date of the income.
            amount (Decimal): The amount of the income.
            description (str): The description of the income.
            last_id (int): The ID of the last record.
        """
        new_record = {
            "ID": str(last_id + 1),
            "Дата": date,
            "Категория": "Доход",
            "Сумма": f"{amount:.2f}",
            "Описание": description,
        }
        self.records.append(new_record)

    def search_by_category(self, category: str) -> List[Dict[str, str]]:
        """
        Searches for records by category.

        Args:
            category (str): The category to search for.

        Returns:
            List[Dict[str, str]]: A list of matching records.
        """
        return [record for record in self.records if record["Категория"] == category]

    def search_by_description(self, description: str) -> List[Dict[str, str]]:
        """
        Searches for records by description.

        Args:
            description (str): The description to search for.

        Returns:
            List[Dict[str, str]]: A list of matching records.
        """
        return [record for record in self.records if description in record["Описание"]]

    def search_by_date(self, date: str) -> List[Dict[str, str]]:
        """
        Searches for records by date.

        Args:
            date (str): The date to search for.

        Returns:
            List[Dict[str, str]]: A list of matching records.
        """
        return [record for record in self.records if record["Дата"] == date]

    def search_by_amount(self, amount: Decimal) -> List[Dict[str, str]]:
        """
        Searches for records by amount.

        Args:
            amount (Decimal): The amount to search for.

        Returns:
            List[Dict[str, str]]: A list of matching records.
        """
        return [record for record in self.records if Decimal(record["Сумма"]) == amount]

    def get_last_id(self) -> int:
        """
        Gets the ID of the last record.

        Returns:
            int: The ID of the last record.
        """
        return max(int(record["ID"]) for record in self.records) if self.records else 0

    def execute_command(self, args):
        """
        Executes a command based on the provided arguments.

        Args:
            args: The parsed command-line arguments.
        """
        last_id = self.get_last_id()
        if args.show:
            self.display_balance()
        elif args.add_expense:
            date, amount, description = args.add_expense
            self.add_expense(date, Decimal(amount), description, last_id)
        elif args.add_income:
            date, amount, description = args.add_income
            self.add_income(date, Decimal(amount), description, last_id)
        elif args.search_category:
            category_results = self.search_by_category(args.search_category)
            for result in category_results:
                print(result)
        elif args.search_date:
            date_results = self.search_by_date(args.search_date)
            for result in date_results:
                print(result)
        elif args.search_amount:
            amount_results = self.search_by_amount(Decimal(args.search_amount))
            for result in amount_results:
                print(result)
        elif args.search_description:
            description_results = self.search_by_description(args.search_description)
            for result in description_results:
                print(result)
        elif args.edit:
            record_id, new_date, new_amount, new_description = args.edit
            self.edit_record(record_id, new_date, Decimal(new_amount), new_description)


def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Личный финансовый кошелек")
    parser.add_argument("--show", action="store_true", help="Показать текущий баланс")
    parser.add_argument(
        "--add-expense",
        nargs=3,
        metavar=("date", "amount", "description"),
        help="Добавить запись о расходе",
    )
    parser.add_argument(
        "--add-income",
        nargs=3,
        metavar=("date", "amount", "description"),
        help="Добавить запись о доходе",
    )
    parser.add_argument(
        "--search-category",
        metavar=("category"),
        help="Поиск записей по категории",
    )
    parser.add_argument(
        "--search-date",
        metavar=("date"),
        help="Поиск записей по дате",
    )
    parser.add_argument(
        "--search-amount",
        metavar=("amount"),
        help="Поиск записей по сумме",
    )
    parser.add_argument(
        "--search-description",
        metavar=("description"),
        help="Поиск записей по описанию",
    )
    parser.add_argument(
        "--edit",
        nargs=4,
        metavar=("record_id", "new_date", "new_amount", "new_description"),
        help="Изменить существующую запись о доходе или расходе",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    return parser.parse_args()


def main():
    """
    A function that executes the main logic of the program.
    This function initializes a FinancialManager object with a given filename,
    parses command line arguments, executes a command based on the arguments, and writes records to a file.
    """
    filename = "finances.txt"
    financial_manager = FinancialManager(filename)
    args = parse_args()
    financial_manager.execute_command(args)
    financial_manager.write_records()


if __name__ == "__main__":
    main()
