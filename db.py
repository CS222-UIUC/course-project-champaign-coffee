"""Reference: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm"""
import pandas
import csv
from sqlalchemy import create_engine, Column, Integer, String, inspect,  MetaData, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# structure:
# coffee shop table (id, name, location)
# items table (id, name)
# sell (coffee shop id, item id (from items table), price, *ratings)
# primary and foreign keys

engine = create_engine('sqlite:///champaign_menu.db',
                       echo=True, connect_args={'timeout': 1})  # adding timeout to verify that timeout is not the cause of errors
Base = declarative_base()
meta = MetaData()
conn = engine.connect()


class CoffeeShop(Base):
    """SQL Coffee Shop Object by Id, Name, and Location"""
    __tablename__ = 'coffee_shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)


class Item(Base):
    """SQL Item Object by Id and Name"""
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class CoffeeData(Base):
    """SQL Coffee Data Object by Shop, Item, Price, and Ratings"""
    __tablename__ = 'coffee_data'
    coffee_shop_id = Column(Integer, ForeignKey(
        'coffee_shop.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    price = Column(Float)
    ratings = Column(Integer)
    coffee_shop = relationship(CoffeeShop, backref='items')
    item = relationship(Item)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Parse CSV file for database
with open('coffee_data/champaign_coffee_menus.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip first line
    for row in reader:
        csv_item, csv_price, csv_shop, csv_location = row
        if csv_price:  # skip any empty str's
            coffee_shop = session.query(CoffeeShop).filter(
                CoffeeShop.name == csv_shop).first()
            if not coffee_shop:
                # initialize location attribute with csv_location
                coffee_shop = CoffeeShop(name=csv_shop, location=csv_location)
                session.add(coffee_shop)
            # check if the item already exists in the database
            item = session.query(Item).filter(Item.name == csv_item).first()
            if not item:
                item = Item(name=csv_item)
                session.add(item)
            # check if a row with the same coffee_shop and item already exists in the database
            existing_coffee_data = session.query(CoffeeData).filter(
                CoffeeData.coffee_shop == coffee_shop, CoffeeData.item == item).first()
            if existing_coffee_data:
                # if a row already exists, update its price and ratings instead of inserting a new row
                existing_coffee_data.price = float(csv_price)
                existing_coffee_data.ratings = 0
            else:
                # create a new CoffeeData object with the foreign keys to CoffeeShop and Item
                coffee_data = CoffeeData(
                    coffee_shop=coffee_shop, item=item, price=float(csv_price), ratings=0)
                session.add(coffee_data)
                

# INFORMAL TESTING
# Finds and returns all items under $2.00 in Espresso Royale


# def get_item(shop):
#     """Return all items from a specified shop"""
#     get_shop_items = session.query(CoffeeData).join(
#         CoffeeShop).filter(CoffeeData.shop == shop)
#     items = [(item.item.name, item.price, item.shop.name)
#              for item in get_shop_items]
#     return items


# items = get_item('Brew Lab')
# print(items)


# inspector = inspect(engine)
# table_names = inspector.get_table_names()
# table_name = table_names[0] if len(table_names) == 1 else ''
# print(table_name)

# print(inspector.get_table_names())


# session.close()
