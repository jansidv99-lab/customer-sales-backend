# app/routers/chat.py
from fastapi        import APIRouter
from pydantic       import BaseModel
from app.services.bigquery  import get_all_customers
from app.services.llm_service import generate_answer

router = APIRouter(prefix="/chat", tags=["chat"])

# ── Request / response models ─────────────────────────────
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    question: str
    answer:   str

# ── Helper — build context string from BigQuery data ─────
def build_context() -> str:
    """
    Fetches live customer records and formats them as plain text
    so the LLM can reason about the data.
    """
    customers = get_all_customers()
    lines = ["Here is the current customer sales data:\n"]
    for c in customers:
        lines.append(
            f"- {c.customer_name} (ID: {c.customer_id}): "
            f"total sales = ${c.total_sales:,.2f}"
        )
    return "\n".join(lines)

# ── POST /chat ────────────────────────────────────────────
@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    context = build_context()          # fetch fresh data from BigQuery
    answer  = generate_answer(         # run LLM inference
        context=context,
        question=request.question,
    )
    return ChatResponse(
        question=request.question,
        answer=answer,
    )