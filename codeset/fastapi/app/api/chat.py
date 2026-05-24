import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.retriever import search

router = APIRouter()

OLLAMA_GEN_URL = "http://localhost:11434/api/generate"
LLM_MODEL      = "gemma4:e2b"


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


def _build_prompt(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[{c['corp_name']} / {c['report_type']}]\n{c['content']}"
        for c in chunks
    )
    return (
        "당신은 초보 투자자를 위한 주식 및 기업 공시 전문 챗봇입니다.\n"
        "아래 참고 자료를 바탕으로 질문에 한국어로 간결하게 답변하세요.\n\n"
        f"[참고 자료]\n{context}\n\n"
        f"[질문]\n{question}\n\n"
        "[답변]"
    )


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    chunks = search(req.question)
    prompt = _build_prompt(req.question, chunks)

    try:
        res = requests.post(
            OLLAMA_GEN_URL,
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        res.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM 호출 실패: {e}")

    answer = res.json()["response"]
    sources = [
        {
            "corp_name":   c["corp_name"],
            "report_type": c["report_type"],
            "title":       c["title"],
        }
        for c in chunks
    ]
    return QueryResponse(answer=answer, sources=sources)
