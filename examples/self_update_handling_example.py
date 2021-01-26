import sys
sys.path.append('../')
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
# if you want to send a message and check out all examples make it true.
debug_mode : bool = False


@app.on_event("startup")
async def startup_event():  
    # print(telebot.get_me(bot))
    # print(bot)
    return

@app.on_event("shutdown")
async def shutdown_event():
    telebot.shutdown_webhook(bot)


def is_message_update(update : Any, message : str) -> bool:
    return debug_mode or 'message' in update and 'text' in update['message'] and update['message']['text'] == message

def is_callback_data_update(update : Any) -> bool:
    return 'callback_query' in update and 'data' in update['callback_query']

@app.post(telegram_webhook_endpoing)
async def telegram_webhook(update = Body(...)):

    # help
    if is_message_update(update, 'help'):
        commands = '\nping\nphoto\nphoto_file\nbuttoms\naudio\naudio_file\ndocument\ndocument_file\nvideo\nvideo_fie\nlocation\nvenue\ncontact\npoll\ndice\nreply\ndisable_notification'
        telebot.send_message(bot, update['message']['chat']['id'], f'commands:{commands}')

    # ping pong example 
    if is_message_update(update, 'ping'):
        telebot.send_message(bot, update['message']['chat']['id'], 'pong')

     # send photo example
    if is_message_update(update, 'photo'):
        optinals = telebot.optinal_caption('this is a moose?')
        telebot.send_photo(bot, update['message']['chat']['id'], 'https://source.unsplash.com/random', optinals)

        # inline bottons example
    if is_message_update(update, 'buttons'):
        buttons = [
                   [{'text' : 'button wide', 'callback_data' : 'button wide'}],
                   [{'text' : 'button half', 'callback_data' : 'button half left'}, {'text' : 'button half', 'callback_data' : 'button half right'}]
                ]
        buttons_options = telebot.optinal_inline_keyboard(buttons)
        telebot.send_message(bot, update['message']['chat']['id'], 'buttons', buttons_options)

    if is_callback_data_update(update):
        chat_id = update['callback_query']['message']['chat']['id']
        data = update['callback_query']['data']
        telebot.send_message(bot, chat_id, f'you choosed: {data}')

    # audio
    if is_message_update(update, 'audio'):
        telebot.send_audio(bot, update['message']['chat']['id'], 'https://sounds-mp3.com/mp3/0005635.mp3')

    # document
    if is_message_update(update, 'document'):
        telebot.send_document(bot, update['message']['chat']['id'], 'https://www.rfc-editor.org/rfc/pdfrfc/rfc7231.txt.pdf')

    # video
    if is_message_update(update, 'video'):
        telebot.send_video(bot, update['message']['chat']['id'], 'https://cdn.videvo.net/videvo_files/video/premium/video0037/large_watermarked/docklands_clocks06_preview.mp4')

    # location
    if is_message_update(update, 'location'):
        telebot.send_location(bot, update['message']['chat']['id'], 32.2655662, -112.7396284)

    # venue
    if is_message_update(update, 'venue'):
        telebot.send_venue(bot, update['message']['chat']['id'], 32.2655662, -112.7396284, 'Best City Ever', 'Why, Arizona, USA')

    # contact
    if is_message_update(update, 'contact'):
        telebot.send_contact(bot, update['message']['chat']['id'], '1-234-457-89', 'John', 'Doe')

    # poll
    if is_message_update(update, 'poll'):
        telebot.send_poll(bot, update['message']['chat']['id'], 'am I a gopollod Bot ;3', ['Yes', 'No', 'Maybe'])

    # dice
    if is_message_update(update, 'dice'):
        telebot.send_dice(bot, update['message']['chat']['id'], '🎯')
    
    # reply
    if is_message_update(update, 'reply'):
        options = telebot.optinal_reply_to_message(update['message']['message_id'])
        telebot.send_message(bot, update['message']['chat']['id'], 'replying to message', options)

    # disable notification
    if is_message_update(update, 'disable_notification'):
        options = telebot.optinal_disable_notification()
        telebot.send_message(bot, update['message']['chat']['id'], 'no notification', options)

    # using multipart/form-data

    if is_message_update(update, 'audio_file'):
        # dont for get to and binary flag in open()
        telebot.send_audio(bot, update['message']['chat']['id'], open('../files/example_audio.mp3', 'rb'))

    if is_message_update(update, 'document_file'):
        # dont for get to and binary flag in open()
        telebot.send_document(bot, update['message']['chat']['id'], open('../files/example_document.txt', 'rb'))

    if is_message_update(update, 'video_file'):
        # dont for get to and binary flag in open()
        telebot.send_video(bot, update['message']['chat']['id'], open('../files/example_video.mp4', 'rb'))

    if is_message_update(update, 'photo_file'):
        # dont for get to and binary flag in open()
        telebot.send_photo(bot, update['message']['chat']['id'], open('../files/example_photo.jpg', 'rb'))