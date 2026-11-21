from pydantic import BaseModel

class TransactionRequest(BaseModel):
    amount: int
    description: str
    customer_id: str