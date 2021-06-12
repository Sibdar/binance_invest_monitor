import requests
import config
import telebot


class TelegramHandler():

    def __init__(self):
        # CryptInvest_Bbot token
        self.token = config.tg_token
        # init telebot
        self.tb = telebot.TeleBot(self.token)
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
        req_api = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={obj}&" \
                  f"parse_mode=Markdown"
        return requests.get(req_api)

    def send_msg_tb(self, msg):
        self.tb.send_message(self.chat_id, msg, parse_mode='MarkdownV2')


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