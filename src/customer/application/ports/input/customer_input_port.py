
from typing import Protocol
from src.customer.application.dto.customer_request import CustomerRequest
from src.customer.application.dto.customer_response import CustomerResponse

class CustomerInputPort(Protocol):
    def create_customer(self, customer_data: CustomerRequest) -> CustomerResponse:
        ...

    def get_customers(self) -> list[CustomerResponse]:
        ...

    def get_customer_by_id(self, id: str) -> CustomerResponse | None:
        ...

    def delete_customer(self, id: str) -> None:
        ...

    def update_customer(self, id: str, customer_data: CustomerRequest) -> CustomerResponse:
        ...