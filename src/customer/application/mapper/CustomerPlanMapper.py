from src.customer.application.dto.customer_plan_response import CustomerPlanResponse
from src.customer.domain.model.CustomerPlan import CustomerPlan


def customer_plan_to_response(customer_plan: CustomerPlan) -> CustomerPlanResponse:
    return CustomerPlanResponse(
        id = customer_plan.id,
        customer_id=customer_plan.customer_id,
        plan_id=customer_plan.plan_id
    )

def customer_plan_request_to_domain(customer_id: str, plan_id: str) -> CustomerPlan:
    return CustomerPlan(
        customer_id=customer_id,
        plan_id=plan_id
    )