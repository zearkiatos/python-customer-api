class Filter:
    def __init__(self, field: str, operator: str, value: str):
        self.field = field
        self.operator = operator
        self.value = value

    def to_dict(self):
        return {
            "field": self.field,
            "operator": self.operator,
            "value": self.value
        }

    def serialization(self):
        return f"{self.field} {self.operator} {self.value}"