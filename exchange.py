from datetime import datetime
from helpers import get_oder_class
from models import Storage
import json

storage = Storage()
orderbook = storage.orderbook


def create_order(data_in):


    keys = sorted(list(data_in.keys()))
    if keys != ['price', 'size', 'type']:
        output = {
            "error": "Missing keys",
        }
        return json.dumps(output)
    _class = get_oder_class(data_in['type'])
    order = _class(data_in['price'], data_in['size'])
    orderbook.add_order(order)
    output = {
        "order_id": 123
    }   
    return json.dumps(output)


def get_order(id):


    for o in storage.orderbook.get_all_orders():
        if o.id == id:
            order = o
            break
    else:
        order = None
    if order:
        output = {
            "order": vars(order)
        }
    else:
        output = {
            "error": "No such order."
        }
    return json.dumps(output, default=str)


def get_orderbook():
    

    output = storage.orderbook.aggregate()
    return json.dumps(output)



