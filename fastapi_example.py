from fastapi import FastAPI, Body
from telebot import TelegramBot
from typing import Any
import telebot

token : str = '<bot-token>'
host : str = 'https://yourhost.com'
telegram_webhook_endpoing :str = '/telegram_webhook'

app : FastAPI = FastAPI()

# we are initialazining the bot here because 
# for some reason if we initialaze the bot in starup event it doesnt work.
bot_data : TelegramBot = telebot.create_bot(f'{host}{telegram_webhook_endpoing}', token)

@app.on_event("startup")
async def startup_event():  
    # print(telebot.get_me(bot_data))
    # print(bot_data)
    return

@app.on_event("shutdown")
async def shutdown_event():
    telebot.shutdown_webhook(bot_data)


def is_message_update(update : Any) -> bool:
    return 'message' in update and 'text' in update['message']

def is_callback_data_update(update : Any) -> bool:
    return 'callback_query' in update and 'data' in update['callback_query']

@app.post(telegram_webhook_endpoing)
async def telegram_webhook(update = Body(...)):

    # ping pong example 
    if is_message_update(update) and update['message']['text'] == 'ping':
        telebot.send_message(bot_data, update['message']['chat']['id'], 'pong')

     # send photo example
    if is_message_update(update) and update['message']['text'] == 'photo':
        telebot.send_photo(bot_data, update['message']['chat']['id'], 'https://source.unsplash.com/random')

        # inline bottons example
    if is_message_update(update) and update['message']['text'] == 'buttons':
        buttons = [
                   [{'text' : 'button wide', 'callback_data' : 'button wide'}],
                   [{'text' : 'button half', 'callback_data' : 'button half left'}, {'text' : 'button half', 'callback_data' : 'button half right'}]
                ]
        buttons_options = telebot.option_inline_keyboard(buttons)
        telebot.send_message(bot_data, update['message']['chat']['id'], 'buttons', buttons_options)

    if is_callback_data_update(update):
        #print(update['callback_query']['message'])
        chat_id = update['callback_query']['message']['chat']['id']
        data = update['callback_query']['data']
        telebot.send_message(bot_data, chat_id, f'you choosed: {data}')

    # help
    if is_message_update(update) and update['message']['text'] == 'help':
        telebot.send_message(bot_data, update['message']['chat']['id'], 'commands:\nping\nphoto\nbuttoms')
