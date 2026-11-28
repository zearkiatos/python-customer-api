
from typing import Protocol
from src.customer.application.dto.customer_plan_response import CustomerPlanResponse
from src.customer.application.dto.customer_request import CustomerRequest
from src.customer.application.dto.customer_response import CustomerResponse
from src.customer.application.dto.subscribe_customer_plan_request import SubscribeCustomerPlanRequest
from src.customer.application.dto.subscribe_customer_plan_update import SubscribeCustomerPlanUpdate

class CustomerInputPort(Protocol):
    def create_customer(self, customer_data: CustomerRequest) -> CustomerResponse:
        ...

    def get_customers(self) -> list[CustomerResponse]:
        ...

    def get_customer_by_id(self, id: str) -> CustomerResponse | None:
        ...

    def delete_customer(self, id: str) -> None:
        ...

    def update_customer(self, id: str, customer_data: CustomerRequest) -> CustomerResponse:
        ...

    def subscribe_customer_to_plan(self, subscription_data: SubscribeCustomerPlanRequest) -> CustomerPlanResponse:
        ...

    def get_plans_by_customer_id(self, customer_id: str) -> list[CustomerPlanResponse]:
        ...

    def subscribe_customer_plan_update(self, customer_id: str, plan_id: str, subscription_update: SubscribeCustomerPlanUpdate) -> CustomerPlanResponse:
        ...