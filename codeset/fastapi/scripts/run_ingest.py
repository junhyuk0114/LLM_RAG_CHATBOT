"""
DART 공시 데이터를 OpenSearch에 적재하는 실행 스크립트.

사용법:
  python scripts/run_ingest.py

적재 대상 기업 및 기간은 아래 TARGETS를 수정하세요.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.parser  import parse_reports
from app.rag.chunker import chunk_reports
from app.rag.ingestor import ingest

# 사업보고서만 100,000자 제한 / 분기·반기보고서는 제한 없음
ANNUAL_MAX_LEN = 100000

# 적재 대상: (corp_code, corp_name, 시작일, 종료일)
TARGETS = [
    ("00126380", "삼성전자",      "20250101", "20260525"),
    ("00164742", "현대자동차",    "20250101", "20260525"),
    ("00266961", "NAVER",         "20250101", "20260525"),
    ("00688996", "KB금융",        "20250101", "20260525"),
    ("00164830", "HD한국조선해양","20250101", "20260525"),
]

def apply_limit(report: dict) -> dict:
    if "사업보고서" in report.get("report_type", ""):
        report["text"] = report["text"][:ANNUAL_MAX_LEN]
    return report

if __name__ == "__main__":
    total = 0
    for corp_code, corp_name, bgn_de, end_de in TARGETS:
        print(f"\n[{corp_name}] 공시 조회 중...")
        reports = parse_reports(corp_code, corp_name, bgn_de, end_de)
        if not reports:
            print(f"  → 공시 없음")
            continue
        print(f"  → {len(reports)}건 공시 확인, 청킹 중...")
        for r in reports:
            apply_limit(r)
            print(f"     - {r['report_type']}: {len(r['text']):,}자")
        chunks = chunk_reports(reports)
        print(f"  → {len(chunks)}개 청크 생성, 임베딩 및 적재 중...")
        saved = ingest(chunks)
        total += saved
        print(f"  → {saved}건 저장 완료")

    print(f"\n전체 {total}건 적재 완료")
