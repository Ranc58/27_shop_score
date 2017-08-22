from datetime import date
from sqlalchemy import create_engine, Date, cast, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session


postgres_db = {'drivername': 'postgresql',
               'username': 'score',
               'password': 'Rysherat2',
               'host': 'shopscore.devman.org',
               'database': 'shop'}
ENGINE = create_engine(URL(**postgres_db))
YELLOW_STATUS = 420
RED_STATUS = 1800


def get_table():
    base = automap_base()
    base.prepare(ENGINE, reflect=True)
    return base.classes.orders


def get_orders_handling_info(orders):
    session = Session(ENGINE)
    time_diff = orders.confirmed - orders.created
    day_confirmed_filter = cast(orders.confirmed, Date) == date.today()
    db_query = session.query(time_diff)
    unhandled_orders_count = db_query.filter(orders.confirmed is None).count()
    handled_orders_count = db_query.filter(day_confirmed_filter).count()
    max_handled_time = session.query(func.max(time_diff))
    max_daily_handled_time = max_handled_time.filter(day_confirmed_filter)
    return {'unhandled_orders_count': unhandled_orders_count,
            'max_daily_handled_time': max_daily_handled_time.scalar(),
            'handled_orders_count': handled_orders_count}


def get_orders_handling_status(handling_info):
    handling_status = 'Green'
    handling_time = handling_info['max_daily_handled_time'].seconds
    if handling_time > RED_STATUS:
        handling_status = 'Red'
    elif handling_time > YELLOW_STATUS:
        handling_status = 'Yellow'
    return handling_status


def get_info_for_flask():
    orders = get_table()
    handling_info = get_orders_handling_info(orders)
    handling_status = get_orders_handling_status(handling_info)
    return {'unhandled_orders_count': handling_info['unhandled_orders_count'],
            'status': handling_status,
            'handled_orders_count': handling_info['handled_orders_count']}
