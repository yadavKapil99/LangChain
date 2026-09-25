"""Shared configuration; importing this module makes no API requests."""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def require_key(*names):
    load_dotenv(PROJECT_ROOT / ".env")
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    raise ValueError(f"Set {' or '.join(names)} in {PROJECT_ROOT / '.env'}")


def chat_model(temperature=0, max_tokens=1000):
    key = require_key("OPENROUTER_API_KEY", "OPEN_ROUTER_API_KEY")
    return ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL", "qwen/qwen3-8b"),
        api_key=key,
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        temperature=temperature,
        max_tokens=max_tokens,
    )


def huggingface_model():
    key = require_key("HUGGINGFACEHUB_API_TOKEN", "HF_TOKEN")
    return ChatOpenAI(
        model=os.getenv("HUGGINGFACE_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        api_key=key,
        base_url="https://router.huggingface.co/v1",
        temperature=0.7,
        max_tokens=50,
    )


def embedding_model(dimensions=32):
    key = require_key("OPENROUTER_API_KEY", "OPEN_ROUTER_API_KEY")
    return OpenAIEmbeddings(
        model=os.getenv("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-large"),
        dimensions=dimensions,
        api_key=key,
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        check_embedding_ctx_length=False,
    )
