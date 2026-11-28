from src.customer.application.ports.output.plan_lookup_output_port import PlanLookupOutputPort
from src.plan.application.ports.plan_input_port import PlanInputPort

class PlanLookupAdapter(PlanLookupOutputPort):
    def __init__(self, plan_port: PlanInputPort):
        self.plan_port = plan_port

    def plan_exists(self, plan_id: str) -> bool:
        try:
            return self.plan_port.get_plan_by_id(plan_id) is not None
        except ValueError:
            return False # Replace with actual implementation