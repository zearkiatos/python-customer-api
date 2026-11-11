from pydantic import BaseModel, EmailStr

class CustomerRequest(BaseModel):
    name: str
    description: str | None
    email: EmailStr
    age: int