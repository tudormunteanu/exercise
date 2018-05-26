from exchange import create_order, get_order, get_orderbook
from exchange import storage
from models import SellOrder, BuyOrder, Storage, Orderbook
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
            "type": "sell",        
            "price": 20,
            "size": 100,
        }
        res = create_order(data)
        self.assertIn("order_id", res)
        self.assertEqual(len(self.orderbook.sell_orders), 1)
        self.assertIsInstance(self.orderbook.sell_orders[0], SellOrder)

    def test_create_order_buy(self):
        data = {
            "type": "buy",        
            "price": 20,
            "size": 100,
        }
        res = create_order(data)
        self.assertIn("order_id", res)
        self.assertEqual(len(self.orderbook.buy_orders), 1)
        self.assertIsInstance(self.orderbook.buy_orders[0], BuyOrder)

    def test_create_buy_order_missing_data(self):
        data = {
            "price": 20,
        }
        res = create_order(data)
        self.assertIn("error", res)

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

    def test_get_orderbook_only_buy(self):
        order = BuyOrder(20, 200)
        self.orderbook.add_order(order)
        res = get_orderbook()
        res_json = json.loads(res)
        self.assertEqual(len(res_json["buy"]), 1)

    def test_get_orderbook_both(self):
        order1 = BuyOrder(20, 200)
        order2 = SellOrder(22, 100)        
        self.orderbook.add_order(order1)
        self.orderbook.add_order(order2)        
        res = get_orderbook()
        res_json = json.loads(res)
        self.assertEqual(len(res_json["buy"]), 1)
        self.assertEqual(len(res_json["sell"]), 1)

    def test_get_orderbook_aggregated(self):
        order1 = BuyOrder(20, 200)
        order2 = SellOrder(22, 100)
        order3 = SellOrder(22, 50)
        order4 = SellOrder(21, 50)        
        self.orderbook.add_orders([order1, order2, order3, order4])
        res = get_orderbook()
        res_json = json.loads(res)
        self.assertEqual(len(res_json["buy"]), 1)
        self.assertEqual(len(res_json["sell"]), 2)
        self.assertEqual(res_json["sell"][0]["size"], 50)
        self.assertEqual(res_json["sell"][1]["size"], 150)


class TestModels(unittest.TestCase):


    def test_sorting_buy_orders(self):
        order1 = BuyOrder(20, 100)
        order2 = BuyOrder(19, 150)
        order3 = BuyOrder(10, 40)
        order4 = BuyOrder(20, 121)
        orderbook = Orderbook()
        orderbook.add_orders([order1, order2, order3, order4])
        self.assertEqual(orderbook.buy_orders, [order3, order2, order1, order4])

    def test_sorting_sell_orders(self):
        order1 = SellOrder(20, 100)
        order2 = SellOrder(19, 150)
        order3 = SellOrder(10, 40)
        order4 = SellOrder(20, 121)
        orderbook = Orderbook()
        orderbook.add_orders([order1, order2, order3, order4])
        self.assertEqual(orderbook.sell_orders, [order3, order2, order1, order4])


if __name__ == '__main__':


    unittest.main()    
