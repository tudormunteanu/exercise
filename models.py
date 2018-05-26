from datetime import datetime
from random import randrange
import json

class Order:


    def __init__(self, price, size):
        self.price = price
        self.date = datetime.utcnow()
        self.size = size
        self.id = randrange(1000)

    def __repr__(self):
        return "{} - {}".format(self.price, self.date)


class BuyOrder(Order):
    pass


class SellOrder(Order):
    pass


class Orderbook:


    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        self.buy_orders.append(order)

    def aggregate(self, orders):
        pass

    def render(self):
        pass

    def get_all_orders(self):
        return self.buy_orders + self.sell_orders

    def clear(self):
        self.buy_orders = []


class Storage:


    def __init__(self):
        self.orderbook = Orderbook()
