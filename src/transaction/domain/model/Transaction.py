class Transaction:
    def __init__(self, id: str, amount: int, description: str):
        self.id = id
        self.amount = amount
        self.description = description