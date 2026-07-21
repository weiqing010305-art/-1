from openai import OpenAI

from backend.config import Config


class LLM:
    """OpenAI 兼容对话客户端；无 Key 时 client 为 None，由调用方降级处理。"""

    def __init__(self, config: Config):
        self.config = config
        self.client = (
            OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
            if config.openai_api_key
            else None
        )

    def answer(self, system: str, user: str) -> str | None:
        if not self.client:
            return None
        resp = self.client.chat.completions.create(
            model=self.config.openai_model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content
