__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
import peewee
from textblob import TextBlob
from models import Tag, Product, User, Sale, UserProduct, ProductTag

def search(term):
    tospellcheck = TextBlob(term.lower())
    term = str(tospellcheck.correct())
    query = Product.select()
    results = []
    for product in query:
        if (product.name.lower() == term) or (term in product.description.lower()):
            if product.amount_in_stock > 0:
                results.append([product.name, (product.unit_price_cents/100), product.amount_in_stock])
    print(results)


def list_user_products(user_id):
    userproducts = UserProduct.select().where(UserProduct.user == user_id)
    results = []
    for product in userproducts:
        product1 = Product.get(product.id == Product.id)
        results.append([product1.name, (product1.unit_price_cents/100), product1.amount_in_stock])
    print(results)


def list_products_per_tag(tag_id):
    productswithtag = ProductTag.select().where(ProductTag.tag == tag_id)
    results = []
    for product in productswithtag:
        product1 = Product.get(Product.id == product.product.id)
        if product1.amount_in_stock > 0:
            results.append([product1.name, (product1.unit_price_cents/100), product1.amount_in_stock])
    print(results)


def add_product_to_catalog(user_id, product):
    new_product = Product.create(name=product[0], description=product[1], unit_price_cents=product[3], amount_in_stock=product[4])
    UserProduct.create(user=user_id, product=new_product)
    for tagname in product[2]:
        try:
            tag = Tag.create(tag=tagname)
        except:
            tag = Tag.get(Tag.tag == tagname)
        ProductTag.create(product=new_product, tag=tag)


def update_stock(product_id, new_quantity):
    query = product_id.update(amount_in_stock=new_quantity).where(Product.id == product_id)
    query.execute()


def purchase_product(product_id, buyer_id, quantity):
    seller_id = UserProduct.get(UserProduct.product == product_id)
    new_sale = Sale.create(buyer=buyer_id, seller=seller_id.user, product_purchased=product_id, quantity=quantity)
    newquantity = product_id.amount_in_stock - quantity
    if newquantity < 1:
        remove_product(product_id)
    else:
        update_stock(product_id, newquantity)


def remove_product(product_id):
    query1 = product_id.update(amount_in_stock=0).where(Product.id == product_id) 
    query1.execute()   
    query2 = UserProduct.delete().where(UserProduct.product == product_id)
    query2.execute() 

