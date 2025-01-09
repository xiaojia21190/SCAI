from dataclasses import dataclass
from typing import List
from elasticsearch import Elasticsearch
import json

@dataclass
class Paper:
    id: str
    title: str
    authors: str
    abstract: str
    categories: List[str]

class MetadataSearch:
    def __init__(self, es_host: str = "localhost"):
        self.es = Elasticsearch(es_host)
    
    def search(self, query: str, size: int = 10) -> List[Paper]:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "abstract", "authors"],
                    "type": "best_fields"
                }
            }
        }
        
        response = self.es.search(index="arxiv", body=body, size=size)
        
        papers = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            papers.append(Paper(
                id=source["id"],
                title=source["title"],
                authors=source["authors"],
                abstract=source["abstract"],
                categories=source["categories"]
            ))
        
        return papers