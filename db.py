"""Reference: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm"""
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///champaign_menu.db', echo=True)
Base = declarative_base()
class CoffeeData(Base):
    """SQL Coffee Data Object by Id, Item, Price, and Shop"""
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True)
    item = Column(String)
    price = Column(String) # should change to float but gives parsing error
    shop = Column(String)
    def pub1(self):
        """Pylint case"""
    def pub2(self):
        """Pylint case"""
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Parse CSV file for database
with open('coffee_data/champaign_coffee_menus.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        csv_item, csv_price, csv_shop = row
        menu_item = CoffeeData(item=csv_item, price=csv_price, shop=csv_shop)
        session.add(menu_item)

# INFORMAL TESTING
# Finds and returns all items under $2.00 in Espresso Royale
def get_item(shop):
    """Return all items from a specified shop"""
    get_shop_items = session.query(CoffeeData).filter(CoffeeData.shop == shop)
    for item in get_shop_items:
        print(item.item, item.price, item.shop)

get_item('Brew Lab')
