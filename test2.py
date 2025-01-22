from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging

# Включаем логирование для отладки
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
API_TOKEN = '8143935303:AAFMFtTEWgyXFp2BM5h0w5ZB-CM7NgKXHh8'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Создаем кнопку для открытия Mini App
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Открыть Mini App", web_app=types.WebAppInfo(url="https://typli.github.io/PrControl/"))]
    ])
    await message.reply("Нажмите кнопку, чтобы открыть Mini App:", reply_markup=keyboard)

# Обработка данных из Mini App
@dp.message()
async def handle_web_app_data(message: types.Message):
    if message.web_app_data:
        data = message.web_app_data.data  # Данные из Mini App
        # Обработайте данные (например, сохраните в Google Sheets)
        await message.reply(f"Данные получены: {data}")
    else:
        await message.reply("Данные не получены или формат сообщения неверный.")

# Запуск бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())