import requests

OLLAMA_URL  = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"


def embed(text: str) -> list[float]:
    """텍스트 1개를 벡터로 변환합니다."""
    res = requests.post(OLLAMA_URL, json={"model": EMBED_MODEL, "input": text}, timeout=30)
    res.raise_for_status()
    return res.json()["embeddings"][0]


def embed_batch(texts: list[str]) -> list[list[float]]:
    """텍스트 목록을 벡터 목록으로 변환합니다."""
    return [embed(t) for t in texts]
