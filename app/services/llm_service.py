# app/services/llm_service.py
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# Module-level variable — model loads once on startup, reused for all requests
_llm_pipeline = None

def load_model():
    """
    Called once at FastAPI startup.
    TinyLlama-1.1B runs comfortably on CPU with 2GB RAM.
    """
    global _llm_pipeline
    if _llm_pipeline is not None:
        return

    logger.info("Loading TinyLlama-1.1B model — this takes ~30s on first start...")
    _llm_pipeline = pipeline(
        task="text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device=-1,            # -1 = CPU (no GPU required)
        torch_dtype="auto",
    )
    logger.info("Model loaded and ready.")

def generate_answer(context: str, question: str) -> str:
    """
    Builds a prompt with customer data context and generates an answer.
    context  — customer records injected as plain text
    question — the user's question from the chat UI
    """
    if _llm_pipeline is None:
        return "Model is not loaded yet. Please try again in a moment."

    # TinyLlama chat format
    prompt = f"""<|system|>
You are a helpful sales assistant. Answer questions using ONLY the customer data provided below.
Keep answers short, factual, and friendly.

Customer data:
{context}
</s>
<|user|>
{question}
</s>
<|assistant|>
"""

    result = _llm_pipeline(
        prompt,
        max_new_tokens=150,     # short answers — keeps it fast on CPU
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=_llm_pipeline.tokenizer.eos_token_id,
    )

    # Strip the prompt from the generated text — return only the answer
    generated = result[0]["generated_text"]
    answer    = generated.split("<|assistant|>")[-1].strip()
    return answer