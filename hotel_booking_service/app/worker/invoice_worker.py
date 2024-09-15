import time
import json
from kafka import KafkaConsumer, KafkaProducer
from app.db.session import SessionLocal
from app.models.invoice import Invoice
from app.services.invoice_service import create_invoice_pdf, send_email

consumer = KafkaConsumer('InvoiceGenerationQueue', bootstrap_servers=['localhost:9092'])
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

def process_invoice_generation():
    while True:
        for message in consumer:
            invoice_data = json.loads(message.value.decode('utf-8'))
            invoice_id = invoice_data["invoice_id"]

            db = SessionLocal()
            invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()

            if invoice:
                try:
                    pdf_url = create_invoice_pdf(invoice)
                    send_email(invoice, pdf_url)
                    invoice.status = 'SENT'
                except Exception as e:
                    invoice.status = 'SEND_FAILURE'
                db.commit()
            db.close()
        time.sleep(1)

if __name__ == "__main__":
    process_invoice_generation()
