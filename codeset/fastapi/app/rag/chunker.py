CHUNK_SIZE    = 500   # 청크 최대 글자 수
CHUNK_OVERLAP = 50    # 앞뒤 청크 겹침 글자 수


def chunk_text(text: str) -> list[str]:
    """텍스트를 CHUNK_SIZE 단위로 분할합니다. 앞뒤 CHUNK_OVERLAP만큼 겹칩니다."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return [c for c in chunks if len(c.strip()) > 20]


def chunk_reports(reports: list[dict]) -> list[dict]:
    """parse_reports() 결과를 청크 단위로 변환합니다."""
    result = []
    for report in reports:
        chunks = chunk_text(report["text"])
        for i, chunk in enumerate(chunks):
            result.append({
                "title":       f"{report['corp_name']} {report['report_type']} chunk{i+1}",
                "content":     chunk,
                "corp_name":   report["corp_name"],
                "report_type": report["report_type"],
                "year":        report["year"],
            })
    return result
