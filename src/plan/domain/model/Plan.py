class Plan:
    def __init__(self, name: str, price: float, description: str, id: str = None):
            self.id = id
            self.name = name
            self.price = price
            self.description = description