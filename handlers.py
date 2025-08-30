from aiogram import Router
from aiogram.filters import Command
from aiogram import types as ttypes
from aiogram import F
from aiogram.fsm.context import FSMContext
import json

from config import REQUEST_LABELS, Send_Info

####################################### - MASTER - #######################################

masterR = Router(name="master")

@masterR.message(Command("start")) # the /start command was sent
async def send_welcome(msg: ttypes.Message, state: FSMContext):
    "send a welcome message"
    await msg.answer(
        "Hello! 👋\n" \
        "I am a bot for Telegram bot developers.\n" \
        "Use /help to see the list of available commands.\n" \
        "<i>From developers, for developers</i>"
    ) # send welcomming message
    await state.clear() # clear the state

@masterR.message(Command("help")) # the /help command was sent
async def send_list_of_commands(msg: ttypes.Message):
    await msg.answer(
        "Here's the list of all features for now:\n\n" \
        "/getid - get the ID of a user, bot, group, or channel\n\n" \
        "We are constantly making this bot better, so stay tuned for updates! 🚀"
    ) # send a list of commands

####################################### - GET ID - #######################################

idR = Router(name="get_ID")

@idR.message(Command("getid")) # the /getid command was sent
async def ask_whose_id(msg: ttypes.Message):
    "ask whose id to get"

    get_id_keyboard = ttypes.ReplyKeyboardMarkup(
        keyboard=[
            [
                ttypes.KeyboardButton(
                    text="👤 User",
                    request_user=ttypes.KeyboardButtonRequestUser(request_id=1)
                )
            ],
            [
                ttypes.KeyboardButton(
                    text="🤖 Bot",
                    request_user=ttypes.KeyboardButtonRequestUser(
                        request_id=2,
                        user_is_bot=True,
                    ),
                )
            ],
            [
                ttypes.KeyboardButton(
                    text="👥 Group",
                    request_chat=ttypes.KeyboardButtonRequestChat(
                        request_id=3,
                        chat_is_channel=False,
                    ),
                )
            ],
            [
                ttypes.KeyboardButton(
                    text="📢 Channel",
                    request_chat=ttypes.KeyboardButtonRequestChat(
                        request_id=4,
                        chat_is_channel=True,
                    ),
                )
            ],
        ],
        resize_keyboard=True,
    )

    await msg.answer(
        "Choose whose ID to get:",
        reply_markup=get_id_keyboard,
    )

@idR.message(F.user_shared) # a user or a bot was shared
async def send_user_id(msg: ttypes.Message):
    "send the shared user's id"
    shared = msg.user_shared 
    user_id = shared.user_id
    req_id = shared.request_id

    text = f"<b>{REQUEST_LABELS[req_id]} id:</b> <code>{user_id}</code>"
    await msg.answer(text, reply_markup=ttypes.ReplyKeyboardRemove())

@idR.message(F.chat_shared) # a group or a channel was shared
async def send_chat_id(msg: ttypes.Message):
    "send the shared chat's id"
    shared = msg.chat_shared
    chat_id = shared.chat_id
    req_id = shared.request_id

    text = f"<b>{REQUEST_LABELS[req_id]} id:</b> <code>{chat_id}</code>"
    await msg.answer(text, reply_markup=ttypes.ReplyKeyboardRemove())

####################################### - GET INFO - #######################################

infoR = Router(name="get_info")

@infoR.message(Command("getinfo")) # the /getinfo command was sent
async def set_info_state(msg: ttypes.Message, state: FSMContext):
    "set the state to get update"
    await msg.answer("Send me a message and I will give you all i knwo about it!")
    await state.set_state(Send_Info.waiting_for_update)

@infoR.business_message(Command("getinfo")) # the /getinfo command was sent in a business chat
async def set_business_info_state(msg: ttypes.Message, state: FSMContext):
    "set the state to get business update"
    await msg.answer("Send me a business message and I will give you all i knwo about it!")
    await state.set_state(Send_Info.waiting_for_business_update)

@infoR.message(Send_Info.waiting_for_update) # a message when the bot is waiting for an update to be sent
async def send_message_info(msg: ttypes.Message, state: FSMContext):
    "send the json-formatted message update"

    msg_json = json.dumps(msg.model_dump(mode="json"), indent=2, ensure_ascii=False)
    from_name_tag = {("@" + msg.from_user.username) if msg.from_user.username else msg.from_user.full_name}
    forwarded_tag = "Forwarded from " + (f"<pre>{msg.forward_from.id} ({("@" + msg.forward_from.username) if msg.forward_from.username else msg.forward_from.full_name})</pre>\n") if msg.forward_from else ""

    await msg.answer(
        "<b>💬 Message received:</b>\n\n" \
        f"<blockquote expandable><pre>{msg_json}</pre></blockquote>\n" \
        "<b>Main info:</b>\n" \
        "<blockquote expandable>" \
            f"Message ID: <pre>{msg.message_id}</pre>\n" \
            f"From: <pre>{msg.from_user.id} ({from_name_tag})</pre>\n" \
            f"Content type: <pre>{msg.content_type}</pre>\n" \
            f"{forwarded_tag}" + \
        "</blockquote>"
    )
    await state.clear() # clear the state

@infoR.business_message(Send_Info.waiting_for_business_update) # a message when the bot is waiting for an update to be sent
async def send_message_info(msg: ttypes.Message, state: FSMContext):
    "send the json-formatted business message update"

    msg_json = json.dumps(msg.model_dump(mode="json"), indent=2, ensure_ascii=False)
    from_name_tag = {("@" + msg.from_user.username) if msg.from_user.username else msg.from_user.full_name}
    forwarded_tag = "Forwarded from " + (f"<pre>{msg.forward_from.id} ({("@" + msg.forward_from.username) if msg.forward_from.username else msg.forward_from.full_name})</pre>\n") if msg.forward_from else ""

    await msg.answer(
        "<b>💬 Business message received:</b>\n\n" \
        f"<blockquote expandable><pre>{msg_json}</pre></blockquote>\n" \
        "<b>Main info:</b>\n" \
        "<blockquote expandable>" \
            f"Message ID: <pre>{msg.message_id}</pre>\n" \
            f"Business connection ID: <pre>{msg.business_connection_id}</pre>\n" \
            f"From: <pre>{msg.from_user.id} ({from_name_tag})</pre>\n" \
            f"Content type: <pre>{msg.content_type}</pre>\n" \
            f"{forwarded_tag}" + \
        "</blockquote>"
    )
    await state.clear() # clear the state
