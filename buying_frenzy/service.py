from flask import current_app
from datetime import datetime, time
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .entity import RestaurantEntity, CustomerEntity
from .model import (
    Restaurant, RestaurantOpening, RestaurantMenu,
    Customer, CustomerHistory,
)
from . import db

logger = current_app.logger

def commit():
    """
    DRY the try-except around `db.session.commit()`
    """
    try:
        db.session.commit()
    except Exception as e:
        logger.error(e)
        raise e

class RestaurantService():

    def __init__(self) -> None:
        pass

    @classmethod
    def create(cls, data: RestaurantEntity):
        resta = Restaurant(data.name, data.cash_balance)
        db.session.add(resta)
        commit()

        db.session.flush()
        # https://www.codegrepper.com/code-examples/sql/sqlalchemy+return+id+after+insert
        # get the id of the just inserted record
        # `flush()` is necessary for returning the id created on the database to the `Restaurant` instance

        # TODO: using list comprehension, cause I failed with generator comprehension
        # logger.debug(f'preparing to insert {RestaurantMenu.__tablename__}')
        [db.session.add(RestaurantMenu(resta.id, i.name, i.price)) for i in data.menu]
        # logger.debug(f'preparing to insert {RestaurantOpening.__tablename__}')
        [db.session.add(RestaurantOpening(resta.id, opening.weekday, opening.start, opening.end)) for opening in data.opening_hours]
        commit()

    @classmethod
    def list_available_restaurant_by(cls, dt: datetime):
        # FIXME: should intake datetime which carries day of week information
        logger.debug(f'start list_available_restaurant_by({dt})')
        logger.debug(f'weekday {dt.weekday()}, time {dt.time()}')
        # FIXME: method 1:
        # stmt = (select(RestaurantOpening.restaurant)
        #     .where(RestaurantOpening.weekday == dt.weekday())
        #     .where(RestaurantOpening.start < dt.time())
        #     .where(RestaurantOpening.end > dt.time()))
        # """SELECT restaurant_opening.id, restaurant_opening.restaurant_id, restaurant_opening.weekday, restaurant_opening.start, restaurant_opening."end" 
        # FROM restaurant_opening 
        # WHERE restaurant_opening.weekday = :weekday_1 AND restaurant_opening.start < :start_1 AND restaurant_opening."end" > :end_1

        # SELECT restaurant.id = restaurant_opening.restaurant_id AS restaurant 
        # FROM restaurant, restaurant_opening 
        # WHERE restaurant_opening.weekday = :weekday_1 AND restaurant_opening.start < :start_1 AND restaurant_opening."end" > :end_1
        # """    
        # logger.debug(f'stmt: {stmt}')
        # result = db.session.execute(stmt)
        # resta_openings = result.fetchall()

        # method 2:
        restaurants = (db.session.query(RestaurantOpening)
            .join(RestaurantOpening.restaurant)
            .options(joinedload(RestaurantOpening.restaurant))
            .filter(RestaurantOpening.weekday == dt.weekday())
            .filter(RestaurantOpening.start < dt.time())
            .filter(RestaurantOpening.end > dt.time())
        )
        """SELECT restaurant_opening.id AS restaurant_opening_id, restaurant_opening.restaurant_id AS restaurant_opening_restaurant_id, restaurant_opening.weekday AS restaurant_opening_weekday, restaurant_opening.start AS restaurant_opening_start, restaurant_opening."end" AS restaurant_opening_end, restaurant_1.id AS restaurant_1_id, restaurant_1.name AS restaurant_1_name, restaurant_1.cash_balance AS restaurant_1_cash_balance 
        FROM restaurant_opening JOIN restaurant ON restaurant.id = restaurant_opening.restaurant_id LEFT OUTER JOIN restaurant AS restaurant_1 ON restaurant_1.id = restaurant_opening.restaurant_id 
        WHERE restaurant_opening.weekday = %(weekday_1)s AND restaurant_opening.start < %(start_1)s AND restaurant_opening."end" > %(end_1)s
        """
        restaurants.all()
        breakpoint()

class CustomerService():

    def __init__(self) -> None:
        pass

    @classmethod
    def create(cls, customer_entity: CustomerEntity):
        customer = Customer(customer_entity.id, customer_entity.name, customer_entity.cash_balance)
        db.session.add(customer)
        # FIXME: legacy code
        if customer_entity.purchase_history:
            [db.session.add(CustomerHistory(customer_entity.id, i.dish_name, i.restaurant_name, i.trans_amount, i.trans_date)) for i in customer_entity.purchase_history]
        commit()

