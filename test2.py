from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# Токен вашего бота
API_TOKEN = 'YOUR_BOT_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Создаем кнопку для открытия Mini App
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Открыть Mini App", web_app=types.WebAppInfo(url="https://your-web-app-url.com"))]
    ])
    await message.reply("Нажмите кнопку, чтобы открыть Mini App:", reply_markup=keyboard)

# Обработка данных из Mini App
@dp.message()
async def handle_web_app_data(message: types.Message):
    if message.web_app_data:
        data = message.web_app_data.data  # Данные из Mini App
        # Обработайте данные (например, сохраните в Google Sheets)
        await message.reply(f"Данные получены: {data}")

# Запуск бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())