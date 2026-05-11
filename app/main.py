# app/main.py
from fastapi import FastAPI
from app.routers import customers, chat
from app.services.llm_service import load_model

app = FastAPI(
    title="Customer Sales API",
    version="2.0.0",
    description="Customer sales data + AI chatbot powered by TinyLlama",
)

@app.on_event("startup")
async def startup_event():
    # Load the LLM in the background when FastAPI starts
    # Pods will pass readiness probe before model is loaded
    # — model loads async so health check still passes
    import threading
    threading.Thread(target=load_model, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "ok", "service": "customer-sales-backend"}

app.include_router(customers.router)
app.include_router(chat.router)      # ← new