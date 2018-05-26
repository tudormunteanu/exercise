from models import BuyOrder, SellOrder


def get_oder_class(order_type):

    
    if order_type == "buy":
        return BuyOrder
    elif order_type == "sell":
        return SellOrder
    raise Exception("Invalid order type")