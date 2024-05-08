# Personal Wallet

A simple Python program for managing personal finances.

## Description

This project provides a command-line interface (CLI) for managing personal finances. It allows users to record income and expenses, search for transactions, edit existing records, and display balance summaries.

## Features

- Add new income or expense records
- Search for records by category, description, date, or amount
- Edit existing records
- Display balance summary

## Installation

1. Clone the repository:
`git clone https://github.com/Gvolny/Wallet`

2. Navigate to the project directory:
`cd Wallet`
3. Install the required packages: `pipenv install`
4. Activate the virtual environment: `pipenv shell`

## Usage

To run the program, execute the main script:

`python wallet.py [options]`

Options:
- `--show`: Display current balance
- `--add-expense [date] [amount] [description]`: Add a new expense record
- `--add-income [date] [amount] [description]`: Add a new income record
- `--search-category [category]`: Search records by category
- `--search-date [date]`: Search records by date
- `--search-amount [amount]`: Search records by amount
- `--search-description [description]`: Search records by description
- `--edit [record_id] [new_date] [new_amount] [new_description]`: Edit an existing record

## Testing

To run the tests and see coverage, execute:

`coverage run -m unittest tests/tests.py`

`coverage report -m`

## Example Data File

An example of a data file (`example.txt`) might look like this:

```
ID: 1
Дата: 2024-01-01
Категория: Доход
Сумма: 1000
Описание: Заработная плата

ID: 2
Дата: 2024-01-02
Категория: Расход
Сумма: 500
Описание: Покупка продуктов
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

