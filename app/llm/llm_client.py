# app/llm/llm_client.py
from langchain_openai import ChatOpenAI
from app.config import settings


def get_llm(
    model: str = "nvidia/nemotron-3-ultra",
    temperature: float = 0.2,
):
    """
    Get an LLM instance via OpenRouter.

    Args:
        model: OpenRouter model ID.
        temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)

    Returns:
        ChatOpenAI instance configured for OpenRouter

    Raises:
        ValueError: If OPENROUTER_API_KEY is not set.
    """
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")

    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,  # type: ignore[arg-type]
        model=model,
        temperature=temperature,
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Knowledge Assistant",
        },
    )