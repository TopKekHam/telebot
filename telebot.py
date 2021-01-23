import requests
import json
from typing import Optional, List, Any, Dict, Union

# Types
class TelegramBot:
    token: str

    def __init__(self, token : str):
        self.token = token


# Functions
# helper functions

# token : telegram bot token
# method_name : telegram bot api method name
def telegram_endpoint(token: str, method_name: str) -> str:
    return f'https://api.telegram.org/bot{token}/{method_name}'


def get(token: str, method: str) -> Optional[Any]:
    res = requests.get(telegram_endpoint(token, method)).json()

    if res['ok']:
        return res['result']

    else:
        print(res)
        return None


def post(token: str, method: str, data: Any) -> Optional[Any]:
    res = requests.post(telegram_endpoint(token, method), data=data).json()
    
    if res['ok']:
        return res['result']

    else:
        print(res)
        return None

# telegram methods


def get_me(bot : TelegramBot) -> Optional[Any]:
    res = get(bot.token, 'getMe')

    if res:
        return User.parse_obj(res)
    
    else:buttons
# creates bot instance and opens telegram bot webhook
# url: webhook endpoint
# token: bot private token
def create_bot(url : str , token : str) -> Optional[TelegramBot]:
    res = post(token, 'setWebhook', data = {'url' : url})
    
    if res != None:
        return TelegramBot(token)

    else:
        return None


def shutdown_webhook(bot : TelegramBot) -> None:
    res = get(bot.token, 'deleteWebhook')

# the first list is the row of buttons
# the second list is the buttons in the row
# the button is InlineButtonWithCallbackData telegram class
def option_inline_keyboard(buttons : List[List[Any]]) -> Dict[str, Any]:
    return {'reply_markup': json.dumps({'inline_keyboard': buttons})}


# view options ib telegram bot api
def send_message(bot: TelegramBot, chat_id: str, text: str, options: Optional[Dict[str, Any]] = None) -> Optional[Any]:
    data = {'chat_id': chat_id, 'text': text}

    if options:
        data.update(options)

    print(data)
    res = post(bot.token, 'sendMessage', data)

    if res:
        return res

    return None

# TODO: for now we can only use url of the photo to send one
# we need to implement multipart/form-data as a photo
#-------------------------------------------------------------
# photo: url of the image or InputFile(telegram class, use message_photo to create one)
# check options: https://core.telegram.org/bots/api#sendphoto
def send_photo(bot : TelegramBot, chat_id : str, photo : str, options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'photo' : photo}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendPhoto', data)
    return res