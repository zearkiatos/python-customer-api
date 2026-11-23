class PlanNotFoundException(Exception):
    def __init__(self, plan_id: str):
        self.plan_id = plan_id
        super().__init__(f"Plan with id {plan_id} not found")