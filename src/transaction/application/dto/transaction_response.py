from pydantic import BaseModel

class TransactionResponse(BaseModel):
    id: str
    amount: str
    description: str