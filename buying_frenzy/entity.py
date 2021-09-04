from typing import Generator
from flask import current_app
from datetime import datetime, time
from dateutil.parser import parse
import json
import re

class RestaurantEntity():
    name = None
    cash_balance = float()
    menu: list = list()
    opening_hours: list = list()

    def __init__(self, item: dict) -> None:
        self.name = item['restaurantName']
        self.cash_balance = item['cashBalance']
        self.__menu(item['menu'])
        self.__opening_hours(item['openingHours'])

    def __menu(self, items: list):
        self.menu = [Dish(i['dishName'], i['price']) for i in items]

    def __opening_hours(self, item: str):
        # initialize with empty list
        self.opening_hours = list()
        for i in (i.strip() for i in item.split(' / ')):
            j = (j for j in re.split(r'(?<=\w)\s+(?=\d)', i, maxsplit=2))
            weekday = next(j)
            time_range = next(j)
            days = self.__weekday(weekday)
            # print(f'weekday: {weekday}')
            # print(f'time_range: {time_range}')
            # print(f'days: {days}')
            for k in days:
                time_range_split = self.__time_range(time_range)
                if len(time_range_split) == 2:
                    next_k = k + 1 if k < 6 else 0
                    self.opening_hours += [Opening(k, time_range_split[0])]
                    self.opening_hours += [Opening(next_k, time_range_split[1])]
                else:
                    self.opening_hours += [Opening(k, time_range)]

    # FIXME: could be optimized by refactoring 
    def __time_range(self, time_range: str) -> tuple[str]:
        """(Patch) Special care on start > end cases, which denotes to a cross day time range
        e.g. 
        4:15 pm - 3:15 am
        5:00 am - 4:00 am

        >>> parse('11:59:59.999999 pm').time() > parse('16:15:00').time()
        True
        """
        # current_app.logger.debug('start __time_range()...')
        time_range_split: tuple = (time_range,)
        times = tuple(i.strip() for i in time_range.split('-', maxsplit=2))
        (start, end) = times
        if parse(start).time() > parse(end).time() and parse(end).time() != parse('12 am').time():
            time_range_split = (f'{start} - 11:59:59.999999 pm', f'12:00 am - {end}')
            # current_app.logger.debug(f'[{self.name}] {time_range_split}')
        return time_range_split

    def __weekday(self, item: str) -> tuple[int]:
        """parse the string into a set of numbers which
        each denotes to a specific day of week.

        # FIXME: align the with the weekday indices of package `datetime`

        Pattern could be one of these:
            Mon, Fri
            Mon-Thu
            Thurs
            Sat
            Sun
            Sat - Sun (5 - 6)
            Sun - Mon (6 - 0)*

        *requires special handle          
        """
        weekdays = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',)

        def one_word_to_one_num(item: str) -> int:
            for i in weekdays:
                if i in item.lower():
                    return weekdays.index(i)

            current_app.logger.error(f'item {item} no match to weekdays!')
            raise Exception('no match to weekdays!')                    

        with_comma = ',' in item
        with_hyphen = '-' in item

        day_indices: tuple = None
        if with_comma:
            day_indices = tuple(one_word_to_one_num(i.strip()) for i in item.split(',', maxsplit=2))
        elif with_hyphen:
            start_and_end = (one_word_to_one_num(i.strip()) for i in item.split('-', maxsplit=2))
            start = next(start_and_end)
            end = next(start_and_end)
            # CAVEAT: handle Sun - Mon (6 - 0) or Sat - Mon (5 - 0) cases
            if end == 0:
                day_indices = tuple([i for i in range(start, len(weekdays))] + [0])
                # current_app.logger.debug(f'name {self.name}, day_indices {day_indices}')
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
    """Redesign required!
    
    Denotes the opening period of each `representative` day

    This:
    Tues 4:15 pm - 3:15 am / Weds 1:15 pm - 6 pm

    Should denote to:
    - Tues 16:15 - 24:00
    - Weds 24:00 - 3:15
    - Weds 13:15 - 18:00

    Just found data of this kind: 
    "openingHours": "Mon 10 am - 5:30 pm / Tues 4:15 pm - 3:15 am / Weds 1:15 pm - 6 pm / Thurs 9 am - 2:45 am / Fri - Sat 12:15 pm - 12:30 am / Sun 11:30 am - 6 pm",
    "restaurantName": "Zinc Restaurant"  

    """
    weekday: int = None
    start_str: str = None
    end_str: str = None
    start: time = None
    end: time = None

    def __init__(self, weekday: int, time_range: str) -> None:
        # current_app.logger.debug(f'{weekday} => {time_range}')
        self.weekday = weekday
        self.__str_to_time(time_range)

    def __str_to_time(self, time_range: str):
        """Parse start/end time from string like:
        7:45 am - 10 am
        2:30 pm - 8 pm
        4:15 pm - 3:15 am*

        *should be split into two records, each under different weekdays 
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
            weekday = self.weekday,
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
        # FIXME: for legacy
        if item.get('purchaseHistory', None):
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