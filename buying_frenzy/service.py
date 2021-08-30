from typing import Generator
from flask import current_app
from datetime import datetime, time
from sqlalchemy import select, func
from sqlalchemy.sql.expression import label
from sqlalchemy.orm import joinedload, load_only

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
    def list_available_restaurant_by(cls, dt: datetime) -> Generator:
        # FIXME: should intake datetime which carries day of week information
        logger.debug(f'start list_available_restaurant_by({dt})')
        logger.debug(f'weekday {dt.weekday()}, time {dt.time()}')

        # method 1: [ref](https://stackoverflow.com/a/39553869)
        stmt = (db.session.query(Restaurant.name)
            .select_from(RestaurantOpening)
            .join(RestaurantOpening.restaurant)
            .filter(RestaurantOpening.weekday == dt.weekday())
            .filter(RestaurantOpening.start <= dt.time())
            .filter(RestaurantOpening.end >= dt.time())            
        )
        logger.debug(stmt)
        """
        SELECT restaurant.name AS restaurant_name 
        FROM restaurant_opening JOIN restaurant ON restaurant.id = restaurant_opening.restaurant_id 
        WHERE restaurant_opening.weekday = %(weekday_1)s AND restaurant_opening.start < %(start_1)s AND restaurant_opening."end" > %(end_1)s
        """
        
        restaurants = stmt.all()
        """
        "openingHours": "Mon 10 am - 5:30 pm / Tues 4:15 pm - 3:15 am / Weds 1:15 pm - 6 pm / Thurs 9 am - 2:45 am / Fri - Sat 12:15 pm - 12:30 am / Sun 11:30 am - 6 pm",
        "restaurantName": "Zinc Restaurant"

        select * from restaurant where name = 'Zinc Restaurant';

        select * from restaurant_opening where restaurant_id = 2182;  

        >>> from dateutil.parser import parse
        >>> parse('00:00:00').time() > parse('16:15:00').time()
        False

        >>> parse('11:59:59.999999 pm').time() > parse('16:15:00').time()
        True

        >>> parse('04/10/2020 03:14 AM').time()
        """
        return (i[0] for i in restaurants)

        """
        # might be useful someday
        method 2: joinedload(), load_only()
        stmt = (db.session.query(RestaurantOpening)
            .join(RestaurantOpening.restaurant)
            .filter(RestaurantOpening.weekday == dt.weekday())
            .filter(RestaurantOpening.start < dt.time())
            .filter(RestaurantOpening.end > dt.time())
            .options(joinedload(RestaurantOpening.restaurant))
            # .options(load_only(Restaurant.name))
        )
        print(stmt)

        method 3: db.session.execute()
        stmt = (select(RestaurantOpening.restaurant)
            .where(RestaurantOpening.weekday == dt.weekday())
            .where(RestaurantOpening.start < dt.time())
            .where(RestaurantOpening.end > dt.time()))
        logger.debug(f'stmt: {stmt}')
        result = db.session.execute(stmt).fetchall()
        """

    @classmethod
    def list_by_dish_count_and_price_range(cls, restaurant_count: int, action: str, dish_count: int, **kwargs) -> Generator:
        """Objective: 
        1. filter by price range
        2. filter by more or less of the dish count
        3. limit with top restaurant count 

        Currently ordered by dish count in desc

        Target SQL:

SELECT b.name, count(a.id) counts
FROM public.restaurant_menu a
JOIN restaurant b ON a.restaurant_id = b.id 
WHERE a.price <= 20 AND a.price >= 15 
GROUP BY b.name 
HAVING count(a.id) >= 2
ORDER BY counts DESC, b.name ASC

        [ref](https://stackoverflow.com/a/4086229)
        session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()
        """
        logger.info('start list_by_dish_count_and_price_range()...')
        count_ = func.count(RestaurantMenu.id)
        stmt = (db.session.query(Restaurant.name, count_)
            .select_from(RestaurantMenu)
            .join(RestaurantMenu.restaurant)
            .filter(RestaurantMenu.price <= kwargs['max'])
            .filter(RestaurantMenu.price >= kwargs['min'])
            .group_by(Restaurant.name)
        )
        # [lifesaver](https://stackoverflow.com/a/34829004)
        stmt = (stmt.having(count_ >= dish_count) if action == 'more' 
            else stmt.having(count_ <= dish_count))
        stmt = stmt.order_by(count_.desc()).limit(restaurant_count)
        # logger.debug(stmt)
        """
SELECT restaurant.name AS restaurant_name, count(restaurant_menu.id) AS count 
FROM restaurant_menu JOIN restaurant ON restaurant.id = restaurant_menu.restaurant_id 
WHERE restaurant_menu.price <= %(price_1)s AND restaurant_menu.price >= %(price_2)s GROUP BY restaurant.name 
HAVING count(restaurant_menu.id) <= %(count_1)s ORDER BY count(restaurant_menu.id) DESC
        """
        result = stmt.all()
        return (i for i in result)
        
    @classmethod
    def search_by_type_and_term(cls, term: str) -> Generator:
        logger.info(f'start search_by_type_and_term({term})...')
        stmt = (db.session.query(Restaurant.name, Restaurant.id)
            .select_from(Restaurant)
            .filter(Restaurant.name.ilike(f'%{term}%'))
            .order_by(Restaurant.name)
        )
        logger.debug(stmt)
        """
SELECT restaurant.name AS restaurant_name 
FROM restaurant, restaurant_menu 
WHERE restaurant_menu.price LIKE %(price_1)s    
        """
        result = stmt.all()
        return (i for i in result)


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

    @classmethod
    def search_by_type_and_term(cls, term: str):
        logger.info(f'start search_by_type_and_term({term})...')
        stmt = (db.session.query(RestaurantMenu.dish_name, RestaurantMenu.id)
            .select_from(RestaurantMenu)
            .filter(RestaurantMenu.dish_name.ilike(f'%{term}%'))
            .order_by(RestaurantMenu.dish_name)
        )
        logger.debug(stmt)
        """
SELECT customer.name AS customer_name 
FROM customer 
WHERE customer.name LIKE %(name_1)s ORDER BY customer.name   
        """
        result = stmt.all()
        return (i for i in result)

    @classmethod
    def buy(cls, user_id: int, restaurant_id: int, dish_id: int):
        """
        Sequence 
        1. query dish price from `RestaurantMenu`
        2. deduct customer's cashBalance
        3. add to restaurant's cashBalance
        """
        logger.info(f'start {cls.__name__}.buy()...')
        
