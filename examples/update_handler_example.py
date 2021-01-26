import sys
sys.path.append('../')

from fastapi import FastAPI, Body
from typing import Any, List, Any
from telebot import UpdateHandler, TelegramBot, MessageRouter
import telebot

# redefine 'on' methods to use them.
class ExampleHandler(UpdateHandler):
    bot : TelegramBot
    router : MessageRouter

    def __init__(self, bot : TelegramBot, router : MessageRouter):
        self.bot = bot
        self.router = router
    
    # this is example for redefinition.
    # context is data that you can pass to handler on handling updates
    # this data is getting passed through the pipeline of the handler
    # the pipeline looks like this:
    #           you can do other stuff here ↴
    # handle_update -> on_##### method -> router.handle_message -> route
    def on_message(self, update : Any, message : str, context : Any) -> bool:
        words = message.split()
        context.update({'chat_id' : update['message']['chat']['id'], 'bot' : self.bot})
        self.router.handle_message(words[0], words[1:], context)
        return False

token : str = '<bot-token>'
# telegram webhooks only work with https, you can use ngrok for dev(that what I use for testing).
host : str = 'https://host.com'

telegram_webhook_endpoing :str = '/telegram_webhook'

app : FastAPI = FastAPI()
bot : TelegramBot = telebot.create_bot(f'{host}{telegram_webhook_endpoing}', token)
bot_message_router : MessageRouter = MessageRouter()
update_handler : ExampleHandler = ExampleHandler(bot, bot_message_router)

@app.on_event("shutdown")
async def shutdown_event():
    telebot.shutdo#               wn_webhook(bot)


@app.post(telegram_webhook_endpoing)
async def telegram_webhook(update = Body(...)):
# use the update handler
    update_handler.handle_update(update, {})

# routes

# the first word of the message is the route ex: 'get video 1231' => route = 'get, message = ['video', '1231']
# the context is data that get pass by the router
@bot_message_router.route("ping")
def ping(message : List[str], context : Any) -> bool:
    telebot.send_message(context['bot'], context['chat_id'], 'pong')
    return True

@bot_message_router.route('video')
def video(message : List[str], context : Any) -> bool:
    url = 'https://cdn.videvo.net/videvo_files/video/premium/video0037/large_watermarked/docklands_clocks06_preview.mp4'
    telebot.send_video(context['bot'], context['chat_id'], url)
    return True