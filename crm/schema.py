# crm/schema.py
import graphene
from graphene import Field, List, Mutation, InputObjectType, ID, String, Decimal, Int, Float
from .models import Customer, Product, Order
from .graphql_types import CustomerType, ProductType, OrderType
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter

# --- Inputs ---

class CustomerInput(InputObjectType):
    name = String(required=True)
    email = String(required=True)
    phone = String()

class ProductInput(InputObjectType):
    name = String(required=True)
    price = Decimal(required=True)
    # price = Float(required=True)
    stock = Int()

class OrderInput(InputObjectType):
    customer_id = ID(required=True)
    product_ids = List(ID, required=True)
    order_date = String()

# --- Mutations ---

class CreateCustomer(Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = Field(CustomerType)
    message = String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise GraphQLError("Email already Exists")

        if input.phone and not re.match(r'^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$', input.phone):
            raise GraphQLError("Invalid phone format")

        customer = Customer.objects.create(**input)
        return CreateCustomer(customer=customer, message="Customer created successfully")


class BulkCreateCustomers(Mutation):
    class Arguments:
        input = List(CustomerInput)

    customers = List(CustomerType)
    errors = List(String)

    def mutate(self, info, input):
        customers = []
        errors = []

        for data in input:
            try:
                if Customer.objects.filter(email=data.email).exists():
                    raise GraphQLError(f"Email {data.email} already exists")

                if data.phone and not re.match(r'^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$', data.phone):
                    raise GraphQLError(f"Invalid phone format for {data.name}")

                customer = Customer.objects.create(**data)
                customers.append(customer)

            except Exception as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=customers, errors=errors)


class CreateProduct(Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise GraphQLError("Price must be positive")
        if input.stock is not None and input.stock < 0:
            raise GraphQLError("Stock cannot be negative")

        product = Product.objects.create(**input)
        return CreateProduct(product=product)


class CreateOrder(Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Customer not found")

        if not input.product_ids:
            raise GraphQLError("At least one product must be selected")

        products = []
        total_amount = 0

        for pid in input.product_ids:
            try:
                product = Product.objects.get(pk=pid)
                products.append(product)
                total_amount += product.price
            except Product.DoesNotExist:
                raise GraphQLError(f"Invalid product ID: {pid}")

        order = Order.objects.create(customer=customer, total_amount=total_amount)
        order.products.set(products)
        return CreateOrder(order=order)

# --- Queries ---
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
    all_products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
    all_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)
    # all_customers = graphene.List(CustomerType)
    # all_products = graphene.List(ProductType)
    # all_orders = graphene.List(OrderType)

    # def resolve_all_customers(root, info):
    #     return Customer.objects.all()

    # def resolve_all_products(root, info):
    #     return Product.objects.all()

    # def resolve_all_orders(root, info):
    #     return Order.objects.all()
    hello = graphene.String()

    def resolve_hello(root, info):
        return "CRM is alive"


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()