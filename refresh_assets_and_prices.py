from Binance_API.Binance_API import Binance_API
from MySQL.MySQL import MySQL


bapi = Binance_API()
db = MySQL()
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



