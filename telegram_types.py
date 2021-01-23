from typing import Optional, Union, List, Any
from enum import Enum
from pydantic import BaseModel, Field

class User(BaseModel):
    id : int
    is_bot : bool
    first_name : str
    last_name : Optional[str]
    username : Optional[str]
    language_code : Optional[str]
    can_join_groups : Optional[bool]
    can_read_all_group_messages : Optional[bool]
    supports_inline_queries : Optional[bool]

class Location(BaseModel):
    longitude: float
    latitude : float 
    horizontal_accuracy : Optional[Union[float, int]]
    live_period : Optional[int]
    heading : Optional[int]
    proximity_alert_radius : Optional[int]

class InlineQuery(BaseModel):
    id : str
    _from : User = Field(None, alias ='from')
    location : Optional[Location]
    query : str
    offset : str

class ChosenInlineResult(BaseModel):
    result_id : str
    _from : User = Field(None, alias ='from')
    location : Optional[Location]
    inline_message_id : Optional[str]
    query : str

class ShippingAddress(BaseModel):
    country_code : str
    state : str
    city : str
    street_line1 : str 
    street_line2 : str
    post_code : str

class ShippingQuery(BaseModel):
    id : str
    _from : User = Field(None, alias ='from')
    invoice_payload : str
    shipping_address : ShippingAddress


class OrderInfo(BaseModel):
    name : Optional[str]
    phone_number : Optional[str]
    email : Optional[str]
    shipping_address : Optional[ShippingAddress]

class PreCheckoutQuery(BaseModel):
    id : str
    _from : User = Field(None, alias ='from')
    currency : str
    total_amount : int 
    invoice_payload : str
    shipping_option_id : Optional[str]
    order_info : Optional[OrderInfo]

class PollOption(BaseModel):
    text : str
    voter_count : int

class MessageEntity(BaseModel):
    _type : str = Field(None, alias ='type')
    offset : int
    length : int 
    url : Optional[str]
    user : Optional[User]
    language : Optional[str]

# class PollType(str, Enum, BaseModel):
#    regular = 'regular'
#    quiz = 'quiz'

class Poll(BaseModel):
    id : str
    options : List[PollOption]
    total_voter_count : int
    is_closed : bool
    is_anonymous : bool
    _type : str = Field('', alias ='type')
    allows_multiple_answers : bool
    correct_option_id : Optional[int]
    explanation : Optional[str]
    explanation_entities : Optional[List[MessageEntity]]
    open_period : Optional[int]
    close_date : Optional[int]

class PollAnswer(BaseModel):
    poll_id : str
    user : User
    option_ids : List[int]

class ChatPhoto(BaseModel):
    small_file_id : str
    small_file_unique_id : str
    big_file_id : str
    big_file_unique_id : str

class ChatPermissions(BaseModel):
    can_send_messages : Optional[bool]
    can_send_media_messages : Optional[bool]
    can_send_polls : Optional[bool]
    can_send_other_messages : Optional[bool]
    can_add_web_page_previews : Optional[bool]
    can_change_info : Optional[bool]
    can_invite_users : Optional[bool]
    can_pin_messages : Optional[bool]

class ChatLocation(BaseModel):
    location : Location
    address : str

# we are defining Message here and second time in the end of the file because python cant handle cicler class dependency
class Message():
    pass

class Chat(BaseModel):
    id : int
    _type : str = Field('', alias ='type')
    title : Optional[str]
    username : Optional[str]
    first_name : Optional[str]
    last_name : Optional[str]
    photo : Optional[ChatPhoto]
    bio : Optional[str]
    description : Optional[str]
    invite_link : Optional[str]
    pinned_message : Optional[Message]
    permissions : Optional[ChatPermissions]
    slow_mode_delay : Optional[int]
    sticker_set_name : Optional[str]
    can_set_sticker_set : Optional[bool]
    linked_chat_id : Optional[int]
    location : Optional[ChatLocation]

class PhotoSize(BaseModel):
    file_id : str
    file_unique_id : str
    width : int
    height : int
    file_size : Optional[int]

class Animation(BaseModel):
    file_id : str
    file_unique_id : str
    width : int
    height : int
    duration : int
    thumb : Optional[PhotoSize]
    file_name : Optional[str]
    mime_type : Optional[str]
    file_size : Optional[int]

class Audio(BaseModel):
    file_id : str
    file_unique_id : str
    duration : int
    performer : Optional[str]
    title : Optional[str]
    file_name : Optional[str]
    mime_type : Optional[str]
    file_size : Optional[int]
    thumb : Optional[PhotoSize]

class Document(BaseModel):
    file_id : str
    file_unique_id : str
    thumb : Optional[PhotoSize]
    file_name : Optional[str]
    mime_type : Optional[str]
    file_size : Optional[int]

class MaskPosition(BaseModel):
    point : str
    x_shift : Union[float, int]
    y_shift : Union[float, int]
    scale : Union[float, int]

class Video(BaseModel):
    file_id : str
    file_unique_id : str
    width : int
    height : int
    duration : int
    thumb : Optional[PhotoSize]
    file_name : Optional[str]
    mime_type : Optional[str]
    file_size : Optional[int]

class Sticker(BaseModel):
    file_id : str
    file_unique_id : str
    width : int
    height : int
    is_animated : bool
    thumb : Optional[PhotoSize]
    emoji : Optional[str]
    set_name : Optional[str]
    mask_position : Optional[MaskPosition]
    file_size : Optional[int]

