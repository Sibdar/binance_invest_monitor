from Binance_API.Binance_API import Binance_API
from MySQL.MySQL import MySQL
from Telegram.TelegramHandler import TelegramHandler

bapi = Binance_API()
db = MySQL()
tg = TelegramHandler()

# 1
# get curr crypto prices from binance API
price_data = bapi.get_all_curr_prices()
# construct values for insert statement | curr_prices
values_cps = ', '.join([f"('{t[0]}', '{t[1]}', NOW())" for t in price_data])
# insert into curr_prices tab
db.insrt_into_prices(values_cps)
# get assets data & curr prices in usdt
assets_data = sorted(bapi.get_assets(), key=lambda k: k['asset'])
curr_price_usdt = sorted(bapi.get_curr_coin_price_usdt(), key=lambda k: k[0])
# construct values for insert statement | my_assets
values = ', '.join([f"('{a['asset']}', {round(float(a['free']), 5)}, {round(float(a['free'])*cp[1], 1)}, CURDATE(), CURTIME())"
                    for a, cp in zip(assets_data, curr_price_usdt)])
# insert into my_assets
db.insrt_into_my_assets(values)

# 2
# get list of all orders
orders = bapi.construct_all_orders()
# orderId, symbol, price, quantity, invested, status, side, time, date
values = ', '.join([f"({ordr['orderId']}, '{ordr['symbol']}', {ordr['price']}, {ordr['quantity']}, "
                      f"{ordr['invested']}, '{ordr['status']}', '{ordr['side']}', '{ordr['time'][0]}', '{ordr['time'][1]}')"
                    for ordr in orders])
# insert into curr_prices tab
db.insrt_into_orders(values)

# 3
db.update_prj_detail_tab()

# 4
db.update_prj()

# 5 send prj_data to tg
prj_name, mon_acc, comp_at, t_pas = db.get_prj_data('Driving Licence')
msg = f"\U0001F4CA*Daily Report:*\n\n" \
      f"\U0001F4BC_Project_: {prj_name}\n" \
      f"\U0001F4B0Profit: {mon_acc}\n" \
      f"\U00002705Completed at: {comp_at}\n" \
      f"\U000023F3Time passed: {t_pas}"
tg.send_msg(msg)
