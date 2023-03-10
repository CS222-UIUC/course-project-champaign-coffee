"""Reference: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm"""
import pandas
import csv
from sqlalchemy import create_engine, Column, Integer, String, inspect,  MetaData, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///champaign_menu.db',
                       echo=True, connect_args={'timeout': 1}) #adding timeout to verify that timeout is not the cause of errors
Base = declarative_base()
meta = MetaData()
conn = engine.connect()


class CoffeeData(Base):
    """SQL Coffee Data Object by Id, Item, Price, and Shop"""
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True)
    item = Column(String)
    price = Column(Float)  
    shop = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Parse CSV file for database
with open('coffee_data/champaign_coffee_menus.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip first line
    for row in reader:
        csv_item, csv_price, csv_shop = row
        if csv_price:  # skip any empty str's
            menu_item = CoffeeData(
                item=csv_item, price=float(csv_price), shop=csv_shop)
            session.add(menu_item)

# INFORMAL TESTING
# Finds and returns all items under $2.00 in Espresso Royale


def get_item(shop):
    """Return all items from a specified shop"""
    get_shop_items = session.query(CoffeeData).filter(CoffeeData.shop == shop)
    items = [(item.item, item.price, item.shop) for item in get_shop_items]
    return items


items = get_item('Brew Lab')
print(items)


inspector = inspect(engine)
table_names = inspector.get_table_names()
table_name = table_names[0] if len(table_names) == 1 else ''
print(table_name)

print(inspector.get_table_names())

session.close()
