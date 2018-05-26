from exchange import create_order, get_order, get_orderbook
from exchange import storage
from models import SellOrder, BuyOrder, Storage
import unittest
import json
import mock


class TestExchange(unittest.TestCase):


    def setUp(self):
        self.storage = storage
        self.orderbook = storage.orderbook

    def tearDown(self):
        self.storage.orderbook.clear()

    def test_create_order_sell(self):
        data = {
            "price": 20,
            "size": 100,
            "type": "sell",
        }
        res = create_order(data)
        self.assertIn("order_id", res)
        self.assertEqual(len(self.orderbook.buy_orders), 1)
        self.assertIsInstance(self.orderbook.buy_orders[0], SellOrder)

    def test_create_order_buy(self):
        data = {
            "price": 20,
            "size": 100,
            "type": "buy",
        }
        res = create_order(data)
        self.assertIn("order_id", res)
        self.assertEqual(len(self.orderbook.buy_orders), 1)
        self.assertIsInstance(self.orderbook.buy_orders[0], BuyOrder)

    def test_get_order(self):
        order = BuyOrder(20, 200)
        self.orderbook.add_order(order)
        res = get_order(order.id)
        res_json = json.loads(res)
        self.assertEqual(res_json['order']['id'], order.id)
        self.assertEqual(res_json['order']['size'], order.size)
        self.assertEqual(res_json['order']['price'], order.price)

    def test_order_404(self):
        res = get_order(1)
        self.assertIn('error', res)

    def test_get_orderbook(self):
        res = get_orderbook()


class TestModels(unittest.TestCase):
    pass



if __name__ == '__main__':


    unittest.main()    
