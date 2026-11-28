
from typer.cli import state

from src.customer.application.dto.customer_create_request import CustomerCreateRequest
from src.customer.application.dto.customer_plan_response import CustomerPlanResponse
from src.customer.application.dto.customer_response import CustomerResponse
from src.customer.application.dto.subscribe_customer_plan_request import SubscribeCustomerPlanRequest
from src.customer.application.errorHandler.PlanNotFoundException import PlanNotFoundException
from src.customer.application.mapper import CustomerMapper, CustomerPlanMapper
from src.customer.application.ports.output.plan_lookup_output_port import PlanLookupOutputPort
from src.customer.domain.repositories.customer_repository import CustomerRepository
from src.customer.domain.model.CustomerPlan import CustomerPlanStatus
from src.shared.utils.criterial.CompareOperator import CompareOperator
from src.shared.utils.criterial.Filter import Filter


class CustomerUseCases:
    def __init__(self, customer_input_port, customer_repository: CustomerRepository, plan_lookup_port: PlanLookupOutputPort):
        self.customer_input_port = customer_input_port
        self.customer_repository = customer_repository
        self.plan_lookup_port = plan_lookup_port

    def create_customer(self, customer_data: CustomerCreateRequest) -> CustomerResponse:
        customer = CustomerMapper.request_to_domain(customer_data)
        
        customer_updated = self.customer_repository.save(customer)

        return CustomerMapper.domain_to_response(customer_updated)

    def get_customers(self) -> list[CustomerResponse]:
        customers = self.customer_repository.get()
        return [CustomerMapper.domain_to_response(customer) for customer in customers]

    def get_customer_by_id(self, id: str) -> CustomerResponse | None:
        customer = self.customer_repository.get_by_id(id)

        if not customer:
            raise ValueError(f"Customer with id {id} not found")
        return CustomerMapper.domain_to_response(customer)

    def delete_customer(self, id: str) -> None:
        customer = self.customer_repository.get_by_id(id)
        if not customer:
            raise ValueError(f"Customer with id {id} not found")
        self.customer_repository.delete(id)

    def update_customer(self, id: str, customer_data: CustomerCreateRequest) -> CustomerResponse:
        customer = CustomerMapper.request_to_domain(customer_data)
        customer.id = id
        customer_updated = self.customer_repository.update(customer)

        if not customer_updated:
            raise ValueError(f"Customer with id {id} not found")
        return CustomerMapper.domain_to_response(customer_updated)

    def subscribe_customer_to_plan(self, subscription_data: SubscribeCustomerPlanRequest) -> CustomerPlanResponse:
        customer = self.customer_repository.get_by_id(subscription_data.customer_id)
        if not customer:
            raise ValueError(f"Customer with id {subscription_data.customer_id} not found")
        plan_exists = self.plan_lookup_port.plan_exists(subscription_data.plan_id)
        if not plan_exists:
            raise PlanNotFoundException(subscription_data.plan_id)
        return CustomerPlanMapper.customer_plan_to_response(
            self.customer_repository.subscribe_to_plan(subscription_data.customer_id, subscription_data.plan_id)
        )

    def get_plans_by_customer_id(self, customer_id: str) -> list[CustomerPlanResponse]:

        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")
        
        customer_plans = self.customer_repository.get_plans_by_customer_id(customer_id)

        return [CustomerPlanMapper.customer_plan_to_response(cp) for cp in customer_plans]

    def get_plans_by_customer_id_and_state(self, customer_id: str, status: CustomerPlanStatus) -> list[CustomerPlanResponse]:
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")
        if status.name not in CustomerPlanStatus.__members__:
            raise ValueError(f"Invalid plan state: {status}")

        customer_plans = self.customer_repository.get_plans_by_filter([
            Filter(field="customer_id", operator=CompareOperator.EQUAL, value=customer_id),
            Filter(field="state", operator=CompareOperator.EQUAL, value=status.name.upper())
        ])

        return [CustomerPlanMapper.customer_plan_to_response(cp) for cp in customer_plans]

    def subscribe_customer_plan_update(self, customer_id: str, plan_id: str, subscription_update: CustomerPlanStatus) -> CustomerPlanResponse:
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found")
        plan_exists = self.plan_lookup_port.plan_exists(plan_id)
        if not plan_exists:
            raise PlanNotFoundException(plan_id)
        if subscription_update.name not in CustomerPlanStatus.__members__:
            raise ValueError(f"Invalid plan state: {subscription_update}")
        
        return CustomerPlanMapper.customer_plan_to_response(
            self.customer_repository.update_subscription_state(
                customer_id,
                plan_id,
                subscription_update
            )
        )
