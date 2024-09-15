from fastapi import FastAPI
from app.api.endpoints import invoice

app = FastAPI()

app.include_router(invoice.router, prefix="/invoices", tags=["invoices"])
