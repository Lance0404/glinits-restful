from flask import current_app
from datetime import datetime, time
from sqlalchemy import select

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
        [db.session.add(RestaurantOpening(resta.id, opening.day_of_week, opening.start, opening.end)) for opening in data.opening_hours]
        commit()

    @classmethod
    def list_restaurant_by(cls, t: time):
        # FIXME: should intake datetime which carries day of week information
        logger.debug(f'start list_restaurant_by({time})')
        stmt = (select(RestaurantOpening)
            .where(RestaurantOpening.start < t)
            .where(RestaurantOpening.end > t))
        logger.debug(f'stmt: {stmt}')
        result = db.session.execute(stmt)
        resta_openings = result.fetchall()
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

