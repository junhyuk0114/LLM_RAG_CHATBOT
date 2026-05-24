import os
import json
import requests
import urllib3
from dotenv import load_dotenv
from app.rag.embedder import embed

load_dotenv()
urllib3.disable_warnings()

OPENSEARCH_URL  = os.getenv("OPENSEARCH_URL", "https://localhost:9200")
OPENSEARCH_AUTH = (os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin"))
INDEX_NAME      = "dart_docs"
BULK_SIZE       = 50


def ingest(chunks: list[dict]) -> int:
    """청크 목록을 임베딩하여 OpenSearch에 적재합니다. 저장된 건수를 반환합니다."""
    total = 0
    for i in range(0, len(chunks), BULK_SIZE):
        batch = chunks[i:i + BULK_SIZE]
        bulk_body = ""
        for chunk in batch:
            meta   = json.dumps({"index": {"_index": INDEX_NAME}})
            vector = embed(chunk["content"])
            doc    = {
                "title":       chunk["title"],
                "content":     chunk["content"],
                "corp_name":   chunk["corp_name"],
                "report_type": chunk["report_type"],
                "year":        chunk["year"],
                "embedding":   vector,
            }
            bulk_body += meta + "\n" + json.dumps(doc, ensure_ascii=False) + "\n"

        res = requests.post(
            f"{OPENSEARCH_URL}/_bulk",
            auth=OPENSEARCH_AUTH,
            verify=False,
            headers={"Content-Type": "application/x-ndjson"},
            data=bulk_body.encode("utf-8"),
            timeout=60,
        )
        res.raise_for_status()
        result = res.json()
        saved = sum(1 for item in result["items"] if item["index"]["status"] in (200, 201))
        total += saved
        print(f"  배치 {i // BULK_SIZE + 1}: {saved}건 저장")

    return total
