# crm/seed_db2.py
import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order

# Sample data
FIRST_NAMES = [
    "Alice", "Bob", "Carol", "David", "Eva",
    "Frank", "Grace", "Henry", "Ivy", "Jack",
    "Kara", "Leo", "Mona", "Nate", "Olivia",
    "Paul", "Queenie", "Ray", "Sophie", "Tom"
]

PRODUCT_NAMES = [
    "Laptop", "Desk Chair", "Monitor", "Keyboard", "Mouse",
    "Smartphone", "Tablet", "USB Hub", "Webcam", "Headphones",
    "Printer", "Standing Desk", "External Drive", "Router", "Microphone"
]

def clear_data():
    Order.objects.all().delete()
    Customer.objects.all().delete()
    Product.objects.all().delete()

def seed_customers():
    print("Seeding customers...")
    customers = []
    base_date = datetime(2025, 1, 1)

    for i, first_name in enumerate(FIRST_NAMES):
        name = first_name
        email = f"{first_name.lower()}@example.com"
        phone = (
            f"+1{random.randint(1000000000, 9999999999)}"
            if i % 2 == 0
            else f"123-456-{random.randint(1000, 9999)}"
        )
        created_at = base_date + timedelta(days=i)
        c = Customer(name=name, email=email, phone=phone, created_at=created_at)
        c.save()
        customers.append(c)

    return customers

def seed_products():
    print("Seeding products...")
    products = []

    for name in PRODUCT_NAMES:
        price = Decimal(f"{random.uniform(20, 1500):.2f}")
        stock = random.randint(0, 100)
        p = Product(name=name, price=price, stock=stock)
        p.save()
        products.append(p)

    return products

def seed_orders(customers, products):
    print("Seeding orders...")

    for _ in range(25):
        customer = random.choice(customers)
        selected_products = random.sample(products, k=random.randint(1, 3))
        total = sum(p.price for p in selected_products)
        order_date = datetime.now() - timedelta(days=random.randint(0, 90))
        order = Order.objects.create(customer=customer, total_amount=total, order_date=order_date)
        order.products.set(selected_products)

def run():
    clear_data()
    customers = seed_customers()
    products = seed_products()
    seed_orders(customers, products)
    print("Seeding complete.")

if __name__ == "__main__":
    run()