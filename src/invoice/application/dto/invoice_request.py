from pydantic import BaseModel
from uuid import UUID

class InvoiceRequest(BaseModel):
    name: str
    customer_id: UUID
    transactions: list[UUID]