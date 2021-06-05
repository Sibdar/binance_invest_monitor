# import api_config
from Binance_API import api_config
from binance.client import Client
from datetime import datetime


class Binance_API():
    def __init__(self):
        self.client = Client(api_config.API_KEY, api_config.API_SECRET)
        self.coins = ['ATOM', 'BTC', 'BNB', 'DOGE', 'ETH', 'LINK', 'MATIC', 'USDT', 'XRP']
        self.coins_pairs = ['USDTRUB', 'ETHUSDT', 'MATICUSDT', 'BTCUSDT', 'DOGEUSDT', 'ETHBUSD', 'DOGERUB', 'ATOMBTC']

    def get_assets(self):
        l = []
        info = self.client.get_account()
        for asset_info in info['balances']:
            if asset_info['asset'] in self.coins:
                l.append(asset_info)
        return l

    def get_all_orders(self, coin):
        l = []
        orders = self.client.get_all_orders(symbol=coin, limit=20)
        for order in orders:
            l.append(order)
        return l

    def construct_all_orders(self):
        all_orders = []
        for coin in self.coins_pairs:
            orders_per_coin = self.client.get_all_orders(symbol=coin)
            for order in orders_per_coin:
                if order['status'] == 'FILLED':
                    order_data = ({'orderId': order["orderId"],
                                   'symbol': order["symbol"],
                                   'time': datetime.fromtimestamp(order["updateTime"] / 1000).strftime("%Y-%m-%d %H:%M:%S").split(' '),
                                   'price': float(order["price"]),
                                   'invested': float(order["cummulativeQuoteQty"]),
                                   'quantity': float(order["origQty"]),
                                   'side': order["side"],
                                   'status': order["status"]
                                  })
                    all_orders.append(order_data)
        return all_orders

    def get_curr_coin_price(self, symbol):
        items = self.client.get_all_tickers()
        for item in items:
            if item['symbol'] == symbol:
                return item['symbol'], float(item['price'])

    def get_all_curr_prices(self):
        return [self.get_curr_coin_price(coin) for coin in self.coins_pairs]

    def get_curr_coin_price_usdt(self):
        l = []
        for coin in self.coins:
            if coin != 'USDT':
                coin += 'USDT'
                curr_pr = self.get_curr_coin_price(coin)
                l.append(curr_pr)
        return l + [('USDT', 1)]


def main():
    bapi = Binance_API()
    print(bapi.get_all_orders('USDTRUB'))


if __name__ == '__main__':
    main()