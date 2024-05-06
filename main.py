import argparse
import os
import uuid


def read_records(filename):
    records = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
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


def write_records(filename, records):
    with open(filename, "w") as file:
        for record in records:
            for key, value in record.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")


def display_balance(records):
    total_income = sum(
        float(record["Сумма"]) for record in records if record["Категория"] == "Доход"
    )
    total_expense = sum(
        float(record["Сумма"]) for record in records if record["Категория"] == "Расход"
    )
    balance = total_income - total_expense
    print(f"Текущий баланс: {balance}")
    print(f"Доходы: {total_income}")
    print(f"Расходы: {total_expense}")


def add_expense(records, date, amount, description):
    new_record = {
        "ID": str(uuid.uuid4()),
        "Дата": date,
        "Категория": "Расход",
        "Сумма": amount,
        "Описание": description,
    }
    records.append(new_record)


def add_income(records, date, amount, description):
    new_record = {
        "ID": str(uuid.uuid4()),
        "Дата": date,
        "Категория": "Доход",
        "Сумма": amount,
        "Описание": description,
    }
    records.append(new_record)


def search_by_category(records, category):
    return [record for record in records if record["Категория"] == category]


def search_by_date(records, date):
    return [record for record in records if record["Дата"] == date]


def search_by_amount(records, amount):
    return [record for record in records if float(record["Сумма"]) == amount]


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
    return parser.parse_args()


def execute_command(args, records):
    if args.show:
        display_balance(records)
    elif args.add_expense:
        date, amount, description = args.add_expense
        add_expense(records, date, amount, description)
    elif args.add_income:
        date, amount, description = args.add_income
        add_income(records, date, amount, description)
    elif args.search_category:
        category_results = search_by_category(records, args.search_category)
        for result in category_results:
            print(result)
    elif args.search_date:
        date_results = search_by_date(records, args.search_date)
        for result in date_results:
            print(result)
    elif args.search_amount:
        amount_results = search_by_amount(records, float(args.search_amount))
        for result in amount_results:
            print(result)


def main():
    filename = "finances.txt"
    records = read_records(filename)
    args = parse_args()
    execute_command(args, records)
    write_records(filename, records)


if __name__ == "__main__":
    main()
