# DART RAG 챗봇

DART(전자공시시스템) 기업 공시 데이터를 기반으로 초보 투자자의 질문에 답변하는 RAG(Retrieval-Augmented Generation) 챗봇입니다.

## 아키텍처

```
[Spring MVC 프론트엔드]
        ↓ HTTP
[FastAPI 백엔드]
   ├── DART API → 공시 원문 수집 (parser)
   ├── 청킹 (chunker) → 500자 단위 분할
   ├── 임베딩 (Ollama bge-m3) → 1024차원 벡터
   ├── OpenSearch kNN 인덱스 (dart_docs)
   └── Ollama gemma4:e2b → 답변 생성
```

## 기술 스택

| 레이어 | 기술 |
|---|---|
| 프론트엔드 | Spring MVC, JSP |
| 백엔드 API | FastAPI (Python) |
| 벡터 DB | OpenSearch 3.3 (kNN + Nori 형태소 분석기) |
| 임베딩 모델 | `bge-m3` via Ollama |
| 생성 모델 | `gemma4:e2b` via Ollama |
| 공시 데이터 | DART OpenAPI (`opendart.fss.or.kr`) |

## 프로젝트 구조

```
RAGpjt/
├── codeset/
│   ├── fastapi/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   └── chat.py          # POST /query 엔드포인트
│   │   │   └── rag/
│   │   │       ├── parser.py        # DART API 공시 수집 및 텍스트 추출
│   │   │       ├── chunker.py       # 텍스트 청킹 (500자, overlap 50자)
│   │   │       ├── embedder.py      # Ollama bge-m3 임베딩
│   │   │       ├── ingestor.py      # OpenSearch 벌크 적재
│   │   │       ├── retriever.py     # kNN 벡터 검색
│   │   │       └── index_setup.py   # OpenSearch 인덱스 생성
│   │   ├── scripts/
│   │   │   ├── run_ingest.py        # 주요 기업 공시 적재 실행
│   │   │   └── run_ingest_hd.py     # HD한국조선해양 공시 적재
│   │   ├── requirements.txt
│   │   └── .env
│   ├── dataset/
│   │   └── stock_terms.json         # 주식 용어 사전
│   └── spring/
│       └── src_tree.txt             # Spring 프로젝트 구조
```

## 사전 요구사항

- Python 3.10+
- [Ollama](https://ollama.ai) 설치 및 실행
- OpenSearch 3.3+ (kNN 플러그인, Nori 플러그인 포함)
- DART OpenAPI 인증키

### Ollama 모델 준비

```bash
ollama pull bge-m3
ollama pull gemma4:e2b
```

## 설치 및 실행

### 1. 환경 변수 설정

`codeset/fastapi/.env` 파일을 수정합니다.

```env
DART_API_KEY=your_dart_api_key
OPENSEARCH_URL=https://localhost:9200
OPENSEARCH_USER=admin
OPENSEARCH_PASSWORD=your_password
```

### 2. 패키지 설치

```bash
cd codeset/fastapi
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. OpenSearch 인덱스 생성

```bash
python -m app.rag.index_setup
```

### 4. 공시 데이터 적재

```bash
python scripts/run_ingest.py
```

기본 적재 대상 기업: 삼성전자, 현대자동차, NAVER, KB금융, HD한국조선해양

### 5. API 서버 실행

```bash
uvicorn app.main:app --reload
```

서버 기동 후 `http://localhost:8000/health` 에서 상태를 확인할 수 있습니다.

## API

### `POST /query`

질문을 입력하면 관련 공시 청크를 검색하고 LLM이 한국어로 답변을 생성합니다.

**Request**
```json
{ "question": "삼성전자의 최근 실적은 어떤가요?" }
```

**Response**
```json
{
  "answer": "...",
  "sources": [
    {
      "corp_name": "삼성전자",
      "report_type": "사업보고서",
      "title": "삼성전자 사업보고서 chunk3"
    }
  ]
}
```

## RAG 파이프라인 상세

1. **수집**: DART API로 기업 공시 원문(ZIP/XML)을 다운로드하고 HTML 태그를 제거합니다.
2. **청킹**: 500자 단위로 분할하며 앞뒤 50자를 겹쳐 문맥 단절을 방지합니다.
3. **임베딩**: Ollama `bge-m3`로 각 청크를 1024차원 벡터로 변환합니다.
4. **저장**: OpenSearch `dart_docs` 인덱스에 벌크 적재합니다 (HNSW + cosine similarity).
5. **검색**: 질문을 임베딩하여 kNN으로 상위 5개 청크를 조회합니다.
6. **생성**: 검색된 청크를 컨텍스트로 `gemma4:e2b`에 전달하여 한국어 답변을 생성합니다.
