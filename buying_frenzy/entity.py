# transformers that do the ugly work
import json

class Restaurant():
    name = None
    cash_balance = float()
    menu = None
    opening_hours = None

    def __init__(self, item: dict) -> None:
        self.name = item['restaurantName']
        self.cash_balance = item['cashBalance']
        self.menu = self.__menu(item['menu'])
        self.opening_hours = item['openingHours']

    def __menu(self, items: list) -> tuple:
        return (Dish(i['dishName'], i['price']) for i in items)

    def __str__(self) -> str:
        return json.dumps(dict(
            name = self.name,
            cash_balance = self.cash_balance,
            menu = [i.__repr__() for i in self.menu],
            opening_hours = self.opening_hours,
        ))

    def __repr__(self) -> str:
        return self.__str__()

class Dish():
    name = None
    price = float()

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return json.dumps(dict(
            name = self.name,
            price = self.price
        ))

    def __repr__(self) -> str:
        return dict(
            name = self.name,
            price = self.price
        )
