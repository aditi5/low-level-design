from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.invoice import Invoice, InvoiceCreate
from app.models.invoice import Invoice as InvoiceModel
from app.api.deps import get_db
from app.services.invoice_service import create_invoice
from uuid import uuid4

router = APIRouter()


@router.post("/", response_model=Invoice)
def create_new_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    invoice_id = uuid4()
    invoice_data = InvoiceModel(
        customer_id=invoice.customer_id,
        invoice_id=invoice_id,
        invoice_period_start=invoice.invoice_period_start,
        invoice_period_end=invoice.invoice_period_end,
        hotel_id=invoice.hotel_id,
        booking_id=invoice.booking_id,
        status='CREATED'
    )
    return create_invoice(db=db, invoice=invoice_data)
