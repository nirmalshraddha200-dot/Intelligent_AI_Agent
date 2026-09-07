import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:

    # =========================================================
    # GEMINI EMBEDDINGS
    # =========================================================
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


    # =========================================================
    # QDRANT VECTOR DATABASE
    # =========================================================
    QDRANT_URL = os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = "enterprise_rag"


    # =========================================================
    # GROQ REASONING ENGINE
    # =========================================================
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Kept for compatibility with existing code
    GROQ_MODEL = "llama-3.3-70b-versatile"

    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")


    # =========================================================
    # PORTKEY LLM GATEWAY
    # =========================================================
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")

    # Saved Portkey Config slug
    # Example: pc-xxxxxxxxxxxxxxxx
    PORTKEY_CONFIG = os.getenv("PORTKEY_CONFIG")

    # These are kept for compatibility with existing gateway code
    GROQ_SLUG = "rag"
    GROQ_SLUG_2 = "brag"


    # =========================================================
    # FASTAPI BACKEND
    # =========================================================
    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )


    # =========================================================
    # LANGSMITH OBSERVABILITY
    # =========================================================
    LANGSMITH_TRACING = os.getenv(
        "LANGSMITH_TRACING",
        "false"
    )

    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

    LANGSMITH_PROJECT = os.getenv(
        "LANGSMITH_PROJECT",
        "Intelligent_AI_Agent"
    )

    LANGSMITH_ENDPOINT = os.getenv(
        "LANGSMITH_ENDPOINT",
        "https://api.smith.langchain.com"
    )


# =============================================================
# APPLY LANGCHAIN ENVIRONMENT VARIABLES
# =============================================================

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv(
    "LANGSMITH_TRACING",
    "false"
)

os.environ["LANGCHAIN_API_KEY"] = os.getenv(
    "LANGSMITH_API_KEY",
    ""
)

os.environ["LANGCHAIN_PROJECT"] = os.getenv(
    "LANGSMITH_PROJECT",
    "Intelligent_AI_Agent"
)

os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
    "LANGSMITH_ENDPOINT",
    "https://api.smith.langchain.com"
)


# =============================================================
# SETTINGS INSTANCE
# =============================================================

settings = Settings()