import requests

OLLAMA_URL  = "http://localhost:11434/api/embed"
EMBED_MODEL = "bge-m3"


def embed(text: str) -> list[float]:
    """텍스트 1개를 벡터로 변환합니다."""
    for attempt in range(3):
        try:
            res = requests.post(OLLAMA_URL, json={"model": EMBED_MODEL, "input": text}, timeout=120)
            res.raise_for_status()
            return res.json()["embeddings"][0]
        except requests.exceptions.Timeout:
            if attempt == 2:
                raise
            print(f"  [임베딩 타임아웃 재시도 {attempt+1}/3]")


def embed_batch(texts: list[str]) -> list[list[float]]:
    """텍스트 목록을 벡터 목록으로 변환합니다."""
    return [embed(t) for t in texts]
