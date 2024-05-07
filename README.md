# Personal Finance Manager

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
`git clone https://github.com/your-username/personal-finance-manager.git`

2. Navigate to the project directory:
`cd personal-finance-manager`


## Usage

To run the program, execute the main script:

`python main.py [options]`

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


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

