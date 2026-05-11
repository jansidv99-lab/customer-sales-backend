# app/config.py
import os

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "waybackhome-mto0ibjp7iru8bkisr")
DATASET    = os.getenv("BQ_DATASET",     "customer_sales_db")
TABLE      = os.getenv("BQ_TABLE",       "customers")

FULL_TABLE = f"`{PROJECT_ID}.{DATASET}.{TABLE}`"
#test