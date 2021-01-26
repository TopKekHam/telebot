import requests
import json
from io import BufferedReader
from typing import Optional, List, Any, Dict, Union, IO, Callable


# Types


class TelegramBot:
    token: str

    def __init__(self, token : str):
        self.token = token


class File:
    file_id : str
    file_unique_id : str
    file_size : Optional[int]
    file_path : Optional[str]

# Functions
# helper functions

# token : telegram bot token
# method_name : telegram bot api method name
def telegram_endpoint(token: str, method_name: str) -> str:
    return f'https://api.telegram.org/bot{token}/{method_name}'


def get(token: str, method: str) -> Optional[Any]:
    res = requests.get(telegram_endpoint(token, method)).json()
    print(res)

    if res['ok']:
        return res['result']

    else:
        print(res)
        return None


def post(token: str, method: str, data: Any, files : Dict[str, Any] = None) -> Optional[Any]:

    res = requests.post(telegram_endpoint(token, method), data=data, files = files).json()
    print(res)

    if res['ok']:
        return res['result']

    else:
        print(res)
        return None

def post_ex(token: str, method: str, optinals: Optional[Dict[str, Any]], **kwargs) -> Optional[Any]:

    data : Dict[str, Any] = {}
    files : Dict[str, IO] = {}
    
    if optinals:
        for i ,(key, value) in enumerate(optinals.items()):
            if isinstance(value, BufferedReader):
                files[key] = value
            else:
                if value:
                    data[key] = value
    
    for i ,(key, value) in enumerate(kwargs.items()):
        if isinstance(value, BufferedReader):
            files[key] = value
        else:
            if value:
                data[key] = value

    res = requests.post(telegram_endpoint(token, method), data=data, files = files).json()
    #print(res)

    if res['ok']:
        return res['result']

    else:
        print(res)
        return None


def ValueOrNone(key : str, dict : Dict[str, Any]) -> Any:
    if key in dict:
        return dict[key]
    else:
        return None

# telegram methods


def get_me(bot : TelegramBot) -> Optional[Any]:
    res = get(bot.token, 'getMe')
    print[res]

    if res['ok']:
        return res['result']
    else:
        print(res)
        return None


# creates bot instance and opens telegram bot webhook
# url: webhook endpoint
# token: bot private token
def create_bot(url : str , token : str) -> Optional[TelegramBot]:
    res = post(token, 'setWebhook', data = {'url' : url})
    
    if res != None:
        return TelegramBot(token)

    else:
        return None


def shutdown_webhook(bot : TelegramBot) -> bool:
    res = get(bot.token, 'deleteWebhook')
    return res != None

# read: https://core.telegram.org/bots/api#logout
def log_out(bot: TelegramBot) -> bool:
    res = get(bot.token, 'logOut')
    return res != None


# read: https://core.telegram.org/bots/api#close
def close(bot: TelegramBot) -> bool:
    res = get(bot.token, 'close')
    return res != None


# the first list is the row of buttons
# the second list is the buttons in the row
# the button is InlineButtonWithCallbackData telegram class
def optinal_inline_keyboard(buttons : List[List[Any]]) -> Dict[str, Any]:
    return {'reply_markup': json.dumps({'inline_keyboard': buttons})}


def optinal_disable_notification(value : bool = True) -> Dict[str, Any]:
    return {'disable_notification' : value}


def optinal_reply_to_message(message_id : int, allow_sending_without_reply: bool = False) -> Dict[str, Any]:
    return {'reply_to_message_id' : message_id, 'allow_sending_without_reply' : allow_sending_without_reply }


# works for video, audio, photo ,ducoment, voice.
def optinal_caption(caption : str) -> Dict[str, Any]:
    return {'caption' : caption}


# TODO: for now we can only use url of the thumbnail to send one
# we need to implement multipart/form-data as a thumbnail
# the thumbmail should be in JPEG format and less than 200 kB in size
# A thumbnail's width and height should not exceed 320
def option_thumbnail(url : Union[str, IO]) -> Dict[str, Any]:
    return {'thumb' : url}


# duration: in seconds
def options_audio(duration : int = 0, preformer : str = '', title : str = '') -> Dict[str, Any]:
    return {'duration' : duration, 'preformer' : preformer, 'title' : title}


# duration: in seconds
def options_video(duration : int = 0, width : int = 0, height : int = 0) -> Dict[str, Any]:
    return {'duration' : duration, 'width' : width, 'height' : height}


# check optinals: https://core.telegram.org/bots/api#sendmessage
def send_message(bot: TelegramBot, chat_id: str, text: str, optinals: Optional[Dict[str, Any]] = None) -> Optional[Any]:
    res = post_ex(bot.token, 'sendMessage', optinals, chat_id=chat_id, text=text)
    
    if res:
        return res

    return None


