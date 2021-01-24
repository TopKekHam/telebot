from fastapi import FastAPI, Body
from telebot import TelegramBot
from typing import Any
import telebot

token : str = '<bot-token>'
# telegram webhooks only work with https, you can use ngrok for dev(that what I use for testing).
host : str = 'https://host.com'
telegram_webhook_endpoing :str = '/telegram_webhook'

app : FastAPI = FastAPI()

# we are initialazining the bot here because 
# for some reason if we initialaze the bot in starup event it doesnt work.
bot : TelegramBot = telebot.create_bot(f'{host}{telegram_webhook_endpoing}', token)

@app.on_event("startup")
async def startup_event():  
    # print(telebot.get_me(bot))
    # print(bot)
    return

@app.on_event("shutdown")
async def shutdown_event():
    telebot.shutdown_webhook(bot)


def is_message_update(update : Any) -> bool:
    return 'message' in update and 'text' in update['message']

def is_callback_data_update(update : Any) -> bool:
    return 'callback_query' in update and 'data' in update['callback_query']

@app.post(telegram_webhook_endpoing)
async def telegram_webhook(update = Body(...)):

    # help
    if is_message_update(update) and update['message']['text'] == 'help':
        commands = '\nping\nphoto\nbuttoms\naudio\ndocument\nvideo\nlocation\nvenue\ncontact\npoll\ndice'
        telebot.send_message(bot, update['message']['chat']['id'], f'commands:{commands}')

    # ping pong example 
    if is_message_update(update) and update['message']['text'] == 'ping':
        telebot.send_message(bot, update['message']['chat']['id'], 'pong')

     # send photo example
    if is_message_update(update) and update['message']['text'] == 'photo':
        telebot.send_photo(bot, update['message']['chat']['id'], 'https://source.unsplash.com/random')

        # inline bottons example
    if is_message_update(update) and update['message']['text'] == 'buttons':
        buttons = [
                   [{'text' : 'button wide', 'callback_data' : 'button wide'}],
                   [{'text' : 'button half', 'callback_data' : 'button half left'}, {'text' : 'button half', 'callback_data' : 'button half right'}]
                ]
        buttons_options = telebot.option_inline_keyboard(buttons)
        telebot.send_message(bot, update['message']['chat']['id'], 'buttons', buttons_options)

    if is_callback_data_update(update):
        #print(update['callback_query']['message'])
        chat_id = update['callback_query']['message']['chat']['id']
        data = update['callback_query']['data']
        telebot.send_message(bot, chat_id, f'you choosed: {data}')

    # audio
    if is_message_update(update) and update['message']['text'] == 'audio':
        telebot.send_audio(bot, update['message']['chat']['id'], 'https://sounds-mp3.com/mp3/0005635.mp3')

    # documentdocument['message']['text'] == 'document':
        telebot.send_audio(bot, update['message']['chat']['id'], 'https://www.rfc-editor.org/rfc/pdfrfc/rfc7231.txt.pdf')

    # video
    if is_message_update(update) and update['message']['text'] == 'video':
        telebot.send_video(bot, update['message']['chat']['id'], 'https://cdn.videvo.net/videvo_files/video/premium/video0037/large_watermarked/docklands_clocks06_preview.mp4')

    # location
    if is_message_update(update) and update['message']['text'] == 'location':
        telebot.send_location(bot, update['message']['chat']['id'], 32.2655662, -112.7396284)

    # venue
    if is_message_update(update) and update['message']['text'] == 'venue':
        telebot.send_venue(bot, update['message']['chat']['id'], 32.2655662, -112.7396284, 'Best City Ever', 'Why, Arizona, USA')

    # contact
    if is_message_update(update) and update['message']['text'] == 'contact':
        telebot.send_contact(bot, update['message']['chat']['id'], '1-234-457-89', 'John')

    # poll
    if is_message_update(update) and update['message']['text'] == 'poll':
        telebot.send_poll(bot, update['message']['chat']['id'], 'am I a gopollod Bot ;3', ['Yes', 'No', 'Maybe'])

    # dice
    if is_message_update(update) and update['message']['text'] == 'dice':
        telebot.send_dice(bot, update['message']['chat']['id'], '🎯')
