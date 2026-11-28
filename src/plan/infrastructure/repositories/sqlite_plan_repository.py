

from uuid import uuid4

from sqlmodel import Field,Relationship, SQLModel, Session

from src.customer.infrastructure.repositories.sqlite_customer_repository import CustomerPlanTable
from src.plan.domain.model.Plan import Plan
from src.plan.domain.repositories.plan_repository import PlanRepository


class PlanTable(SQLModel, table=True):
    __tablename__ = "plans"

    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    name: str = Field(default=None)
    description: str = Field(default=None)
    price: float = Field(default=0)
    customers: list["CustomerTable"] = Relationship(back_populates="plans", link_model=CustomerPlanTable)

class SqlitePlanRepository(PlanRepository):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _to_table(plan: Plan) -> PlanTable:
        return PlanTable(
            id=plan.id,
            name=plan.name,
            description=plan.description,
            price=plan.price
        )

    @staticmethod
    def _to_domain(table: PlanTable) -> Plan:
        return Plan(
            id=table.id,
            name=table.name,
            description=table.description,
            price=table.price
        )

    def get(self) -> list[Plan]:
        plans = self.session.query(PlanTable).all()
        return [self._to_domain(plan) for plan in plans]

    def get_by_id(self, id: str) -> Plan | None:
        plan = self.session.get(PlanTable, id)
        if plan is None:

            return None
        return self._to_domain(plan)

    def save(self, plan: Plan) -> Plan:
        plan_table = self._to_table(plan)
        self.session.add(plan_table)
        self.session.commit()
        self.session.refresh(plan_table)
        return self._to_domain(plan_table)

    def delete(self, id: str) -> None:
        plan = self.session.get(PlanTable, id)
        if plan is not None:
            self.session.delete(plan)
            self.session.commit()

    def update(self, plan: Plan) -> Plan | None:
        plan_table = self.session.get(PlanTable, plan.id)
        if plan_table is None:
            return None
        plan_table.name = plan.name
        plan_table.description = plan.description
        plan_table.price = plan.price
        self.session.commit()
        self.session.refresh(plan_table)
        return self._to_domain(plan_table)
