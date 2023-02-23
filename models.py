import peewee

db = peewee.SqliteDatabase("betsy.db")

class Meta(peewee.Model):
        database = db
        
class Tag(Meta):
    tag = peewee.CharField(unique=True)
    description = peewee.CharField(null = True)

class Product(Meta):
    name = peewee.CharField()
    description = peewee.CharField()
    tags = peewee.ManyToManyField(Tag)
    unit_price_cents = peewee.IntegerField()
    amount_in_stock = peewee.IntegerField()

class User(Meta):
    email = peewee.CharField(unique=True)
    name = peewee.CharField()
    address = peewee.CharField()
    billing_information = peewee.CharField()
    products = peewee.ManyToManyField(Product)

class Sale(Meta):
    buyer = peewee.ForeignKeyField(User, null = False)
    seller = peewee.ForeignKeyField(User, null = False)
    product_purchased = peewee.ForeignKeyField(Product, null = False)
    quantity = peewee.IntegerField(null = False)

class ProductTag(Meta):
    product = peewee.ForeignKeyField(Product, null = False)
    tag = peewee.ForeignKeyField(Tag, null = False)

class UserProduct(Meta):
    user = peewee.ForeignKeyField(User, null = False)
    product = peewee.ForeignKeyField(Product, null = False)