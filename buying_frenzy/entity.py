# transformers that do the ugly work
from datetime import datetime, time
from dateutil.parser import parse
import json
import re


from .factory import app

logger = app.logger

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
        # self.opening_hours = self.__opening_hours(item['openingHours'])
        self.__opening_hours(item['openingHours'])
        print(f'self.opening_hours {self.opening_hours}')
        # raise Exception('Lance Checkpoint!')

    def __menu(self, items: list) -> tuple:
        return (Dish(i['dishName'], i['price']) for i in items)

    def __opening_hours(self, item: str) -> list:
        """Returns a tuple of `Opening` instances
        """
        for i in (i.strip() for i in item.split(' / ')):
            j = (j for j in re.split(r'(?<=\w)\s+(?=\d)', i, maxsplit=2))
            day_of_week_str = next(j)
            time_range = next(j)
            # print(f'day_of_week_str: {day_of_week_str}')
            # print(f'time_range: {time_range}')
            days = self.__day_of_week(day_of_week_str)
            # print(f'days {days}')
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
            opening_hours = self.opening_hours,
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
        return json.dumps(dict(
            day_of_week = self.day_of_week,
            start = self.start.__repr__(),
            end = self.end.__repr__()
        ))