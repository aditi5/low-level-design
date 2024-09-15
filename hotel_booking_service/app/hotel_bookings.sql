CREATE TABLE customer_invoice (
    customer_id INTEGER,
    invoice_id TEXT PRIMARY KEY,
    invoice_period_start INTEGER,
    invoice_period_end INTEGER,
    hotel_id INTEGER,
    booking_id INTEGER,
    status TEXT CHECK(status IN ('CREATED', 'GENERATED', 'SENT', 'SEND_FAILURE'))
);

CREATE TABLE hotel_invoice (
    hotel_id INTEGER,
    hotel_name TEXT,
    hotel_invoice_id TEXT PRIMARY KEY,
    invoice_validity_start INTEGER,
    invoice_validity_end INTEGER,
    reference_date TEXT,
    status TEXT CHECK(status IN ('CREATED', 'GENERATED', 'SENT', 'SEND_FAILURE'))
);
