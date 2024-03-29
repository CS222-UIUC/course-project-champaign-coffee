"""Reference: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm"""
import csv
import logging
import pandas
from sqlalchemy import create_engine, Column, Integer, String, inspect,  MetaData, Float, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy.ext.declarative import declarative_base

# structure:
# coffee shop table (id, name, location, *ratings)
# items table (id, name)
# sell (coffee shop id, item id (from items table), price)
# primary and foreign keys


# drink_type, price, flavor, location, ratings, proximity

# string matches to a drink type
def identify_drink_type(item_name):
    drink_types = ["Other", "Tea", "Latte", "Mocha", "Espresso",
                   "Americano", "Cappuccino", "Macchiato", "Frappe"]
    item_name_lower = item_name.lower()

    for drink_type in drink_types[1:]:  # Skip the "Other"
        if drink_type.lower() in item_name_lower:
            return drink_type
    return drink_types[0]


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
    proximity = Column(Float, default=1.0)

   #  def __init__(self, name, location, ratings=0.0, ratings_count=0):
   #      self.name = name
   #      self.location = location
   #      self.ratings = ratings
   #      self.ratings_count = ratings_count
   #      self.display_name = ' '.join([s.capitalize()
   #                                   for s in self.name.split('-')])
    def update_ratings(self, new_rating):
        """Updates the coffee shop's ratings and ratings_count based on a new rating"""
        self.ratings = (self.ratings * self.ratings_count +
                        new_rating) / (self.ratings_count + 1)
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


