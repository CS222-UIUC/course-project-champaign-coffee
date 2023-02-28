#Reference: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import csv

engine = create_engine('sqlite:///champaign_menu.db', echo=True)

Base = declarative_base()

# SQL Coffee Data Object by Id, Item, Price, and Shop
class CoffeeData(Base):
    __tablename__ = 'menu_item',
    id = Column(Integer, primary_key=True)
    item = Column(String)
    price = Column(String) # should change to float but gives parsing error
    shop = Column(String)

Base.metadata.create_all(engine)  

Session = sessionmaker(bind=engine)
session = Session()

# Parse CSV file for database
with open('coffee_data/champaign_coffee_menus.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        item, price, shop = row
        menu_item = CoffeeData(item=item, price=price, shop=shop)
        session.add(menu_item)

# Prints all the entries to terminal as sanity check
# result = session.query(CoffeeData)
# for row in result:
  #  print ("Item:",row.item, ", Price:", row.price, ", Coffee Shop:", row.shop)

# Returns all the items from brewlab
brew_lab_items = session.query(CoffeeData).filter(CoffeeData.shop == 'Brew Lab').all()
for item in brew_lab_items:
    print(item.item, item.price, item.shop)

# Finds and returns all items under $2.00 in Espresso Royale
espresso_royale_items = session.query(CoffeeData).filter(CoffeeData.price < 2.0).filter(CoffeeData.shop == 'Espresso Royale').all()
for item in espresso_royale_items:
    print(item.item, item.price, item.shop)





