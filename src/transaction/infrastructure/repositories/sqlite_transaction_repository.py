
from uuid import uuid4
from sqlmodel import Relationship, SQLModel, Session, Field, select
from src.transaction.domain.model.Transaction import Transaction
from src.transaction.domain.repositories.transaction_repository import TransactionRepository

class TransactionTable(SQLModel, table=True):
    __tablename__ = "transactions"

    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    amount: int = Field(default=0)
    description: str = Field(None)
    customer_id: str = Field(foreign_key="customers.id", index=True)
    customer: "CustomerTable" = Relationship(back_populates="transactions")

class SqliteTransactionRepository(TransactionRepository):
    def __init__(self, session):
        self.session = session

    @staticmethod
    def _to_table(transaction: Transaction) -> TransactionTable:
        return TransactionTable(
            id=transaction.id,
            amount=transaction.amount,
            description=transaction.description,
            customer_id=transaction.customer_id
        )

    @staticmethod
    def _to_domain(table: TransactionTable) -> Transaction:
        return Transaction(
            id=table.id,
            amount=table.amount,
            description=table.description,
            customer_id=table.customer_id
        )

    def get(self)->list[Transaction]:
        transactions = self.session.exec(select(TransactionTable)).all()
        return [self._to_domain(t) for t in transactions]

    def get_by_id(self, id: str) -> Transaction | None:
        transaction = self.session.get(TransactionTable, id)
        if transaction is None:
            return None
        return self._to_domain(transaction)

    def save(self, transaction: Transaction) -> Transaction:
        transaction_table = self._to_table(transaction)
        self.session.add(transaction_table)
        self.session.commit()
        self.session.refresh(transaction_table)
        return self._to_domain(transaction_table)

    def delete(self, id: str) -> None:
        transaction = self.session.get(TransactionTable, id)
        if transaction is not None:
            self.session.delete(transaction)
            self.session.commit()

    def update(self, transaction: Transaction) -> Transaction | None:
        transaction_table = self.session.get(TransactionTable, transaction.id)
        if transaction_table is None:
            return None
        transaction_table.amount = transaction.amount
        transaction_table.description = transaction.description
        transaction_table.customer_id = transaction.customer_id
        self.session.add(transaction_table)
        self.session.commit()
        self.session.refresh(transaction_table)
        return self._to_domain(transaction_table)