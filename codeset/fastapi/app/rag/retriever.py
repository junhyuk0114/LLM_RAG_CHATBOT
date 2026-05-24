import os
import requests
import urllib3
from dotenv import load_dotenv

from app.rag.embedder import embed

load_dotenv()
urllib3.disable_warnings()

OPENSEARCH_URL  = os.getenv("OPENSEARCH_URL", "https://localhost:9200")
OPENSEARCH_AUTH = (os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin"))
INDEX_NAME      = "dart_docs"
TOP_K           = 5


def search(question: str, top_k: int = TOP_K) -> list[dict]:
    """질문을 임베딩하여 OpenSearch에서 유사 청크를 반환합니다."""
    vector = embed(question)
    body = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": vector,
                    "k": top_k,
                }
            }
        },
        "_source": ["title", "content", "corp_name", "report_type", "year"],
    }
    res = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_search",
        auth=OPENSEARCH_AUTH,
        verify=False,
        json=body,
        timeout=30,
    )
    res.raise_for_status()
    hits = res.json()["hits"]["hits"]
    return [h["_source"] for h in hits]