class VideoNote(BaseModel):
    file_id : str
    file_unique_id : str
    length : int
    duration : int
    thumb : Optional[PhotoSize]
    file_size : Optional[int]

class Voice(BaseModel):
    file_id : str
    file_unique_id : str
    duration : int
    mime_type : Optional[str]
    file_size : Optional[int]

class Contact(BaseModel):
    phone_number : str
    first_name : str
    last_name : Optional[str]
    user_id : Optional[int]
    vcard : Optional[str]

class Dice(BaseModel):
    emoji : str
    value : int

class Game(BaseModel):
    title : str
    description : str
    photo : List[PhotoSize]
    text : Optional[str]
    text_entities : Optional[List[MessageEntity]]
    animation : Optional[Animation]

class Venue(BaseModel):
    location : Location
    title : str
    address : str
    foursquare_id : Optional[str]
    foursquare_type : Optional[str]
    google_place_id : Optional[str]
    google_place_type : Optional[str]

class Invoice(BaseModel):
    title : str
    description : str
    start_parameter : str
    currency : str
    total_amount : int

class SuccessfulPayment(BaseModel):
    currency : str
    total_amount : int
    invoice_payload : str
    shipping_option_id : Optional[str]
    order_info : Optional[OrderInfo]
    telegram_payment_charge_id : str
    provider_payment_charge_id : str

class PassportFile(BaseModel):
    file_id : str
    file_unique_id : str
    file_size : int
    file_date : int

class EncryptedPassportElement(BaseModel):
    _type : str = Field('', alias='type')
    data : Optional[str]
    phone_number : Optional[str]
    email : Optional[str]
    files : Optional[List[PassportFile]]
    front_side : Optional[PassportFile]
    reverse_side : Optional[PassportFile]
    selfie : Optional[PassportFile]
    translation : Optional[List[PassportFile]]
    hash : str

class EncryptedCredentials(BaseModel):
    data : str
    hash : str
    secret : str

class PassportData(BaseModel):
    data : List[EncryptedPassportElement]
    credentials : EncryptedCredentials

class ProximityAlertTriggered(BaseModel):
    traveler : User
    watcher : User
    distance : int

class LoginUrl(BaseModel):
    url : str
    forward_text : Optional[str]
    bot_username : Optional[str]
    request_write_access : Optional[bool]

# doc link: https://core.telegram.org/bots/api#inlinekeyboardbutton
class InlineKeyboardButton(BaseModel):
    text : str 
    url : Optional[str] 
    login_url : Optional[LoginUrl]
    callback_data : Optional[str]
    switch_inline_query : Optional[str]
    switch_inline_query_current_chat : Optional[str]
    callback_game : Optional[Any]
    pay : Optional[bool]

class InlineKeyboardMarkup(BaseModel):
    inline_keyboard : List[List[InlineKeyboardButton]]

class Message(BaseModel):
    message_id : Optional[int]
    _from : Optional[User] = Field(None, alias = 'from')
    sender_chat : Optional[Chat]
    date : int
    chat : Chat
    forward_from : Optional[User]
    forward_from_chat : Optional[Chat]
    forward_from_message_id : Optional[int]
    forward_signature : Optional[str]
    forward_sender_name : Optional[str]
    forward_date : Optional[int]
    reply_to_message : Optional[Message]
    via_bot : Optional[User]
    edit_date : Optional[int]
    media_group_id : Optional[str]
    author_signature : Optional[str]
    text : Optional[str]
    entities : Optional[List[MessageEntity]]
    animation : Optional[Animation]
    audio : Optional[Audio]
    document : Optional[Document]
    photo : Optional[List[PhotoSize]]
    sticker : Optional[Sticker]
    video : Optional[Video]
    video_note : Optional[VideoNote]
    voice : Optional[Voice]
    caption : Optional[str]
    caption_entities : Optional[List[MessageEntity]]
    contact : Optional[Contact]
    dice : Optional[Dice]
    game : Optional[Game]
    poll : Optional[Poll]
    venue : Optional[Venue]
    location : Optional[Location]
    new_chat_members : Optional[List[User]]
    left_chat_member : Optional[User]
    new_chat_title : Optional[str]
    new_chat_photo : Optional[List[PhotoSize]]
    delete_chat_photo : Optional[bool]
    group_chat_created : Optional[bool]
    supergroup_chat_created : Optional[bool]
    channel_chat_created : Optional[bool]
    migrate_to_chat_id : Optional[int]
    migrate_from_chat_id : Optional[int]
    pinned_message : Optional[Message]
    invoice : Optional[Invoice]
    successful_payment : Optional[SuccessfulPayment]
    connected_website : Optional[str]
    passport_data : Optional[PassportData]
    proximity_alert_triggered : Optional[ProximityAlertTriggered]
    reply_markup : Optional[InlineKeyboardMarkup]

class CallbackQuery(BaseModel):
    id : str
    _from : User =  Field(None, alias = 'from')
    message : Optional[Message]
    inline_message_id : Optional[str]
    chat_instance : str
    data : Optional[str]
    game_short_name : Optional[str] 

class Update(BaseModel):
    update_id : int
    message : Optional[Message]
    edited_message : Optional[Message]
    channel_post : Optional[Message]
    edited_channel_post : Optional[Message]
    inline_query : Optional[InlineQuery]
    chosen_inline_result : Optional[ChosenInlineResult]
    callback_query : Optional[CallbackQuery]
    shipping_query : Optional[ShippingQuery]
    pre_checkout_query : Optional[PreCheckoutQuery]
    poll : Optional[Poll]
    poll_answer : Optional[PollAnswer]