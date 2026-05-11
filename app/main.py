# app/main.py
from fastapi import FastAPI
from app.routers import customers

app = FastAPI(
    title="Customer Sales API",
    version="1.0.0",
    description="Serves customer sales data from BigQuery",
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "customer-sales-backend"}

app.include_router(customers.router)