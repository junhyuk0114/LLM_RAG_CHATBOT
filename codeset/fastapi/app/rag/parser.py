import os
import requests
from dotenv import load_dotenv

load_dotenv()

DART_API_KEY = os.getenv("DART_API_KEY")
DART_LIST_URL = "https://opendart.fss.or.kr/api/list.json"
DART_DOC_URL  = "https://opendart.fss.or.kr/api/document.xml"


def fetch_report_list(corp_code: str, bgn_de: str, end_de: str, pblntf_ty: str = "A") -> list[dict]:
    """DART에서 공시 목록을 가져옵니다."""
    params = {
        "crtfc_key": DART_API_KEY,
        "corp_code": corp_code,
        "bgn_de": bgn_de,
        "end_de": end_de,
        "pblntf_ty": pblntf_ty,  # A: 정기공시
        "page_count": 2,
    }
    res = requests.get(DART_LIST_URL, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()
    if data.get("status") != "000":
        print(f"DART 오류: {data.get('message')}")
        return []
    return data.get("list", [])


def fetch_document_text(rcept_no: str) -> str:
    """공시 원문 XML에서 텍스트를 추출합니다."""
    params = {"crtfc_key": DART_API_KEY, "rcept_no": rcept_no}
    res = requests.get(DART_DOC_URL, params=params, timeout=15)
    res.raise_for_status()
    # XML에서 태그 제거 후 순수 텍스트만 추출
    import re
    text = re.sub(r"<[^>]+>", " ", res.text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_reports(corp_code: str, corp_name: str, bgn_de: str, end_de: str) -> list[dict]:
    """공시 목록 조회 → 원문 텍스트 추출까지 수행합니다."""
    reports = fetch_report_list(corp_code, bgn_de, end_de)
    results = []
    for r in reports:
        text = fetch_document_text(r["rcept_no"])
        if not text:
            continue
        results.append({
            "corp_name":   corp_name,
            "report_type": r.get("report_nm", ""),
            "year":        r.get("rcept_dt", "")[:4],
            "rcept_no":    r["rcept_no"],
            "text":        text,
        })
    return results
