from pydantic import BaseModel

class TransactionRequest(BaseModel):
    amount: int
    description: str