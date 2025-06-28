# crm/graphql_types.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Customer, Product, Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (graphene.relay.Node, )

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node, )

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (graphene.relay.Node, )



# import graphene
# from graphene_django import DjangoObjectType
# from .models import Customer, Product, Order

# class CustomerType(DjangoObjectType):
#     class Meta:
#         model = Customer

# class ProductType(DjangoObjectType):
#     class Meta:
#         model = Product

# class OrderType(DjangoObjectType):
#     class Meta:
#         model = Order