# algo tabler
class ExtendedCoffeeData(Base):
    __tablename__ = 'extended_coffee_data'
    id = Column(Integer, primary_key=True)
    coffee_shop_id = Column(Integer, ForeignKey('coffee_shop.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    drink_type = Column(String)  # <<<
    price = Column(Float)
    flavor = Column(String)
    location = Column(String)
   #  ratings = Column(Float)
    proximity = Column(Integer, ForeignKey('coffee_shop.proximity'))
    coffee_shop = relationship(
        CoffeeShop, backref='extended_items', foreign_keys=[coffee_shop_id])
    item = relationship(Item)

    @property
    def ratings(self):
        return self.coffee_shop.ratings





def calculate_coffee_data_value(drink_type, price, flavor, location, ratings, proximity):
   #  drink_type_weight = 1.0
   #  price_weight = 1.0
   #  flavor_weight = 1.0
   #  location_weight = 1.0
   #  ratings_weight = 1.0
   #  proximity_weight = 1.0

    normalized_drink_type = algo_for_drink_type(drink_type)
    normalized_price = algo_for_price(price)
    normalized_flavor = algo_for_flavor(flavor)
    normalized_location = algo_for_location(location)
    normalized_ratings = algo_for_ratings(ratings)
    normalized_proximity = algo_for_proximity(proximity)

    drink_type_value = drink_type_weight * normalized_drink_type
    price_value = price_weight * normalized_price
    flavor_value = flavor_weight * normalized_flavor
    location_value = location_weight * normalized_location
    ratings_value = ratings_weight * normalized_ratings
    proximity_value = proximity_weight * normalized_proximity

    # Calculate the overall data value for the coffee entry
    coffee_entry_value = (
        drink_type_value +
        price_value +
        flavor_value +
        location_value +
        ratings_value +
        proximity_value
    )

    return coffee_entry_value


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
                coffee_shop = CoffeeShop(
                    name=csv_shop, location=csv_location, ratings=0.0)
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
            # table for algo
            drink_type = identify_drink_type(csv_item)
            flavor = ''
            proximity = 1.0
            # ratings = 0.0
            extended_coffee_data = ExtendedCoffeeData(
                coffee_shop=coffee_shop, item=item, drink_type=drink_type, price=float(
                    csv_price.strip('$')),
                flavor=flavor, location=csv_location, proximity=coffee_shop.proximity)
            session.add(extended_coffee_data)
session.commit()

# hello eyad look here
# Return closest priced coffee drink


# def find_closest_price_coffee(user_desired_price):
#     coffee_data_query = session.query(CoffeeData).options(
#         joinedload(CoffeeData.coffee_shop), joinedload(CoffeeData.item))

#     closest_price_difference = None
#     closest_coffee_data = None

#     for coffee_data in coffee_data_query:
#         price_difference = abs(coffee_data.price - user_desired_price)
#         if closest_price_difference is None or price_difference < closest_price_difference:
#             closest_price_difference = price_difference
#             closest_coffee_data = coffee_data

#     if closest_coffee_data:
#         return {
#             'coffee_shop': closest_coffee_data.coffee_shop.name,
#             'item': closest_coffee_data.item.name,
#             'price': closest_coffee_data.price,
#             'location': closest_coffee_data.coffee_shop.location
#         }
#     else:
#         return None


def recommended_coffee(min_price, max_price, rating_importance, proximity_importance, coffee_type):
    # proximity importance and rating importance are on a scale from 0 to 2 inclusive, 2 being most important
    extended_coffee_data_query = session.query(ExtendedCoffeeData).options(
        joinedload(ExtendedCoffeeData.coffee_shop), joinedload(ExtendedCoffeeData.item))

    closest_coffee_data = None
    closest_price = max_price
    closest_coffee_data_prox = None
    closest_price_prox = max_price
    closest_coffee_data_rat = None
    closest_price_rat = max_price
# finds coffee that's within price range such that it matches coffee type and has lowest price among those possibilities
    for coffee_data in extended_coffee_data_query:
        if coffee_data.price >= min_price and coffee_data.price <= max_price and coffee_data.drink_type == coffee_type:
            if coffee_data.price < closest_price:
                closest_coffee_data = coffee_data
                closest_price = coffee_data.price
#  same thing as above but with the added constraint that it has a rating of 4 or 5
    for coffee_data in extended_coffee_data_query:
        if coffee_data.price >= min_price and coffee_data.price <= max_price and coffee_data.drink_type == coffee_type and (coffee_data.ratings == 4 or coffee_data.ratings == 5):
            if coffee_data.price < closest_price_rat:
                closest_coffee_data_rat = coffee_data
                closest_price_rat = coffee_data.price
 # same thing as above but instead of rating constraint, constraint that it's in proximity to campus (proximity is 1 not 0)
    for coffee_data in extended_coffee_data_query:
        if coffee_data.price >= min_price and coffee_data.price <= max_price and coffee_data.drink_type == coffee_type and coffee_data.proximity == 1:
            if coffee_data.price < closest_price_prox:
                closest_coffee_data_prox = coffee_data
                closest_price_prox = coffee_data.price
# if proximity importance is greater than rating importance, we prioritze that in returning result
    if proximity_importance > rating_importance:
        return {
            'coffee_shop': closest_coffee_data_prox.coffee_shop.name,
            'item': closest_coffee_data_prox.item.name,
            'price': closest_coffee_data_prox.price,
            'location': closest_coffee_data_prox.coffee_shop.location
        }
# if rating importance is greater, we prioritize that instead
    if rating_importance > proximity_importance:
        return {
            'coffee_shop': closest_coffee_data_rat.coffee_shop.name,
            'item': closest_coffee_data_rat.item.name,
            'price': closest_coffee_data_rat.price,
            'location': closest_coffee_data_rat.coffee_shop.location
        }
# otherwise they must be equal, if greaer than 0 we know it still matters, so we choose the one that yields lower price between the two
    if rating_importance > 0:
        if closest_price_rat < closest_price_prox:
            return {
                'coffee_shop': closest_coffee_data_rat.coffee_shop.name,
                'item': closest_coffee_data_rat.item.name,
                'price': closest_coffee_data_rat.price,
                'location': closest_coffee_data_rat.coffee_shop.location
            }
        else:
            return {
                'coffee_shop': closest_coffee_data_prox.coffee_shop.name,
                'item': closest_coffee_data_prox.item.name,
                'price': closest_coffee_data_prox.price,
                'location': closest_coffee_data_prox.coffee_shop.location
            }
    # otherwise, they are both 0 in importance so we simply choose lowest price coffee
    if closest_coffee_data:
        return {
            'coffee_shop': closest_coffee_data.coffee_shop.name,
            'item': closest_coffee_data.item.name,
            'price': closest_coffee_data.price,
            'location': closest_coffee_data.coffee_shop.location
        }
    else:
        return None


# test
min_price = 1
max_price = 4
rating_importance = 0
proximity_importance = 0
coffee_type = "Latte"
closest_coffee = recommended_coffee(
    min_price, max_price, rating_importance, proximity_importance, coffee_type)
print(closest_coffee)
