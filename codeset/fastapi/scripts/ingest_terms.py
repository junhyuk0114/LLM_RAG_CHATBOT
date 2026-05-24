"""
주식 용어 데이터를 OpenSearch에 적재하는 스크립트.

사용법:
  python scripts/ingest_terms.py
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.ingestor import ingest

TERMS_PATH = os.path.join(os.path.dirname(__file__), "../../dataset/stock_terms.json")

if __name__ == "__main__":
    with open(TERMS_PATH, encoding="utf-8") as f:
        terms = json.load(f)

    chunks = []
    for t in terms:
        chunks.append({
            "title":       t["term"],
            "content":     f"{t['term']}: {t['definition']}",
            "corp_name":   "공통",
            "report_type": f"주식용어_{t['category']}",
            "year":        "공통",
        })

    print(f"주식 용어 {len(chunks)}개 임베딩 및 적재 중...")
    saved = ingest(chunks)
    print(f"완료: {saved}건 저장")
