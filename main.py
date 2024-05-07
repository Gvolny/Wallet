import argparse
import os
import sys

class FinancialRecord:
    def __init__(self, record_id, date, category, amount, description):
        self.record_id = record_id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

class FinancialManager:
    def __init__(self, filename):
        self.filename = filename
        self.records = self.read_records()

    def read_records(self):
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
        with open(self.filename, "w") as file:
            for record in self.records:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")

    def edit_record(self, record_id, new_date, new_amount, new_description):
        for record in self.records:
            if record["ID"] == record_id:
                record["Дата"] = new_date
                record["Сумма"] = new_amount
                record["Описание"] = new_description
                break

    def display_balance(self):
        total_income = sum(
            float(record["Сумма"]) for record in self.records if record["Категория"] == "Доход"
        )
        total_expense = sum(
            float(record["Сумма"]) for record in self.records if record["Категория"] == "Расход"
        )
        balance = total_income - total_expense
        print(f"Текущий баланс: {balance}")
        print(f"Доходы: {total_income}")
        print(f"Расходы: {total_expense}")

    def add_expense(self, date, amount, description, last_id):
        new_record = {
            "ID": str(last_id + 1),
            "Дата": date,
            "Категория": "Расход",
            "Сумма": amount,
            "Описание": description,
        }
        self.records.append(new_record)

    def add_income(self, date, amount, description, last_id):
        new_record = {
            "ID": str(last_id + 1),
            "Дата": date,
            "Категория": "Доход",
            "Сумма": amount,
            "Описание": description,
        }
        self.records.append(new_record)

    def search_by_category(self, category):
        return [record for record in self.records if record["Категория"] == category]

    def search_by_description(self, description):
        return [record for record in self.records if description in record["Описание"]]

    def search_by_date(self, date):
        return [record for record in self.records if record["Дата"] == date]

    def search_by_amount(self, amount):
        return [record for record in self.records if float(record["Сумма"]) == amount]


def parse_args():
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
        "--edit-record",
        nargs=4,
        metavar=("record_id", "new_date", "new_amount", "new_description"),
        help="Изменить существующую запись о доходе или расходе",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    return parser.parse_args()


def execute_command(args, financial_manager, last_id):
    if args.show:
        financial_manager.display_balance()
    elif args.add_expense:
        date, amount, description = args.add_expense
        financial_manager.add_expense(date, amount, description, last_id)
    elif args.add_income:
        date, amount, description = args.add_income
        financial_manager.add_income(date, amount, description, last_id)
    elif args.search_category:
        category_results = financial_manager.search_by_category(args.search_category)
        for result in category_results:
            print(result)
    elif args.search_date:
        date_results = financial_manager.search_by_date(args.search_date)
        for result in date_results:
            print(result)
    elif args.search_amount:
        amount_results = financial_manager.search_by_amount(float(args.search_amount))
        for result in amount_results:
            print(result)
    elif args.search_description:
        description_results = financial_manager.search_by_description(args.search_description)
        for result in description_results:
            print(result)
    elif args.edit_record:
        record_id, new_date, new_amount, new_description = args.edit_record
        financial_manager.edit_record(record_id, new_date, new_amount, new_description)


def main():
    filename = "finances.txt"
    financial_manager = FinancialManager(filename)
    args = parse_args()
    last_id = max(int(record["ID"]) for record in financial_manager.records) if financial_manager.records else 0
    execute_command(args, financial_manager, last_id)
    financial_manager.write_records()

if __name__ == "__main__":
    main()
