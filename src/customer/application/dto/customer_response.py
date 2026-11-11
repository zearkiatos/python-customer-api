from pydantic import BaseModel

class CustomerResponse(BaseModel):
    id: str
    name: str
    description: str
    email: str
    age: str