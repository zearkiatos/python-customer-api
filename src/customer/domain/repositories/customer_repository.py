from typing import Protocol

from src.shared.utils.criterial.Filter import Filter
from ...domain.model.Customer import Customer
from ...domain.model.CustomerPlan import CustomerPlan, CustomerPlanStatus

class CustomerRepository(Protocol):
    def get(self) -> list[Customer]:
        ...

    def get_by_id(self, id: str) -> Customer | None:
        ...

    def save(self, customer: Customer) -> Customer:
        ...

    def delete(self, id: str) -> None:
        ...

    def update(self, customer: Customer) -> Customer | None:
        ...

    def subscribe_to_plan(self, customer_id: str, plan_id: str) -> CustomerPlan:
        ...

    def get_plans_by_customer_id(self, customer_id: str) -> list[CustomerPlan]:
        ...

    def get_plans_by_filter(self, filters: list[Filter]) -> list[CustomerPlan]:
        ...

    def update_subscription_state(self, customer_id: str, plan_id: str, state: CustomerPlanStatus) -> CustomerPlan:
        ...