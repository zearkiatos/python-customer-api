from pydantic import BaseModel


class SubscribeCustomerPlanUpdate(BaseModel):
    state: str
