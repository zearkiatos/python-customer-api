class Invoice:
    def __init__(self, id: str, name: str, customer_id: str, transactions: list[str] ):
        self.id = id
        self.name = name
        self.customer_id = customer_id
        self.transactions = transactions