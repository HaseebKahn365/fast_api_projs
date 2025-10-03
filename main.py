from fastapi import FastAPI
from models import Product
from elasticsearch_client import index_product, search_products
from redis_client import get_cache, set_cache
import json

app = FastAPI()

@app.post("/products")
def create_product(product: Product):
    index_product(product)
    return {"message": "Product indexed"}

@app.get("/search")
def search(query: str):
    cache_key = f"search:{query}"
    cached_result = get_cache(cache_key)
    if cached_result:
        print("Cache hit")
        return {"results": cached_result, "source": "cache"}
    else:
        print("Cache miss, searching Elasticsearch")
        results = search_products(query)
        set_cache(cache_key, results)
        return {"results": results, "source": "elasticsearch"}