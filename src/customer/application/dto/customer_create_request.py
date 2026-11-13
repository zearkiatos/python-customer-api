from pydantic import BaseModel, EmailStr
from .customer_request import CustomerRequest

class CustomerCreateRequest(CustomerRequest):
    name: str
    description: str | None
    email: EmailStr
    age: int