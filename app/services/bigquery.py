# app/services/bigquery.py
from google.cloud import bigquery
from app.config import FULL_TABLE
from app.models.customer import Customer

client = bigquery.Client()   # Uses ambient credentials (SA key or Workload Identity)

def get_all_customers() -> list[Customer]:
    query = f"""
        SELECT customer_id, customer_name, total_sales
        FROM   {FULL_TABLE}
        ORDER  BY total_sales DESC
    """
    rows = client.query(query).result()
    return [
        Customer(
            customer_id=row.customer_id,
            customer_name=row.customer_name,
            total_sales=float(row.total_sales),
        )
        for row in rows
    ]

def get_customer_by_id(customer_id: str) -> Customer | None:
    query = f"""
        SELECT customer_id, customer_name, total_sales
        FROM   {FULL_TABLE}
        WHERE  customer_id = @customer_id
        LIMIT  1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
        ]
    )
    rows = list(client.query(query, job_config=job_config).result())
    if not rows:
        return None
    row = rows[0]
    return Customer(
        customer_id=row.customer_id,
        customer_name=row.customer_name,
        total_sales=float(row.total_sales),
    )