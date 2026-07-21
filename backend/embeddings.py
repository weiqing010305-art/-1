import hashlib
import re
import numpy as np

from openai import OpenAI

from backend.config import Config

LOCAL_DIM = 1024
_CJK = re.compile(r"[一-鿿]")


def _tokenize(text: str) -> list[str]:
    """空格分词 + 中文按字、按二元组，提升离线哈希向量的召回相关性。"""
    tokens: list[str] = []
    for word in text.lower().split():
        tokens.append(word)
        if _CJK.search(word):
            chars = [c for c in word if _CJK.match(c)]
            for c in chars:
                tokens.append(c)
            for i in range(len(chars) - 1):
                tokens.append(chars[i] + chars[i + 1])
    return tokens


class Embedder:
    """优先使用 OpenAI 兼容 embedding；无 Key 时退化为本地哈希向量（仅用于离线演示）。"""

    def __init__(self, config: Config):
        self.config = config
        self.client = (
            OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
            if config.openai_api_key
            else None
        )
        self.dim = 1536 if self.client else LOCAL_DIM

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self.client:
            resp = self.client.embeddings.create(
                model=self.config.openai_embed_model, input=texts
            )
            return [d.embedding for d in resp.data]
        return [self._hash_embed(t) for t in texts]

    def _hash_embed(self, text: str) -> list[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        for tok in _tokenize(text):
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            vec[h % self.dim] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()
