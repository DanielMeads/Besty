import main
import peewee
import models
import unittest
from rich.console import Console
console = Console()

Models = [models.Tag, models.Product, models.User, models.Sale, models.UserProduct, models.ProductTag]

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        models.db.bind(Models, bind_refs=False, bind_backrefs=False)
        models.db.connect()
        models.db.create_tables(Models)

    def tearDown(self):
        models.db.drop_tables(Models)
        models.db.close()


def create_test_users():
    test_users= [
        ['test1@test1.com', 'Trevor', '1 Testlane Test City', 'Testcreditcard'],
        ['test2@test2.com', 'Andrew', '2 Testlane Test City', 'Testcreditcard'],
        ['test3@test3.com', 'Sidney', '3 Testlane Test City', 'Testcreditcard'],
        ['test4@test4.com', 'John', '4 Testlane Test City', 'Testcreditcard'],
        ['test5@test5.com', 'Greg', '5 Testlane Test City', 'Testcreditcard'],
        ['test6@test6.com', 'Edward', '6 Testlane Test City', 'Testcreditcard']
    ]
    for test_user in test_users:
        models.User.create(email=test_user[0], name=test_user[1], address=test_user[2], billing_information=test_user[3])
    console.print('Users Created', style='green bold')
    

def get_user_id(number=1):
        return models.User.get(models.User.id == number)


def get_product_id(number=1):
        return models.Product.get(models.Product.id == number)


def get_tag_id(tag):
        return models.Tag.get(models.Tag.tag == tag)


def add_test_product():
    test_products= [
        [get_user_id(3), ['sWeaTER', 'UglY ChRIstMas SweatTer', ['Ugly', 'Wool', 'Red', 'Red'], 256, 36]],
        [get_user_id(6), ['PAntS', 'UglY ChRIstMas Trousers', ['Ugly', 'Ployester', 'Green'], 120, 2]],
        [get_user_id(2), ['PAntS', 'UglY ChRIstMas Shorts', ['Ugly', 'Cotton'], 95, 2]],
        [get_user_id(1), ['ShirT', 'UglY ChRIstMas Shirt', ['Ugly', 'Wool'], 4578, 12]],
        [get_user_id(1), ['ScaRf', 'UglY ChRIstMas Scarf', ['Ugly'], 2453, 4]],
        [get_user_id(5), ['Scarf', 'UglY ChRIstMas Scarf with ribbons on', ['Ugly', 'Nylon', 'Orange', 'Blue'], 1199, 1]]
    ]
    for product in test_products:
        main.add_product_to_catalog(product[0],product[1])
    console.print('Products Created', style='green bold')


def add_test_purchases():
    test_purchases= [
        [get_product_id(3), get_user_id(1), 1],
        [get_product_id(4), get_user_id(5), 4],
        [get_product_id(2), get_user_id(2), 1],
        [get_product_id(1), get_user_id(5), 15],
    ]
    for purchase in test_purchases:
        main.purchase_product(purchase[0], purchase[1], purchase[2])
    console.print('Purchases Enacted', style='green bold')


def add_test_purchases2():
    test_purchases= [
        [get_product_id(3), get_user_id(6), 1],
    ]
    for purchase in test_purchases:
        main.purchase_product(purchase[0], purchase[1], purchase[2])
    console.print('Purchase Enacted', style='green bold')


#BaseTestCase.setUp(BaseTestCase)
#create_test_users()
#add_test_product()
#add_test_purchases()
#add_test_purchases2()
#print (main.search('ChrisstmaS'))
print (main.search('sWeaTER'))
#main.search('scarf')
#main.list_user_products(get_user_id(1))
#main.list_products_per_tag(get_tag_id('Ugly'))
#print([product for product in models.Product.select().join(models.UserProduct).where(models.UserProduct.user == get_user_id(2))])
#print([tag.tag for tag in models.Tag.select()])
#print([product.amount_in_stock for product in models.Product.select()])
#print([product for product in models.UserProduct.select()])
#BaseTestCase.tearDown(BaseTestCase)
