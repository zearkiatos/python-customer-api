from typing import Protocol
from ...domain.model.Customer import Customer

class CustomerRepository(Protocol):
    def get(self) -> list[Customer]:
        ...

    def get_by_id(self, id: str) -> Customer | None:
        ...

    def save(self, customer: Customer) -> None:
        ...