from uuid import uuid4
from src.customer.application.dto.customer_plan_response import CustomerPlanResponse
from src.customer.domain.model.CustomerPlan import CustomerPlan
from src.customer.domain.model.Customer import Customer
from src.customer.domain.repositories.customer_repository import CustomerRepository

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers: list[Customer] = []
        self.customer_plans: list[CustomerPlan] = []

    def get(self) -> list[Customer]:
        return self.customers

    def get_by_id(self, id: str) -> Customer | None:
        for customer in self.customers:
            if customer.id == id:
                return customer
        return None

    def save(self, customer: Customer) -> Customer:
        customer.id = str(uuid4())
            
        self.customers.append(customer)
        return customer

    def delete(self, id: str) -> None:
        self.customers.remove(next(customer for customer in self.customers if customer.id == id))

    def update(self, customer: Customer) -> Customer | None:
        for i, existing_customer in enumerate(self.customers):
            if existing_customer.id == customer.id:
                self.customers[i] = customer
                return customer
        return None

    def subscribe_to_plan(self, customer_id: str, plan_id: str) -> CustomerPlan:
        customer_plan = CustomerPlan(id=str(uuid4()), customer_id=customer_id, plan_id=plan_id)
        self.customer_plans.append(customer_plan)

        return customer_plan

    def get_plans_by_customer_id(self, customer_id: str) -> list[CustomerPlan]:
        return [cp for cp in self.customer_plans if cp.customer_id == customer_id]
