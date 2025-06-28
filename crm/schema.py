# crm/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
import re


# Object Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists.")

        if input.phone and not re.match(r"^\+?\d{7,15}$|^\d{3}-\d{3}-\d{4}$", input.phone):
            raise Exception("Invalid phone format.")

        customer = Customer.objects.create(**input)
        return CreateCustomer(customer=customer, message="Customer created successfully.")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []

        with transaction.atomic():
            for i, data in enumerate(input):
                try:
                    if Customer.objects.filter(email=data.email).exists():
                        raise Exception(f"Row {i+1}: Email already exists")

                    if data.phone and not re.match(r"^\+?\d{7,15}$|^\d{3}-\d{3}-\d{4}$", data.phone):
                        raise Exception(f"Row {i+1}: Invalid phone format")

                    customer = Customer(name=data.name, email=data.email, phone=data.phone)
                    customer.save()
                    customers.append(customer)
                except Exception as e:
                    errors.append(str(e))

        return BulkCreateCustomers(customers=customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive.")
        if input.stock is not None and input.stock < 0:
            raise Exception("Stock cannot be negative.")

        product = Product.objects.create(**input)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID.")

        if not product_ids:
            raise Exception("At least one product must be selected.")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("One or more product IDs are invalid.")

        total = sum(p.price for p in products)
        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            order_date=order_date or timezone.now()
        )
        order.products.set(products)
        return CreateOrder(order=order)


# Query placeholder
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()


# Mutation root
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
