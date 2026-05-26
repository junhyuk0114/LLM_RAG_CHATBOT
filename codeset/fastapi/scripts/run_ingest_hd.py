"""HD한국조선해양 단독 적재 스크립트 (기존 데이터 삭제 후 재적재)"""
import sys, os, requests, urllib3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
urllib3.disable_warnings()

from app.rag.parser   import parse_reports
from app.rag.chunker  import chunk_reports
from app.rag.ingestor import ingest

ANNUAL_MAX_LEN = 100000
OS_URL  = "https://localhost:9200"
OS_AUTH = ("admin", "admin")

def delete_existing():
    """기존 HD한국조선해양 문서 삭제"""
    body = {"query": {"term": {"corp_name": "HD한국조선해양"}}}
    r = requests.post(f"{OS_URL}/dart_docs/_delete_by_query",
                      auth=OS_AUTH, verify=False, json=body, timeout=30)
    deleted = r.json().get("deleted", 0)
    print(f"  기존 HD한국조선해양 문서 {deleted}건 삭제 완료")

def apply_limit(report):
    if "사업보고서" in report.get("report_type", ""):
        report["text"] = report["text"][:ANNUAL_MAX_LEN]
    return report

if __name__ == "__main__":
    corp_code, corp_name = "00164830", "HD한국조선해양"

    print(f"[{corp_name}] 기존 데이터 정리 중...")
    delete_existing()

    print(f"[{corp_name}] 공시 조회 중...")
    reports = parse_reports(corp_code, corp_name, "20250101", "20260525")
    if not reports:
        print("  → 공시 없음")
        sys.exit(0)

    print(f"  → {len(reports)}건 공시 확인, 청킹 중...")
    for r in reports:
        apply_limit(r)
        print(f"     - {r['report_type']}: {len(r['text']):,}자")

    chunks = chunk_reports(reports)
    print(f"  → {len(chunks)}개 청크 생성, 임베딩 및 적재 중...")
    saved = ingest(chunks)
    print(f"\n완료: {saved}건 저장")
