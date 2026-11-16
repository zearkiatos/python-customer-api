from uuid import uuid4
from src.customer.domain.model.Customer import Customer
from src.customer.domain.repositories.customer_repository import CustomerRepository

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers: list[Customer] = []

    def get(self) -> list[Customer]:
        return self.customers

    def get_by_id(self, id: str) -> Customer | None:
        for customer in self.customers:
            if customer.id == id:
                return customer
        return None

    def save(self, customer: Customer) -> Customer:
        customer.id = str(uuid4())
            
        self.customers.append(customer)
        return customer

    def delete(self, id: str) -> None:
        self.customers.remove(next(customer for customer in self.customers if customer.id == id))

    def update(self, customer: Customer) -> Customer | None:
        for i, existing_customer in enumerate(self.customers):
            if existing_customer.id == customer.id:
                self.customers[i] = customer
                return customer
        return None