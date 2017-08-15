import datetime
from datetime import timedelta
import psycopg2


def connect_to_db():
    db_params = ('shopscore.devman.org', 'shop', 'score', 'Rysherat2')
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'"
    conn = psycopg2.connect(conn_string.format(*db_params))
    cursor = conn.cursor()
    return cursor


def get_today_confirmed_orders(cursor):
    yesterday = 1
    actual_date = datetime.date.today()
    yesterday = actual_date - timedelta(yesterday)
    cursor.execute(
        "SELECT created,confirmed "
        "FROM public.orders "
        "WHERE created>'{0}'AND confirmed>'{1}'"
        .format(yesterday, actual_date))
    today_confirmed_orders = cursor.fetchall()
    return today_confirmed_orders


def output_orders_statuses(today_confirmed_orders):
    orders_status_list = []
    confirmed_time = -1
    created_time = 0
    red_alert_time = 30 * 60
    yellow_alert_time = 7 * 60
    for order in today_confirmed_orders:
        if order[confirmed_time] is None:
            orders_status_list.append('None')
            continue
        time_diff = order[confirmed_time] - order[created_time]
        if time_diff.seconds > red_alert_time:
            orders_status_list.append('Red')
        elif time_diff.seconds > yellow_alert_time:
            orders_status_list.append('Yellow')
        else:
            orders_status_list.append('Green')
    return orders_status_list


def output_for_flask():
    cursor = connect_to_db()
    today_confirmed_orders = get_today_confirmed_orders(cursor)
    orders_statuses = output_orders_statuses(today_confirmed_orders)
    unhandled_orders_count = orders_statuses.count('None')
    min_unhandled_orders_count = 1
    if unhandled_orders_count > min_unhandled_orders_count:
        orders_statuses.remove('None')
    handled_orders_count = len(orders_statuses)
    if 'Red' in orders_statuses:
        status = 'Red'
    elif 'Yellow' in orders_statuses:
        status = 'Yellow'
    else:
        status = 'Green'
    return {'unhandled_orders_count': unhandled_orders_count,
            'handled_orders_count': handled_orders_count,
            'status': status}


if __name__ == '__main__':
    print(output_for_flask())
