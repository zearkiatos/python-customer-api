from pydantic import BaseModel

class CustomerPlanResponse(BaseModel):
    id: str
    customer_id: str
    plan_id: str