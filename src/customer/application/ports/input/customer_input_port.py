
from typing import Protocol
from customer.application.dto.customer_request import CustomerRequest
from customer.application.dto.customer_response import CustomerResponse

class CustomerInputPort(Protocol):
    def create_customer(self, customer_data: CustomerRequest) -> CustomerResponse:
        ...

    def get_customers(self) -> list[CustomerResponse]:
        ...