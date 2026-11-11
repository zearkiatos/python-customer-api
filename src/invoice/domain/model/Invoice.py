from src.invoice.domain.model.Transaction import Transaction

class Invoice:
    def __init__(self, id: str, name: str, customer_id: str, transactions: list[Transaction] ):
        self.id = id
        self.name = name
        self.customer_id = customer_id
        self.transactions = transactions

    @property
    def total(self) -> int:
        return sum(transaction.amount for transaction in self.transactions)