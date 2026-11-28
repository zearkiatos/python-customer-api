from enum import Enum

class CustomerPlanStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    
class CustomerPlan:
    def __init__(
        self, id: str, customer_id: str, plan_id: str,
        state: CustomerPlanStatus = CustomerPlanStatus.ACTIVE,
    ):
        self.id = id
        self.customer_id = customer_id
        self.plan_id = plan_id
        self.state = state
