from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class InvoiceBase(BaseModel):
    customer_id: int
    invoice_period_start: int
    invoice_period_end: int
    hotel_id: int
    booking_id: int


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    invoice_id: UUID
    status: str

    class Config:
        orm_mode = True
