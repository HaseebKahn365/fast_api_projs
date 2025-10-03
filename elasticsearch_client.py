from elasticsearch import Elasticsearch
from models import Product
import json

es = Elasticsearch("http://localhost:9200")

def index_product(product: Product):
    doc = product.dict()
    es.index(index="products", id=product.id, document=doc)
    print(f"Indexed product: {product.name}")

def search_products(query: str):
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "description"]
            }
        }
    }
    response = es.search(index="products", body=search_body)
    hits = response['hits']['hits']
    results = [hit['_source'] for hit in hits]
    return results