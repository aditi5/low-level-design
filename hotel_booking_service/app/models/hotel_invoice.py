from sqlalchemy import Column, Integer, String, Enum, BigInteger, Date
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class HotelInvoiceStatus(str, enum.Enum):
    CREATED = "CREATED"
    GENERATED = "GENERATED"
    SENT = "SENT"
    SEND_FAILURE = "SEND_FAILURE"


class HotelInvoice(Base):
    __tablename__ = "hotel_invoice"

    hotel_id = Column(Integer, nullable=False)
    hotel_name = Column(String, nullable=False)
    hotel_invoice_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    invoice_validity_start = Column(BigInteger, nullable=False)
    invoice_validity_end = Column(BigInteger, nullable=False)
    reference_date = Column(Date, nullable=False)
    status = Column(Enum(HotelInvoiceStatus), default=HotelInvoiceStatus.CREATED, nullable=False)
