from pydantic import BaseModel

class PlanResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float