from typing import Protocol
from ...domain.model.Plan import Plan

class PlanRepository(Protocol):
    def get(self) -> list[Plan]:
        ...

    def get_by_id(self, id: str) -> Plan | None:
        ...

    def save(self, plan: Plan) -> Plan:
        ...

    def delete(self, id: str) -> None:
        ...

    def update(self, plan: Plan) -> Plan | None:
        ...