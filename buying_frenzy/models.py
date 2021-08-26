import enum
from sqlalchemy import func, Index, Column
from sqlalchemy import Integer, Enum, DateTime, String, Float
from sqlalchemy.sql.schema import ForeignKey

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
    name = Column(String(100), nullable=False, index=True, unique=True)
    cash_balance = Column(Float, nullable=False)

    def __repr__(self):
        return f'{self.name}'

class RestaurantOpening(db.Model):
    __tablename__ = 'restaurant_opening'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    start = Column(DateTime(timezone=False), nullable=False)
    end = Column(DateTime(timezone=False), nullable=False)
    day_of_week = Column(Integer, nullable=False, index=True)

    def __repr__(self):
        return f'{self.id}'

class RestaurantMenu(db.Model):
    __tablename__ = 'restaurant_menu'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    dish_name = Column(String(200), nullable=False, index=True)
    price = Column(Float, nullable=False)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=False)
    # `id` came from json
    name = Column(String(100), nullable=False, index=True, unique=True)
    cash_balance = Column(Float, nullable=False)

class CustomerHistory(db.Model):
    __tablename__ = 'customer_history'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), index=True)
    dish_name = Column(String(200), nullable=False, index=True)
    restaurant_name = Column(String(100), nullable=False, index=True, unique=True)
    transaction_amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime(timezone=False), nullable=False)