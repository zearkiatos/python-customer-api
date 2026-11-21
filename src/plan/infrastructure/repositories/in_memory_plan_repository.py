from uuid import uuid4
from src.plan.domain.model.Plan import Plan

from ...domain.repositories.plan_repository import PlanRepository

class InMemoryPlanRepository(PlanRepository):
    def __init__(self):
            self.plans: list[Plan] = []

    def get(self) -> list[Plan]:
        return self.plans

    def get_by_id(self, id: str) -> Plan | None:
        for plan in self.plans:
            if plan.id == id:
                return plan
        return None

    def save(self, plan: Plan) -> Plan:
        plan.id = str(uuid4())

        self.plans.append(plan)
        return plan

    def delete(self, id: str) -> None:
        self.plans.remove(next(plan for plan in self.plans if plan.id == id))

    def update(self, plan: Plan) -> Plan | None:
        for i, p in enumerate(self.plans):
            if p.id == plan.id:
                self.plans[i] = plan
                return plan
        return None