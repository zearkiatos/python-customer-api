from typing import Protocol

class PlanLookupOutputPort(Protocol):
    def plan_exists(self, plan_id: str) -> bool:
        ...