from flask import current_app
from datetime import datetime, time
from dateutil.parser import parse
import json
import re

logger = current_app.logger

class RestaurantEntity():
    name = None
    cash_balance = float()
    menu = None
    # `menu` contains a tuple of `Dish` instance
    opening_hours: list = list()

    def __init__(self, item: dict) -> None:
        self.name = item['restaurantName']
        self.cash_balance = item['cashBalance']
        self.menu = self.__menu(item['menu'])
        self.__opening_hours(item['openingHours'])
        print(self)

    def __menu(self, items: list) -> tuple:
        return (Dish(i['dishName'], i['price']) for i in items)

    def __opening_hours(self, item: str):
        """Returns a tuple of `Opening` instances
        """
        for i in (i.strip() for i in item.split(' / ')):
            j = (j for j in re.split(r'(?<=\w)\s+(?=\d)', i, maxsplit=2))
            day_of_week_str = next(j)
            time_range = next(j)
            days = self.__day_of_week(day_of_week_str)
            # print(f'day_of_week_str: {day_of_week_str}')
            # print(f'time_range: {time_range}')
            # print(f'days: {days}')
            self.opening_hours += [Opening(k, time_range) for k in days]

    def __day_of_week(self, item: str) -> tuple:
        """parse the string into a set of numbers which
        each denotes to a specific day of week.

        Pattern could be one of these:
            Mon, Fri
            Mon-Thu
            Thurs
            Sat
            Sun
            Sat - Sun (6 - 0)*
            Sun - Mon (0 - 1)

        Beware of ranges involve Sun(0)            
        """
        # sun(0), mon(1), tue(2), ..., sat(6) 
        days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

        def one_word_to_one_num(item: str) -> int:
            for i in days:
                if i in item.lower():
                    return days.index(i)

            logger.error(f'item {item} no match to days!')
            raise Exception('no match to days!')                    

        # TODO: to be removed
        # # FIXME: hard code to be removed
        # logger.debug('HARD CODE HERE!')
        # item = 'Tue - Sun'

        with_comma = ',' in item
        with_hyphen = '-' in item

        day_indices: tuple = None
        if with_comma:
            day_indices = tuple(one_word_to_one_num(i.strip()) for i in item.split(',', maxsplit=2))
        elif with_hyphen:
            start_and_end = (one_word_to_one_num(i.strip()) for i in item.split('-', maxsplit=2))
            start = next(start_and_end)
            end = next(start_and_end)
            # CAVEAT: handle if end is Sun(0)
            if end == 0:
                day_indices = tuple([i for i in range(start, days.index('sat') + 1)] + [0])
            else:
                day_indices = tuple(i for i in range(start, end + 1))
        else:
            day_indices = (one_word_to_one_num(item.strip()),)
        return day_indices

    def __str__(self) -> str:
        return json.dumps(self.__repr__())

    def __repr__(self) -> str:
        return dict(
            name = self.name,
            cash_balance = self.cash_balance,
            menu = [i.__repr__() for i in self.menu],
            opening_hours = [i.__repr__() for i in self.opening_hours],
        )

class Dish():
    name = None
    price = float()

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return json.dumps(self.__repr__())

    def __repr__(self) -> str:
        return dict(
            name = self.name,
            price = self.price
        )

class Opening():
    """Denotes the opening period of each day
    """
    day_of_week: int = None
    start_str: str = None
    end_str: str = None
    start: time = None
    end: time = None

    def __init__(self, day_of_week: int, time_range: str) -> None:
        logger.debug(f'{day_of_week} => {time_range}')
        self.day_of_week = day_of_week
        self.__str_to_time(time_range)

    def __str_to_time(self, time_range: str):
        """Parse start/end time from string like:
        7:45 am - 10 am
        2:30 pm - 8 pm
        """
        if '-' not in time_range:
            raise Exception(' - should be in it')

        times = (i.strip() for i in time_range.split('-', maxsplit=2))
        self.start_str = next(times)
        self.end_str = next(times)
        self.start = parse(self.start_str).time()
        self.end = parse(self.end_str).time()

    def __str__(self) -> str:
        return json.dumps(self.__repr__())

    def __repr__(self) -> str:
        return dict(
            day_of_week = self.day_of_week,
            start = self.start.__repr__(),
            end = self.end.__repr__()
        )

class CustomerEntity():
    id: int = None
    name: str = None
    cash_balance: float = None
    purchase_history: tuple = None

    def __init__(self, item: dict) -> None:
        self.id = item['id']
        self.name = item['name']
        self.cash_balance = item['cashBalance']
        self.__purchase_history(item['purchaseHistory'])
        
    def __purchase_history(self, actions: list):
        self.purchase_history = tuple(PurchaseHistory(i) for i in actions)

    def __str__(self) -> str:
        return json.dumps(self.__repr__())

    def __repr__(self) -> str:
        return dict(
            id = self.id,
            name = self.name,
            cash_balance = self.cash_balance,
            purchase_history = [i.__repr__() for i in self.purchase_history]
        )


class PurchaseHistory():
    dish_name: str = None
    restaurant_name: str = None
    trans_amount: float = None
    trans_date: datetime = None

    def __init__(self, item: dict) -> None:
        self.dish_name = item['dishName']
        self.restaurant_name = item['restaurantName']
        self.trans_amount = item['transactionAmount']
        self.__trans_date(item['transactionDate'])

    def __trans_date(self, trans_data: str):
        self.trans_date = parse(trans_data)

    def __str__(self) -> str:
        return json.dumps(self.__repr__())
    
    def __repr__(self) -> str:
        return dict(
            dish_name=self.dish_name,
            restaurant_name = self.restaurant_name,
            trans_amount = self.trans_amount,
            trans_date = self.trans_date.__repr__()
        )