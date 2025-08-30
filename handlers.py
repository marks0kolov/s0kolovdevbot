from aiogram import Router
from aiogram.filters import Command
from aiogram import types as ttypes
from aiogram import F
from config import REQUEST_LABELS

masterR = Router(name="master")
idR = Router(name="get_ID")
infoR = Router(name="get_info")

@masterR.message(Command("start")) # the /start command was sent
async def send_welcome(msg: ttypes.Message):
    "send a welcome message"
    await msg.answer(
        "Hello! 👋\n" \
        "I am a bot for Telegram bot developers.\n" \
        "Use /help to see the list of available commands.\n" \
        "<i>From developers, for developers</i>"
    )

@masterR.message(Command("help")) # the /help command was sent
async def send_list_of_commands(msg: ttypes.Message):
    await msg.answer(
        "Here's the list of all features for now:\n\n" \
        "/getid - get the ID of a user, bot, group, or channel\n\n" \
        "We are constantly making this bot better, so stay tuned for updates! 🚀"
    )

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
