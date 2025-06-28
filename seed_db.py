# seed_db.py

import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order

# Clear existing data (optional)
Customer.objects.all().delete()
Product.objects.all().delete()
Order.objects.all().delete()

# Create sample customers
customers = [
    Customer(name="Alice", email="alice@example.com", phone="+1234567890"),
    Customer(name="Bob", email="bob@example.com", phone="123-456-7890"),
    Customer(name="Carol", email="carol@example.com"),
]
Customer.objects.bulk_create(customers)

# Create sample products
products = [
    Product(name="Laptop", price=Decimal("999.99"), stock=10),
    Product(name="Mouse", price=Decimal("25.50"), stock=100),
    Product(name="Keyboard", price=Decimal("45.00"), stock=50),
]
Product.objects.bulk_create(products)

# Create a sample order
alice = Customer.objects.get(email="alice@example.com")
laptop = Product.objects.get(name="Laptop")
mouse = Product.objects.get(name="Mouse")

order = Order.objects.create(customer=alice, total_amount=laptop.price + mouse.price)
order.products.set([laptop, mouse])

print("Database seeded successfully!")
