import peewee

def main():
    pass

db = peewee.SqliteDatabase(":memory:")


class Tag(peewee.Model):
    tag = peewee.CharField(unique=True)
    description = peewee.CharField()

    class Meta:
        database = db


class Product(peewee.Model):
    name = peewee.CharField()
    seller = peewee.ForeignKeyField(User)
    description = peewee.CharField()
    tags = peewee.ManyToManyField(Tag)
    unit_price_cents = peewee.IntegerField()
    amount_in_stock = peewee.IntegerField(null = False)

    class Meta:
        database = db


class User(peewee.Model):
    email = peewee.CharField(unique=True)
    name = peewee.CharField(default = email)
    address = peewee.CharField()
    billing_information = peewee.CharField()
    products = peewee.ManyToManyField(Product)

    class Meta:
        database = db


class Sale(peewee.model):
    buyer = peewee.ForeignKeyField(User, null = False)
    seller = peewee.ForeignKeyField(User, null = False)
    product_purchased = peewee.ForeignKeyField(Product, null = False)
    quantity = peewee.IntegerField(null = False)

    class Meta:
        database = db


User_Product = User.products.get_through_model()

if __name__ == "__main__":
    main()