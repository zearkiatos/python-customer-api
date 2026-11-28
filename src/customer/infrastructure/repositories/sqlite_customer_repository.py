from uuid import uuid4
from sqlalchemy import text
from sqlmodel import Relationship, SQLModel, Session, Field, select
from src.customer.domain.model.CustomerPlan import CustomerPlan, CustomerPlanStatus
from src.customer.domain.model.Customer import Customer
from src.customer.domain.repositories.customer_repository import CustomerRepository
from src.shared.utils.criterial.CompareOperator import CompareOperator
from src.shared.utils.criterial.Filter import Filter

class CustomerPlanTable(SQLModel, table=True):
    __tablename__ = "customer_plans"

    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    customer_id: str = Field(foreign_key="customers.id")
    plan_id: str = Field(foreign_key="plans.id")
    state: str = Field(
        default=CustomerPlanStatus.ACTIVE.name,
        sa_column_kwargs={"server_default": text("'ACTIVE'")},
    )

class CustomerTable(SQLModel, table=True):
    __tablename__ = "customers"

    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    name: str = Field(default=None)
    email: str = Field(default=None)
    description: str = Field(default=None)
    age: int = Field(default=0)
    transactions: list["TransactionTable"] = Relationship(back_populates="customer")
    plans: list["PlanTable"] = Relationship(back_populates="customers", link_model=CustomerPlanTable)

class SqliteCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _to_table(customer: Customer) -> CustomerTable:
        return CustomerTable(
            name=customer.name,
            email=customer.email,
            description=customer.description,
            age=customer.age
        )
        
    @staticmethod
    def _to_domain(table: CustomerTable) -> Customer:
        return Customer(
            id=table.id,
            name=table.name,
            email=table.email,
            description=table.description,
            age=table.age
        )

    @staticmethod
    def _to_plan_domain(table: CustomerPlanTable) -> CustomerPlan:
        return CustomerPlan(
            id=table.id,
            customer_id=table.customer_id,
            plan_id=table.plan_id,
            state=CustomerPlanStatus[table.state.upper()]
        )

    @staticmethod
    def _to_plan_table(customer_plan: CustomerPlan) -> CustomerPlanTable:
        return CustomerPlanTable(
            plan_id=customer_plan.plan_id,
            state=customer_plan.state.name,
            customer_id=customer_plan.customer_id,
        )

    def get(self) -> list[Customer]:
        customers = self.session.exec(select(CustomerTable)).all()
        return [self._to_domain(customer) for customer in customers]

    def get_by_id(self, id: str) -> Customer | None:
        customer = self.session.get(CustomerTable, id)
        if customer is None:
            return None
        return self._to_domain(customer)

    def save(self, customer: Customer) -> Customer:
        customer_table = self._to_table(customer)
        self.session.add(customer_table)
        self.session.commit()

        self.session.refresh(customer_table)
        return self._to_domain(customer_table)

    def delete(self, id: str) -> None:
        customer = self.session.get(CustomerTable, id)
        if customer:
            self.session.delete(customer)
            self.session.commit()

    def update(self, customer: Customer) -> Customer | None:
        customer_table = self.session.get(CustomerTable, customer.id)
        if not customer_table:
            return None

        customer_table.name = customer.name
        customer_table.email = customer.email
        customer_table.description = customer.description
        customer_table.age = customer.age

        self.session.add(customer_table)
        self.session.commit()
        self.session.refresh(customer_table)
        return self._to_domain(customer_table)

    def subscribe_to_plan(self, customer_id: str, plan_id: str) -> CustomerPlan:
        subscription = CustomerPlanTable(
            customer_id=customer_id,
            plan_id=plan_id
        )
        self.session.add(subscription)
        self.session.commit()
        self.session.refresh(subscription)

        return self._to_plan_domain(subscription)

    def get_plans_by_customer_id(self, customer_id: str) -> list[CustomerPlan]:
        plans = self.session.exec(select(CustomerPlanTable).where(CustomerPlanTable.customer_id == customer_id)).all()
        return [self._to_plan_domain(plan) for plan in plans]

    def get_plans_by_filter(self, filters: list[Filter]) -> list[CustomerPlan]:
        query = select(CustomerPlanTable)
        for filter in filters:
            if filter.operator == CompareOperator.EQUAL:
                query = query.where(getattr(CustomerPlanTable, filter.field) == filter.value)
            elif filter.operator == CompareOperator.NOT_EQUAL:
                query = query.where(getattr(CustomerPlanTable, filter.field) != filter.value)
        plans = self.session.exec(query).all()
        return [self._to_plan_domain(plan) for plan in plans]

    def update_subscription_state(self, customer_id: str, plan_id: str, state: CustomerPlanStatus) -> CustomerPlan:
        subscription = self.session.exec(
            select(CustomerPlanTable).where(
                CustomerPlanTable.customer_id == customer_id,
                CustomerPlanTable.plan_id == plan_id
            )
        ).first()
        if not subscription:
            raise ValueError(f"Customer plan with customer_id {customer_id} and plan_id {plan_id} not found")

        subscription.state = state
        self.session.add(subscription)
        self.session.commit()
        self.session.refresh(subscription)
        return self._to_plan_domain(subscription)
