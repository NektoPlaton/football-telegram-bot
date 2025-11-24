import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import TELEGRAM_TOKEN, FOOTBALL_API_KEY, TEAM_ID, COMPETITION_CODE
from data_api import get_next_matches, get_last_results, get_tournament_table, get_team_squad, get_events
from aiogram.filters import CommandStart, Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ближайшие матчи", callback_data="matches"),
            InlineKeyboardButton(text="Последние игры", callback_data="lastgames")
        ],
        [
            InlineKeyboardButton(text="Таблица", callback_data="tournament"),
            InlineKeyboardButton(text="Состав", callback_data="squad")
        ],
        [
            InlineKeyboardButton(text="События", callback_data="events")
        ]
    ]
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для фанатов команды. Выберите опцию на клавиатуре ниже:", reply_markup=MENU)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Просто нажми на кнопки ниже — всё интуитивно!\nЕсли что-то не работает — пиши @твой_ник", reply_markup=MENU)

@dp.callback_query()
async def cb_handler(query: types.CallbackQuery):
    action = query.data
    await query.answer()  # обязательно, иначе будет "часики" крутиться вечно

    if action == "matches":
        text = get_next_matches(team_id=TEAM_ID, api_key=FOOTBALL_API_KEY)
    elif action == "lastgames":
        text = get_last_results(team_id=TEAM_ID, api_key=FOOTBALL_API_KEY)
    elif action == "tournament":
        text = get_tournament_table(competition_code=COMPETITION_CODE, api_key=FOOTBALL_API_KEY)
    elif action == "squad":
        text = get_team_squad(team_id=TEAM_ID, api_key=FOOTBALL_API_KEY)
    elif action == "events":
        text = get_events()
    else:
        text = "Неизвестная команда."

    await query.message.answer(text)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
