import logfire
from portkey_ai import Portkey, createHeaders, PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI

from app.config import settings


# Portkey saved configuration
portkey_client = Portkey(
    api_key=settings.PORTKEY_API_KEY,
    config=settings.PORTKEY_CONFIG
)


def get_langchain_llm(feature: str = "rag") -> ChatOpenAI:
    """
    Returns a Portkey-backed LangChain ChatOpenAI model.

    Portkey routes the request to the saved configuration
    specified by PORTKEY_CONFIG.
    """

    return ChatOpenAI(
        api_key=settings.PORTKEY_API_KEY,
        base_url=PORTKEY_GATEWAY_URL,
        model="openai/gpt-oss-20b",
        temperature=0,
        default_headers=createHeaders(
            api_key=settings.PORTKEY_API_KEY,
            config=settings.PORTKEY_CONFIG,
            metadata={
                "feature": feature,
                "_user": "rag-system",
                "environment": "production"
            }
        )
    )


def extract_cache_status(response) -> str:
    """
    Pull x-portkey-cache-status from the Portkey native client response.
    """

    for attr in ("_raw_response", "_response", "_http_response"):
        raw = getattr(response, attr, None)

        if raw is not None:
            status = getattr(raw, "headers", {}).get(
                "x-portkey-cache-status",
                ""
            )

            if status:
                return status.upper()

    return "MISS"