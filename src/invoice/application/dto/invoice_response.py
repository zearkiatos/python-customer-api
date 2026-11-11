from uuid import UUID
from pydantic import BaseModel

class InvoiceResponse(BaseModel):
    id: str
    name: str
    customer_id: str
    transactions: list[str]
    total: int