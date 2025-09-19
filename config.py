from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode
from aiogram.filters.state import State, StatesGroup

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") # bot token
PARSE_MODE = ParseMode.HTML # default parse mode for messages
REQUEST_LABELS: dict[int, str] = {
    1: "user",
    2: "bot",
    3: "group",
    4: "channel",
} # labels for different buttons' request_ids

class Send_Info(StatesGroup):
    waiting_for_update = State()
    waiting_for_business_update = State()
class GetUserInfo(StatesGroup):
        waiting_for_user_id = State()
