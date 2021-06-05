from Binance_API.Binance_API import Binance_API
from MySQL.MySQL import MySQL


bapi = Binance_API()
db = MySQL()
# get list of all orders
orders = bapi.construct_all_orders()
# orderId, symbol, price, quantity, invested, status, side, time, date
values = ', '.join([f"({ordr['orderId']}, '{ordr['symbol']}', {ordr['price']}, {ordr['quantity']}, "
                      f"{ordr['invested']}, '{ordr['status']}', '{ordr['side']}', '{ordr['time'][0]}', '{ordr['time'][1]}')"
                    for ordr in orders])
# insert into curr_prices tab
db.insrt_into_orders(values)