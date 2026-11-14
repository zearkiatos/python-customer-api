from uuid import uuid4
from sqlmodel import SQLModel, Session, Field, select
from src.customer.domain.model.Customer import Customer
from src.customer.domain.repositories.customer_repository import CustomerRepository

class CustomerTable(SQLModel, table=True):
    __tablename__ = "customers"

    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    name: str = Field(default=None)
    email: str = Field(default=None)
    description: str = Field(default=None)
    age: int = Field(default=0)

class SqliteCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _to_table(customer: Customer) -> CustomerTable:
        return CustomerTable(
            name=customer.name,
            email=customer.email,
            description=customer.description,
            age=customer.age
        )
        
    @staticmethod
    def _to_domain(table: CustomerTable) -> Customer:
        return Customer(
            id=table.id,
            name=table.name,
            email=table.email,
            description=table.description,
            age=table.age
        )

    def get(self) -> list[Customer]:
        customers = self.session.exec(select(CustomerTable)).all()
        return [self._to_domain(customer) for customer in customers]

    def get_by_id(self, id: str) -> Customer | None:
        customer = self.session.get(CustomerTable, id)
        if customer is None:
            return None
        return self._to_domain(customer)

    def save(self, customer: Customer) -> Customer:
        customer_table = self._to_table(customer)
        self.session.add(customer_table)
        self.session.commit()

        self.session.refresh(customer_table)
        return self._to_domain(customer_table)