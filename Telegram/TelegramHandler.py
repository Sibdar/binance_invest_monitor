import json
import requests
import config


class TelegramHandler():

    def __init__(self):
        # CryptInvest_Bbot token
        self.token = config.tg_token
        # get cryptoinvest_monitor chat_id using `get_updates`
        self.chat_id = config.chat_id

    # check autoriz. by getting `Response: 200`
    def check_autorz(self):
        return requests.get(f"https://api.telegram.org/bot{self.token}/getMe")

    # get chat_id by updates
    def get_updates(self):
        req_api = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates")
        return req_api.content

    def send_msg(self, obj):
        req_api = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={obj}"
        return requests.get(req_api)


def main():
    tg = TelegramHandler()

    # check autoriz.
    # print(tg.check_autorz())

    # get chat_id by updates
    # print(tg.get_updates())

    # send test message
    print(tg.send_msg('Test'))


if __name__ == '__main__':
    main()