from models import Product
from elasticsearch_client import index_product

# Sample products
products = [
    Product(id=1, name="Laptop", description="A high-performance laptop for work and gaming", price=1200.0),
    Product(id=2, name="Smartphone", description="Latest smartphone with advanced features", price=800.0),
    Product(id=3, name="Headphones", description="Noise-cancelling wireless headphones", price=200.0),
    Product(id=4, name="Tablet", description="Portable tablet for entertainment", price=500.0),
    Product(id=5, name="Smartwatch", description="Fitness tracking smartwatch", price=300.0)
]

for product in products:
    index_product(product)

print("Sample products indexed.")