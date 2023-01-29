__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
import peewee
from models import Tag, Product, User, Sale, User_Product

def search(term):
    query = Product.select().where(term >> Product.name.lower())
    return query


def list_user_products(user_id):
    user = User.get().where(User == user_id)
    query = [Product.get() for product in user.products]
    print ((Product.name, Product.price, (Product.unit_price_cents/100), Product.amount_in_stock) for product in query)
    return query


def list_products_per_tag(tag_id):
    query = Product.select().where(tag_id >> Product.tags)
    print ((Product.name, Product.price, (Product.unit_price_cents/100), Product.amount_in_stock) for product in query)
    return query


def add_product_to_catalog(user_id, product):
    #Product == list[name, description, [tags], unitprice, amount of stock]
    #user_id == user() or user name or email
    new_product = Product.create(name=product[0], description=product[1], unit_price_cents=product[3], amount_in_stock=product[4])
    for tagname in product[2]:
        tag = Tag.get().where(Tag.name == tagname[0])
        if len(tag) == 0:
            Tag.create(name=tag[0])
            tag = Tag.get().where(Tag.name == tagname[0])
        new_product.tags.add(tag)
        new_product.save()
    user = User.get().where((User.name == user_id) | (User == user_id) | ((User.email == user_id)))
    user.products.add(new_product)
    user.save()
    return


def update_stock(product_id, new_quantity):
    ...


def purchase_product(product_id, buyer_id, quantity):
    ...


def remove_product(product_id):
    ...
