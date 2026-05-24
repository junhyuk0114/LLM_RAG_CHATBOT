import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OPENSEARCH_URL = "https://localhost:9200"
OPENSEARCH_AUTH = ("admin", "admin")
INDEX_NAME = "dart_docs"

# bge-m3 모델의 임베딩 차원
EMBEDDING_DIM = 1024

mapping = {
    "settings": {
        "index": {
            "knn": True,
            "knn.algo_param.ef_search": 100
        },
        "analysis": {
            "analyzer": {
                "nori_analyzer": {
                    "type": "custom",
                    "tokenizer": "nori_tokenizer",
                    "filter": ["nori_posfilter"]
                }
            },
            "filter": {
                "nori_posfilter": {
                    "type": "nori_part_of_speech",
                    "stoptags": [
                        "JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC",
                        "EF", "EC", "EP", "ETN", "ETM",
                        "XPN", "XSN", "XSV", "XSA"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "title":       {"type": "text", "analyzer": "nori_analyzer"},
            "content":     {"type": "text", "analyzer": "nori_analyzer"},
            "corp_name":   {"type": "keyword"},
            "report_type": {"type": "keyword"},
            "year":        {"type": "keyword"},
            "embedding": {
                "type": "knn_vector",
                "dimension": EMBEDDING_DIM,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "lucene"
                }
            }
        }
    }
}

def create_index():
    # 기존 인덱스 존재 여부 확인
    res = requests.get(f"{OPENSEARCH_URL}/{INDEX_NAME}", auth=OPENSEARCH_AUTH, verify=False)
    if res.status_code == 200:
        print(f"인덱스 '{INDEX_NAME}' 이미 존재합니다.")
        return

    # 인덱스 생성
    res = requests.put(
        f"{OPENSEARCH_URL}/{INDEX_NAME}",
        auth=OPENSEARCH_AUTH,
        verify=False,
        headers={"Content-Type": "application/json"},
        data=json.dumps(mapping)
    )
    if res.status_code == 200:
        print(f"인덱스 '{INDEX_NAME}' 생성 완료!")
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    else:
        print(f"생성 실패: {res.status_code}")
        print(res.text)

if __name__ == "__main__":
    create_index()
