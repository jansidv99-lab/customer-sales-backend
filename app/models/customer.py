# app/models/customer.py
from pydantic import BaseModel

class Customer(BaseModel):
    customer_id:   str
    customer_name: str
    total_sales:   float

class CustomerListResponse(BaseModel):
    count:     int
    customers: list[Customer]