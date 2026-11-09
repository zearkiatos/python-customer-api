
from src.customer.application.dto.customer_request import CustomerRequest
from src.customer.application.dto.customer_response import CustomerResponse
from src.customer.application.mapper import CustomerMapper


class CustomerUseCases:
    def __init__(self, customer_input_port):
        self.customer_input_port = customer_input_port

    def create_customer(self, customer_data: CustomerRequest) -> CustomerResponse:
        customer = CustomerMapper.request_to_domain(customer_data)

        return CustomerMapper.domain_to_response(customer)