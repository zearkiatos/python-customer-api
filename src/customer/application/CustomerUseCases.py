
from src.customer.application.dto.customer_create_request import CustomerCreateRequest
from src.customer.application.dto.customer_response import CustomerResponse
from src.customer.application.mapper import CustomerMapper
from src.customer.domain.repositories.customer_repository import CustomerRepository


class CustomerUseCases:
    def __init__(self, customer_input_port, customer_repository: CustomerRepository):
        self.customer_input_port = customer_input_port
        self.customer_repository = customer_repository

    def create_customer(self, customer_data: CustomerCreateRequest) -> CustomerResponse:
        customer = CustomerMapper.request_to_domain(customer_data)
        
        self.customer_repository.save(customer)

        return CustomerMapper.domain_to_response(customer)

    def get_customers(self) -> list[CustomerResponse]:
        customers = self.customer_repository.get()
        return [CustomerMapper.domain_to_response(customer) for customer in customers]