# The photo must be at most 10 MB in size. 
# photo: url of the image/file_id or InputFile(https://core.telegram.org/bots/api#inputfile)
# check optinals: https://core.telegram.org/bots/api#sendphoto
def send_photo(bot : TelegramBot, chat_id : str, photo : Union[str, IO], optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendPhoto', optinals, chat_id=chat_id, photo=photo)
    return res


# Bots can send audio of .MP3 or .M4A format and up to 50 MB in size
# audio: url of the audio/file_id or InputFile(https://core.telegram.org/bots/api#inputfile)
# check optinals: https://core.telegram.org/bots/api#sendaudio
def send_audio(bot: TelegramBot, chat_id : str, audio : Union[str, IO], optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendAudio', optinals, chat_id=chat_id, audio=audio)
    return res


# Bots can send files of any type of up to 50 MB in size
# audio: url of the audio/file_id or InputFile(https://core.telegram.org/bots/api#inputfile)
# check optinals: https://core.telegram.org/bots/api#senddocuments
def send_document(bot: TelegramBot, chat_id : str, document : [str, IO], optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendDocument', optinals, chat_id=chat_id, document=document)
    return res


# Telegram clients support mp4 videos
# Bots can send video files of up to 50 MB in size
# check optinals: https://core.telegram.org/bots/api#sendvideo
def send_video(bot: TelegramBot, chat_id : str, video : Union[str, IO], optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendVideo', optinals, chat_id=chat_id, video=video)
    return res


# check optinals: https://core.telegram.org/bots/api#sendlocation
def send_location(bot: TelegramBot, chat_id : str, latitude : float , longitude : float, optinals: Optional[Dict[str, Any]] = None) -> any:
    res = post_ex(bot.token, 'sendLocation', optinals, chat_id=chat_id, latitude=latitude, longitude=longitude)
    return res    


# check optinals: https://core.telegram.org/bots/api#sendvenue
def send_venue(bot: TelegramBot, chat_id : str, latitude : float , longitude : float, title : str, address : str, optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendVenue', optinals, chat_id=chat_id, latitude=latitude, longitude=longitude, title=title, address=address)
    return res


# check optinals: https://core.telegram.org/bots/api#sendcontact
def send_contact(bot: TelegramBot, chat_id : str, phone_number: str, first_name : str , last_name : str = None, optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendContact', optinals, chat_id=chat_id, phone_number=phone_number, first_name=first_name, last_name=last_name)
    return res


# check optinals: https://core.telegram.org/bots/api#sendpoll
# options: list of answer options, 2-10 strings 1-100 characters each
def send_poll(bot: TelegramBot, chat_id : str, question : str , poll_options : List[str], optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendPoll', optinals, chat_id=chat_id, question=question, options=json.dumps(poll_options))
    return res


# Currently, must be one of “🎲”, “🎯”, “🏀”, “⚽”, or “🎰”. 
# values 1-6 for “🎲” and “🎯”, 
# values 1-5 for “🏀” and “⚽”,
# values 1-64 for “🎰”
# Defaults to “🎲”
# optinals: https://core.telegram.org/bots/api#senddice
def send_dice(bot: TelegramBot, chat_id : str, emoji : '🎲', optinals: Optional[Dict[str, Any]] = None) -> Any:
    res = post_ex(bot.token, 'sendDice', optinals, chat_id=chat_id, emoji=emoji)
    return res


def get_file(bot: TelegramBot, file_id : str) -> Optional[File]:
    res = post_ex(bot.token, 'getFile', file_id=file_id)

    if res:
        file : File = File()
        file.file_id = res['file_id']
        file.file_unique_id = res['file_unique_id']
        file.file_size = ValueOrNone('file_size', res)
        file.file_path = ValueOrNone('file_path', res)

        return file
    
    else:
        return None


# read: https://core.telegram.org/bots/api#getuserprofilephotos
def get_user_profile_photos(bot: TelegramBot, offset : int = 0, limit : int = 100) -> Any:
    res = post_ex(bot.token, 'getUserProfilePhotos', offset=offset, limit=limit)
    return res


# MessageHandler

#redefine the 'on' methods 
class UpdateHandler:

    # returns true if handled the messagee else false
    def handle_update(self, update: Dict[str, Any], context : Any = None) -> bool:
        if 'message' in update and 'text' in update['message']:
            return self.on_message(update, update['message']['text'], context)

        elif 'callback_query' in update and 'data' in update['callback_query']:
            return self.on_callback_query(update, update['callback_query']['data'], context)
        
        else:
            return False

    def on_message(self, update : Any, message : str, context : Any) -> bool:
        return False
    
    def on_callback_query(self, update : Any, data : str, context : Any) -> bool:
        return False


class MessageRouter:
    
    routes : Dict[str, Callable[[List[str], Any], bool]]

    def __init__(self):
        self.routes = {}

    def handle_message(self, route : str, message : List[str], context : Any = None) -> bool:
        if route in self.routes:
            return self.routes[route](message, context)
        else:
            return False

    def route(self, path):
        def wrapper(method):
            self.routes[path] = method
            return method

        return wrapper
