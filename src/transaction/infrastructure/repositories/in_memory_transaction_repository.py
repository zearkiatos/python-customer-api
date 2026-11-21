from src.transaction.domain.model.Transaction import Transaction
from src.transaction.domain.repositories.transaction_repository import TransactionRepository

class InMemoryTransactionRepository(TransactionRepository):
    def __init__(self):
        self.transactions: list[Transaction] = []

    def get(self) -> list[Transaction]:
        return self.transactions

    def get_by_id(self, id: int) -> Transaction | None:
        for transaction in self.transactions:
            if transaction.id == id:
                return transaction
        return None

    def save(self, transaction: Transaction) -> Transaction:
        self.transactions.append(transaction)
        return transaction

    def delete(self, id: int) -> None:
        self.transactions.remove(next(transaction for transaction in self.transactions if transaction.id == id))

    def update(self, id: int, transaction: Transaction) -> Transaction | None:
        for i, t in enumerate(self.transactions):
            if t.id == id:
                self.transactions[i] = transaction
                return transaction
        return None