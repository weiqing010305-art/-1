import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """从 .env 读取运行配置，未设置时使用默认值。"""

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_embed_model: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

    chroma_dir: str = os.getenv("CHROMA_DIR", "./chroma_db")
    data_dir: str = os.getenv("DATA_DIR", "./data")

    @property
    def has_llm(self) -> bool:
        return bool(self.openai_api_key)
