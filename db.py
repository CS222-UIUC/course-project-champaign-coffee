"""Reference: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm"""
import csv
import logging
import pandas
from sqlalchemy import create_engine, Column, Integer, String, inspect,  MetaData, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# structure:
# coffee shop table (id, name, location, *ratings)
# items table (id, name)
# sell (coffee shop id, item id (from items table), price)
# primary and foreign keys


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
engine = create_engine('sqlite:///champaign_menu.db',
                       echo=False, connect_args={'check_same_thread': False, 'timeout': 1})
	# adding timeout to verify that timeout is not the cause of errors
Base = declarative_base()
meta = MetaData()
conn = engine.connect()


class CoffeeShop(Base):
    """SQL Coffee Shop Object by Id, Name, and Location"""
    __tablename__ = 'coffee_shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
   #  display_name = Column(String)
    ratings = Column(Float, default=0.0)
    ratings_count = Column(Integer, default=0)

   #  def __init__(self, name, location, ratings=0.0, ratings_count=0):
   #      self.name = name
   #      self.location = location
   #      self.ratings = ratings
   #      self.ratings_count = ratings_count
   #      self.display_name = ' '.join([s.capitalize()
   #                                   for s in self.name.split('-')])
    def update_ratings(self, new_rating):
        """Updates the coffee shop's ratings and ratings_count based on a new rating"""
        self.ratings = (self.ratings * self.ratings_count + new_rating) / (self.ratings_count + 1)
        self.ratings_count += 1
      #   session.add(self)
      #   session.commit()


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
    coffee_shop = relationship(CoffeeShop, backref='items')
    item = relationship(Item)


class UserFeedback(Base):
    """SQL User Feedback Object by Id, CoffeeShop, Rating, and Feedback"""
    __tablename__ = 'user_feedback'
    id = Column(Integer, primary_key=True)
    coffee_shop_id = Column(Integer, ForeignKey('coffee_shop.id'))
    rating = Column(Integer)
    feedback = Column(String)
    coffee_shop = relationship(CoffeeShop, backref='feedbacks')


class SiteFeedback(Base):
    """SQL Site Feedback Object by Id, Rating, and Feedback"""
    __tablename__ = 'site_feedback'
    id = Column(Integer, primary_key=True)
    feedback = Column(String)

    def __init__(self, feedback):
        self.feedback = feedback


Base.metadata.create_all(engine)
SiteFeedback.__table__.create(bind=engine, checkfirst=True)


Session = sessionmaker(bind=engine)
session = Session()

# Parse CSV file for database
with open('coffee_data/champaign_coffee_menus.csv', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip first line
    for row in reader:
        csv_item, csv_price, csv_location, csv_shop = row
        if csv_price:  # skip any empty str's
            coffee_shop = session.query(CoffeeShop).filter(
                CoffeeShop.name == csv_shop).first()
            if not coffee_shop:
                # initialize location attribute with csv_location
                coffee_shop = CoffeeShop(name=csv_shop, location=csv_location, ratings=0.0)
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
                # if exists, update its price & ratings instead of inserting a new row
                existing_coffee_data.price = float(csv_price.strip('$'))
            else:
                # create a new CoffeeData object with the foreign keys to CoffeeShop and Item
                coffee_data = CoffeeData(
                    coffee_shop=coffee_shop, item=item, price=float(csv_price.strip('$')))
                session.add(coffee_data)
session.commit()
