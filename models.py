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
        return "{}: {} @ {} ({})".format(self.id, self.size, self.price, self.date)

    def __eq__(self, other):
        return self.id == other.id


class BuyOrder(Order):
    pass


class SellOrder(Order):
    pass


class Orderbook:


    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if isinstance(order, BuyOrder):
            self._insert_order_sorted(self.buy_orders, order)
        elif isinstance(order, SellOrder):
            self._insert_order_sorted(self.sell_orders, order)
        else:
            raise Exception("Wrong error type")

    def add_orders(self, orders):
        for o in orders:
            self.add_order(o)

    def aggregate(self):
        aggregated_buy_orders = self._agregate_orders(self.buy_orders)
        aggregated_sell_orders = self._agregate_orders(self.sell_orders)
        output = {
            "buy": aggregated_buy_orders,
            "sell": aggregated_sell_orders,
        }
        return output

    def _insert_order_sorted(self, orders, order):
        if not orders:
            orders.append(order)
        else:
            # Omit the -1, because the len will become len + 1
            # with the new Order that will be added.
            index = len(orders)
            for i, v in enumerate(orders):
                if order.price < v.price:
                    index = i - 1
            orders.insert(index, order)

    def _agregate_orders(self, orders):
        aggregated_orders = []
        for order in orders:
            found = False
            for aggregated_order in aggregated_orders:
                if aggregated_order["price"] == order.price:
                    aggregated_order["size"] += order.size
                    found = True
            if not found:
                aggregated_orders.append({
                    "price": order.price,
                    "size": order.size
                })     
        return aggregated_orders 

    def get_all_orders(self):
        return self.buy_orders + self.sell_orders

    def clear(self):
        self.buy_orders.clear()
        self.sell_orders.clear()


class Storage:


    def __init__(self):
        self.orderbook = Orderbook()
