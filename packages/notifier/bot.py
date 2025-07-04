import os
from pathlib import Path
from telebot import TeleBot
from vyper import v

config = Path(__file__).parent.joinpath('../../').joinpath('config')
#config = Path(__file__).resolve().parent.parent.parent / 'config'
v.set_config_name('prod')
print(config)
print(config.is_dir())
v.add_config_path(config)
v.read_in_config()

os.environ['TELEGRAM_BOT_CHAT_ID'] = v.get('telegram.chat_id')
os.environ['TELEGRAM_BOT_ACCESS_TOKEN'] = v.get('telegram.token')


def send_file() -> None:
    telegram_bot = TeleBot(v.get('telegram.token'))
    file_path = Path(__file__).resolve().parent.parent.parent / 'swagger-coverage-dm-api-account.html'
    with open(file_path, 'rb') as document:
        telegram_bot.send_document(
            v.get('telegram.chat_id'),
            document=document,
            caption='coverage'
        )

if __name__ == '__main__':
    send_file()