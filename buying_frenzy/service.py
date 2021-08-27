"""
contains functions that directly interacts with database
"""
from .entity import Restaurant as RestaurantEntity
from .model import Restaurant
from . import db

class RestaurantService():

    def __init__(self) -> None:
        pass
    
    @classmethod
    def create(cls, data: RestaurantEntity):
        re = Restaurant(data.name, data.cash_balance)
        db.session.add(re)
        db.session.commit()

