import peewee

db = peewee.SqliteDatabase(":memory:")


class Tag(peewee.Model):
    tag = peewee.CharField(unique=True)
    description = peewee.CharField(null = True)

    class Meta:
        database = db


class Product(peewee.Model):
    name = peewee.CharField()
    description = peewee.CharField()
    tags = peewee.ManyToManyField(Tag)
    unit_price_cents = peewee.IntegerField()
    amount_in_stock = peewee.IntegerField()

    class Meta:
        database = db



class User(peewee.Model):
    email = peewee.CharField(unique=True)
    name = peewee.CharField()
    address = peewee.CharField()
    billing_information = peewee.CharField()
    products = peewee.ManyToManyField(Product)

    class Meta:
        database = db


class Sale(peewee.Model):
    buyer = peewee.ForeignKeyField(User, null = False)
    seller = peewee.ForeignKeyField(User, null = False)
    product_purchased = peewee.ForeignKeyField(Product, null = False)
    quantity = peewee.IntegerField(null = False)

    class Meta:
        database = db


class ProductTag(peewee.Model):
    product = peewee.ForeignKeyField(Product, null = False)
    tag = peewee.ForeignKeyField(Tag, null = False)

    class Meta:
        database = db


class UserProduct(peewee.Model):
    user = peewee.ForeignKeyField(User, null = False)
    product = peewee.ForeignKeyField(Product, null = False)

    class Meta:
        database = db
