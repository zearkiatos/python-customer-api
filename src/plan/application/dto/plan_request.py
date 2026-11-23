from pydantic import BaseModel

class PlanRequest(BaseModel):
    name: str
    description: str
    price: float