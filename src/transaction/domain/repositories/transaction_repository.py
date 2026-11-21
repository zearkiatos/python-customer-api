from typing import Protocol
from src.transaction.domain.model.Transaction import Transaction

class TransactionRepository(Protocol):
    def get(self)-> list[Transaction]:
        ...

    def get_by_id(self, id: int) -> Transaction | None:
        ...

    def save(self, transaction: Transaction) -> Transaction:
        ...

    def delete(self, id: int) -> None:
        ...

    def update(self, id: int, transaction: Transaction) -> Transaction | None:
        ...