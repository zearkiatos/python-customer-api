class Transaction:
    def __init__(self, id: str, amount: int, description: str, customer_id: str):
        self.id = id
        self.amount = amount
        self.description = description
        self.customer_id = customer_id