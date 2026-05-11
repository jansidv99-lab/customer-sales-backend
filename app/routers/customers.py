# app/routers/customers.py
from fastapi import APIRouter, HTTPException
from app.services.bigquery import get_all_customers, get_customer_by_id
from app.models.customer import Customer, CustomerListResponse

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("", response_model=CustomerListResponse)
def list_customers():
    customers = get_all_customers()
    return CustomerListResponse(count=len(customers), customers=customers)

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customer