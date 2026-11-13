class Customer:
    def __init__(self, name: str, description: str, email: str, age: int, id: str = None):
        self.id = id
        self.name = name
        self.description = description
        self.email = email
        self.age = age