from datetime import date
from sqlalchemy import create_engine, Date, cast
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

ENGINE = create_engine("postgresql://"
                       "score:Rysherat2@shopscore.devman.org/shop")
YELLOW_STATUS = 700
RED_STATUS = 700 * 3


def get_table():
    Base = automap_base()
    Base.prepare(ENGINE, reflect=True)
    return Base.classes.orders


def get_actual_content(orders):
    session = Session(ENGINE)
    table = session.query(orders.created, orders.confirmed)
    today_orders = table.filter(cast(orders.created, Date) == date.today())
    return today_orders


def get_statuses(today_orders):
    unhandled_orders_count = 0
    status = 'Green'
    for order in today_orders:
        if order.confirmed is None:
            unhandled_orders_count += 1
            continue
        time_diff = order.confirmed - order.created
        if time_diff.seconds > RED_STATUS:
            status = 'Red'
        elif time_diff.seconds > YELLOW_STATUS and status is not 'Red':
            status = 'Yellow'
    handled_orders_count = len(today_orders.all()) - unhandled_orders_count
    return {'unhandled_orders_count': unhandled_orders_count,
            'status': status,
            'handled_orders_count': handled_orders_count}


def get_info_for_flask():
    orders = get_table()
    today_orders = get_actual_content(orders)
    order_statuses = get_statuses(today_orders)
    return order_statuses
