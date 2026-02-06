# i am here only focus on gemini , cohere and openai cuz they provide both text completion and embeddings

## but note that first focus is only on openai apis, their are some function that openai supports but gemini or cohere does't support and i dont want to waste time creating wrappr
## so if other models does't work then i am just lazy lol

from dotenv import load_dotenv  ## always import this on top to make to ensure all enviroment  variables are loaded
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

# module-level path constants (safe for pydantic v2)
SQLITE_DB_PATH = BASE_DIR / "app/db/smartshop_assistant.db"
VECTOR_DB_PATH = BASE_DIR / "app/vector_db"
VECTOR_COLLECTION = "products"


# ConfigDict here
class AppConfig(BaseSettings):
    """
    Centralized configuration management using Pydantic.
    Automatically reads environment variables, validates types,
    and applies default values if missing.
    """

    # openai  -> llm
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-5-nano-2025-08-07"
    OPENAI_MODEL2: str = "gpt-5-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_EMBEDDING_DIM: int = 1536

    # gemini  -> llm
    GEMINI_API_KEY: str
    GEMINAI_API_KEY2: str
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"
    GEMINI_MODEL2: str = "gemini-2.5-flash"

    # cohere -> llm
    COHERE_API: str
    COHERE_MODEL: str = "command-a-03-2025"

    # langshmit -> logging
    LANGSHMIT_API_KEY: str

    FB_PAGE_ID: str
    FB_PAGE_ACCESS_TOKEN: str
    FB_GRAPH_VERSION: str

    # expose paths through config without making them pydantic fields
    @property
    def BASE_DIR(self) -> Path:
        return BASE_DIR

    @property
    def SQLITE_DB_PATH(self) -> Path:
        return SQLITE_DB_PATH

    @property
    def VECTOR_DB_PATH(self) -> Path:
        return VECTOR_DB_PATH

    @property
    def VECTOR_COLLECTION(self) -> str:
        return VECTOR_COLLECTION

    model_config = ConfigDict(
        # Automatically load environment variables from a .env file
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  ## pydantic will throw error if we have mention other Variable  other then mention here ,
    )


# Singleton instance for global access
config = AppConfig()
