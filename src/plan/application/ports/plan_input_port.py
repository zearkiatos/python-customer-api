from typing import Protocol
from src.plan.application.dto.plan_request import PlanRequest
from src.plan.application.dto.plan_response import PlanResponse

class PlanInputPort(Protocol):
    def create_plan(self, request: PlanRequest) -> PlanResponse:
        ...

    def get_plans(self) -> list[PlanResponse]:
        ...

    def get_plan_by_id(self, id: str) -> PlanResponse | None:
        ...

    def delete_plan(self, id: str) -> None:
        ...

    def update_plan(self, id: str, plan_data: PlanRequest) -> PlanResponse:
        ...