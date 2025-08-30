from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PARSE_MODE = ParseMode.HTML
REQUEST_LABELS: dict[int, str] = {
    1: "user",
    2: "bot",
    3: "group",
    4: "channel",
}
