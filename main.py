import sys
import argparse

from financial_manager import FinancialManager


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
