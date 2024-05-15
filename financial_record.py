from decimal import Decimal


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
