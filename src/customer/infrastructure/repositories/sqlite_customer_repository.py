from uuid import uuid4
from sqlmodel import SQLModel, Session, Field
from src.customer.domain.model import Customer
from src.customer.domain.repositories.customer_repository import CustomerRepository

class CustomerTable(SQLModel, table=True):
    __tablename__ = "customers"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    email: str
    description: str
    age: int

class SqliteCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self) -> list[Customer]:
        ...

    def get_by_id(self, id: str) -> Customer:
        ...

    def save(self, customer: Customer) -> None:
        ...