from datetime import datetime
from helpers import get_oder_class
from models import Storage
import json

storage = Storage()
orderbook = storage.orderbook


def create_order(request):

    data_in = request.json
    keys = sorted(list(data_in.keys()))
    if keys != ['price', 'size', 'type']:
        output = {
            "error": "Missing keys",
        }
        return 400, json.dumps(output)
    _class = get_oder_class(data_in['type'])
    order = _class(data_in['price'], data_in['size'])
    orderbook.add_order(order)
    output = {
        "order_id": order.id
    }   
    return 200, json.dumps(output)


def get_order(request, id):

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
        return 200, json.dumps(output, default=str)        
    output = {
        "error": "No such order."
    }
    return 404, json.dumps(output, default=str)


def get_orderbook(request):
    

    output = storage.orderbook.aggregate()
    return 200, json.dumps(output)
