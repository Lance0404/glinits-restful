from sqlalchemy import Column
from sqlalchemy import Integer, DateTime, String, Float, Time
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from . import db
# import the SQLAlchemy instance so the models can inherit from it

day_of_week = {
    "Sunday": 1,
    "Monday": 2,
    "Tuesday": 3,
    "Wednesday": 4,
    "Thrusday": 5,
    "Friday": 6,
    "Saturday": 7
}

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    # 1-M relationship
    # replaced `uselist=False` with `lazy='dynamic'`, but not clear what's under the hood
    restaurant_menu = relationship(
        "RestaurantMenu", back_populates="restaurant", foreign_keys='RestaurantMenu.restaurant_id', cascade="all, delete-orphan", passive_deletes=True, lazy='dynamic')
    name = Column(String(100), nullable=False, index=True, unique=True)
    cash_balance = Column(Float, nullable=False)

    def __init__(self, name, cash_balance):
        self.name = name
        self.cash_balance = cash_balance

    def __repr__(self):
        return f'<Restaurant {self.id} {self.name} {self.cash_balance}>'

class RestaurantOpening(db.Model):
    __tablename__ = 'restaurant_opening'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    restaurant = relationship('Restaurant', foreign_keys=restaurant_id, single_parent=True)
    day_of_week = Column(Integer, nullable=False, index=True)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)

    def __init__(self, restaurant_id, day_of_week, start, end):
        self.restaurant_id = restaurant_id
        self.day_of_week = day_of_week
        self.start = start
        self.end = end

    def __repr__(self):
        return f'<RestaurantOpening {self.id} {self.restaurant_id} {self.day_of_week} {self.start} {self.end}>'

class RestaurantMenu(db.Model):
    __tablename__ = 'restaurant_menu'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    restaurant = relationship('Restaurant', foreign_keys=restaurant_id, single_parent=True)
    dish_name = Column(String(500), nullable=False, index=True)
    price = Column(Float, nullable=False)

    def __init__(self, restaurant_id, dish_name, price):
        self.restaurant_id = restaurant_id
        self.dish_name = dish_name
        self.price = price

class Customer(db.Model):
    """Currently don't have relationship with Restaurant-tables
    """
    __tablename__ = 'customer'
	# the `id` came from json
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False, index=True)
    cash_balance = Column(Float, nullable=False)
    customer_history = relationship(
        "CustomerHistory", back_populates="customer", foreign_keys='CustomerHistory.customer_id', cascade="all, delete-orphan", passive_deletes=True, lazy='dynamic')

    def __init__(self, id, name, cash_balance):
        self.id = id
        self.name = name
        self.cash_balance = cash_balance

class CustomerHistory(db.Model):
    __tablename__ = 'customer_history'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), index=True)
    customer = relationship('Customer', foreign_keys=customer_id, single_parent=True)
    dish_name = Column(String(200), nullable=False, index=True)
    restaurant_name = Column(String(100), nullable=False, index=True, unique=True)
    trans_amount = Column(Float, nullable=False)
    trans_date = Column(DateTime(timezone=False), nullable=False)

    def __init__(self, customer_id, dish_name, restaurant_name, trans_amount, trans_date):
        self.customer_id = customer_id
        self.dish_name = dish_name
        self.restaurant_name = restaurant_name
        self.trans_amount = trans_amount
        self.trans_date = trans_date