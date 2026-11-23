from src.plan.application.dto.plan_request import PlanRequest
from src.plan.application.dto.plan_response import PlanResponse
from src.plan.application.mapper import PlanMapper
from src.plan.application.ports.plan_input_port import PlanInputPort
from src.plan.domain.model.Plan import Plan
from src.plan.domain.repositories.plan_repository import PlanRepository


class PlanUseCases(PlanInputPort):
    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository
    
    def create_plan(self, plan_data: PlanRequest) -> PlanResponse:
        plan = PlanMapper.request_to_domain(plan_data)
        plan_updated = self.plan_repository.save(plan)
        return PlanMapper.domain_to_response(plan_updated)

    def get_plans(self) -> list[PlanResponse]:
        plans = self.plan_repository.get()
        return [PlanMapper.domain_to_response(plan) for plan in plans]

    def get_plan_by_id(self, id: str) -> PlanResponse | None:
        plan = self.plan_repository.get_by_id(id)
        if not plan:
            raise ValueError(f"Plan with id {id} not found")
        return PlanMapper.domain_to_response(plan)

    def delete_plan(self, id: str) -> None:
        ...

    def update_plan(self, id: str, plan_data: PlanRequest) -> PlanResponse:
        ...