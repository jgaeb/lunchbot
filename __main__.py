from .slck import LunchBot

with LunchBot() as lb:
    lb.send_order_message()
