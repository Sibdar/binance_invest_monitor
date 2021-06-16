from Binance_API.Binance_API import Binance_API
from MySQL.MySQL import MySQL


bapi = Binance_API()
db = MySQL()
last_usdtrub = db.sel_last_usdtrub()
# to get date and time in appr. format, use str()
# print(last_usdtrub)
# project_name, budjet, goal, currency, create_date, create_time, end_date
proj_vals = f"('BrightFuture', {last_usdtrub[0]}, 310, '{last_usdtrub[1][0:3]}', '{last_usdtrub[2]}', " \
            f"'{last_usdtrub[3]}', '2022-06-15' )"
print(proj_vals)
# db.add_new_proj(proj_vals)