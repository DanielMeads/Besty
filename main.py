__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
import peewee
from peewee import fn, JOIN
from textblob import TextBlob
from models import Tag, Product, User, Sale, UserProduct, ProductTag

# Get database id information for further use
def get_user_id(user=1):
    if type(user) == str:
        return User.get(User.name == user)
    elif type(user) == int:
        return User.get(User.id == user)


def get_product_id(product=1):
    if type(product) == str:
        return User.get((fn.Lower(Product.name)) == (fn.Lower(product)))
    elif type(product) == int:
        return Product.get(Product.id == product)


def get_tag_id(tag):
    return Tag.get(Tag.tag == tag)


# Main searches
def search(term):
    #Attempts spellcheck
    tospellcheck = TextBlob(term.lower())
    term2 = str(tospellcheck.correct())
    query = Product.select().where(
        (fn.Lower(term) % fn.Lower(Product.name)) | term2 % fn.Lower(Product.name)
    )
    return [[product.name, product.unit_price_cents / 100, product.amount_in_stock] for product in query]


def list_user_products(user):
    userproducts = (
        Product.select()
        .join(UserProduct, JOIN.LEFT_OUTER)
        .where(UserProduct.user_id == user_id)
    )
    return [product.name for product in userproducts]


def list_products_per_tag(tag):
    #Tag must be a known tag name or id i.e. 'Ugly' or 'Wool'
    id = get_tag_id(tag)
    productswithtag = ProductTag.select(ProductTag.product_id).where(
        ProductTag.tag_id == id
    )
    products = Product.select().where(Product.id.in_(productswithtag))
    return [product.name for product in products]


def add_product_to_catalog(user_id, product):
    # Requires a user name or ID i.e "Trevor" and a List of product information i.e.['ProductName', 'Description', [List of Tags], Price in cents, Amount]
    user_id = get_user_id(user_id)
    new_product = Product.create(
        name=product[0],
        description=product[1],
        unit_price_cents=product[3],
        amount_in_stock=product[4],
    )
    UserProduct.create(user=user_id, product=new_product)
    # Creates tags or returns an existing tags id
    for tagname in product[2]:
        try:
            tag = Tag.create(tag=tagname)
        except:
            tag = Tag.get(Tag.tag == tagname)
        #Logs the Products Tags
        ProductTag.create(product=new_product, tag=tag)


def purchase_product(product_id, buyer_id, quantity):
    # Takes a product name or id i.e 'Pants' or 2, a buyer name or id i.e "Trevor" or 1, and a quantity
    product_id = get_product_id(product_id)
    buyer_id = get_user_id(buyer_id)
    # Find seller ID
    seller_id = UserProduct.get(UserProduct.product == product_id)
    new_sale = Sale.create(buyer=buyer_id, seller=seller_id.user, product_purchased=product_id, quantity=quantity)
    newquantity = product_id.amount_in_stock - quantity
    if newquantity < 1:
        # Removes the product from sale
        query = product_id.update(amount_in_stock=0).where(Product.id == product_id) 
        query.execute()   
        #Removes the product from the User so will no longer be referenced
        query2 = UserProduct.delete().where(UserProduct.product == product_id)
        query2.execute() 
    else:
        # Adjusts the stock
        query = product_id.update(amount_in_stock=newquantity).where(Product.id == product_id)
        query.execute()
