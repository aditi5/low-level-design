from sqlalchemy import Column, Integer, String, Enum, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.db.base import Base


class InvoiceStatus(str, enum.Enum):
    CREATED = "CREATED"
    GENERATED = "GENERATED"
    SENT = "SENT"
    SEND_FAILURE = "SEND_FAILURE"


class Invoice(Base):
    __tablename__ = "invoice"

    customer_id = Column(Integer, nullable=False)
    invoice_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    invoice_period_start = Column(BigInteger, nullable=False)
    invoice_period_end = Column(BigInteger, nullable=False)
    hotel_id = Column(Integer, nullable=False)
    booking_id = Column(Integer, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.CREATED, nullable=False)
