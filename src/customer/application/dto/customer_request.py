from pydantic import BaseModel

class CustomerRequest(BaseModel):
    name: str
    description: str | None
    email: str
    age: int