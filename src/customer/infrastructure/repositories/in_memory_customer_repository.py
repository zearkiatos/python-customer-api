from uuid import uuid4
from src.customer.domain.model import Customer
from src.customer.domain.repositories.customer_repository import CustomerRepository

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers: list[Customer] = []

    def get(self) -> list[Customer]:
        return self.customers

    def get_by_id(self, id: str) -> Customer:
        for customer in self.customers:
            if customer.id == id:
                return customer
        return None

    def save(self, customer: Customer) -> None:
        customer.id = str(uuid4())
            
        self.customers.append(customer)