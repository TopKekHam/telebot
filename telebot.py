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


# https://core.telegram.org/bots/api#sendmessage
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
# The photo must be at most 10 MB in size. 
# photo: url of the image/file_id or InputFile(https://core.telegram.org/bots/api#inputfile)
# check options: https://core.telegram.org/bots/api#sendphoto
def send_photo(bot : TelegramBot, chat_id : str, photo : str, options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'photo' : photo}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendPhoto', data)
    return res


# TODO: for now we can only use url or file_id of the audio to send one
# we need to implement multipart/form-data as a audio
#-------------------------------------------------------------
# Bots can send audio of .MP3 or .M4A format and up to 50 MB in size
# audio: url of the audio/file_id or InputFile(https://core.telegram.org/bots/api#inputfile)
# check options: https://core.telegram.org/bots/api#sendaudio
def send_audio(bot: TelegramBot, chat_id : str, audio : str, options: Optional[Dict[str, Any]] = None):
    
    data = {'chat_id' : chat_id, 'audio' : audio}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendAudio', data)
    return res


# TODO: for now we can only use url or file_id of the document to send one
# we need to implement multipart/form-data as a document
#-------------------------------------------------------------
# Bots can send files of any type of up to 50 MB in size
# audio: url of the audio/file_id or InputFile(https://core.telegram.org/bots/api#inputfile)
# check options: https://core.telegram.org/bots/api#senddocuments
def send_document(bot: TelegramBot, chat_id : str, document : str, options: Optional[Dict[str, Any]] = None):
    
    data = {'chat_id' : chat_id, 'document' : document}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendDocument', data)
    return res


# TODO: for now we can only use url or file_id of the video to send one
# we need to implement multipart/form-data as a document
#-------------------------------------------------------------
# Telegram clients support mp4 videos
# Bots can send video files of up to 50 MB in size
# check options: https://core.telegram.org/bots/api#sendvideo
def send_video(bot: TelegramBot, chat_id : str, video : str, options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'video' : video}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendVideo', data)
    return res


# check options: https://core.telegram.org/bots/api#sendlocation
def send_location(bot: TelegramBot, chat_id : str, latitude : float , longitude : float, options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'latitude' : latitude, 'longitude' : longitude}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendLocation', data)
    return res

# check options: https://core.telegram.org/bots/api#sendvenue
def send_venue(bot: TelegramBot, chat_id : str, latitude : float , longitude : float, title : str, address : str, options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'latitude' : latitude, 'longitude' : longitude, 'title' : title, 'address' : address}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendVenue', data)
    return res

# check options: https://core.telegram.org/bots/api#sendcontact
def send_contact(bot: TelegramBot, chat_id : str, phone_number: str, first_name : str , options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'phone_number' : phone_number, 'first_name' : first_name}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendContact', data)
    return res


# check options: https://core.telegram.org/bots/api#sendpoll
# options: list of answer options, 2-10 strings 1-100 characters each
def send_poll(bot: TelegramBot, chat_id : str, question : str , poll_options : List[str], options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'question' : question, 'options' : json.dumps(poll_options)}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendPoll', data)
    return res


# Currently, must be one of “🎲”, “🎯”, “🏀”, “⚽”, or “🎰”. 
# values 1-6 for “🎲” and “🎯”, 
# values 1-5 for “🏀” and “⚽”,
# values 1-64 for “🎰”
# Defaults to “🎲”
# options: https://core.telegram.org/bots/api#senddice
def send_dice(bot: TelegramBot, chat_id : str, emoji : '🎲', options: Optional[Dict[str, Any]] = None):

    data = {'chat_id' : chat_id, 'emoji' : emoji}   

    if options:
        data.update(options)

    res = post(bot.token, 'sendDice', data)
    return res