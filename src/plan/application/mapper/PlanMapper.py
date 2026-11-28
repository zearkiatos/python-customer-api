from src.plan.application.dto.plan_request import PlanRequest
from src.plan.application.dto.plan_response import PlanResponse
from src.plan.domain.model.Plan import Plan

def request_to_domain(request: PlanRequest) -> Plan:
    return Plan(
        name=request.name,
        description=request.description,
        price=request.price
    )

def domain_to_response(domain: Plan)-> PlanResponse:
    return PlanResponse(
        id=domain.id,
        name=domain.name,
        description=domain.description,
        price=domain.price
    )