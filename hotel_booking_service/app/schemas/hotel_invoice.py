from pydantic import BaseModel
from uuid import UUID
from datetime import date


class HotelInvoiceBase(BaseModel):
    hotel_id: int
    hotel_name: str
    invoice_validity_start: int
    invoice_validity_end: int
    reference_date: date


class HotelInvoiceCreate(HotelInvoiceBase):
    pass


class HotelInvoice(HotelInvoiceBase):
    hotel_invoice_id: UUID
    status: str

    class Config:
        orm_mode = True
