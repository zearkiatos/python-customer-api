from pydantic import BaseModel


class SubscribeCustomerPlanRequest(BaseModel):
    customer_id: str
    plan_id: str