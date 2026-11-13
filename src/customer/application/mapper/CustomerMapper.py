from src.customer.application.dto.customer_create_request import CustomerCreateRequest

from ...application.dto.customer_request import CustomerRequest
from ...application.dto.customer_response import CustomerResponse
from ...domain.model.Customer import Customer

def request_to_domain(request: CustomerCreateRequest) -> Customer:

    return Customer(
        name=request.name,
        description=request.description,
        email=str(request.email),
        age=request.age
    )

def domain_to_response(domain: Customer) -> CustomerResponse:
    return CustomerResponse(
        id=domain.id,
        name=domain.name,
        description=domain.description,
        email=domain.email,
        age=str(domain.age)
    )