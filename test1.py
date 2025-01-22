import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка доступа к Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
])
client = gspread.authorize(creds)
sheet = client.open("Products").sheet1

# Токен вашего бота
API_TOKEN = 'ff'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Состояния пользователя
class Form(StatesGroup):
    drawing_name = State()
    operation_type = State()
    product_count = State()
    setup_time = State()
    manufacturing_time = State()
    defect = State()
    cause_of_defect = State()
    notes = State()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Привет! Я бот для редактирования таблиц. Используй /search для поиска чертежа.")
    await state.set_state(Form.drawing_name)

# Обработка ввода названия чертежа
@dp.message(Form.drawing_name)
async def process_drawing_name(message: types.Message, state: FSMContext):
    await state.update_data(drawing_name=message.text)
    await state.set_state(Form.operation_type)

    # Создаем клавиатуру для выбора типа операции
    operations = ["Токарная", "Фрезерная", "Слесарная", "Шлифовальная", "Сверлильная"]
    buttons = [
        InlineKeyboardButton(text=operation, callback_data=f"operation_{operation}")
        for operation in operations
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])  # Используем inline_keyboard

    await message.reply("Выберите тип операции:", reply_markup=keyboard)

# Обработка выбора типа операции
@dp.callback_query(F.data.startswith("operation_"))
async def process_operation_type(query: types.CallbackQuery, state: FSMContext):
    operation_type = query.data.split("_")[1]
    await state.update_data(operation_type=operation_type)
    await state.set_state(Form.product_count)
    await query.message.edit_text(f"Вы выбрали операцию: {operation_type}. Теперь введите количество изделий:")
    await query.answer()

# Обработка ввода количества изделий
@dp.message(Form.product_count)
async def process_product_count(message: types.Message, state: FSMContext):
    try:
        product_count = int(message.text)
        await state.update_data(product_count=product_count)
        await state.set_state(Form.setup_time)
        await message.reply("Введите время настройки станка (в часах):")
    except ValueError:
        await message.reply("Пожалуйста, введите число.")

# Обработка ввода времени настройки
@dp.message(Form.setup_time)
async def process_setup_time(message: types.Message, state: FSMContext):
    try:
        setup_time = float(message.text)
        await state.update_data(setup_time=setup_time)
        await state.set_state(Form.manufacturing_time)
        await message.reply("Введите время изготовления (в часах):")
    except ValueError:
        await message.reply("Пожалуйста, введите число.")

# Обработка ввода времени изготовления
@dp.message(Form.manufacturing_time)
async def process_manufacturing_time(message: types.Message, state: FSMContext):
    try:
        manufacturing_time = float(message.text)
        await state.update_data(manufacturing_time=manufacturing_time)
        await state.set_state(Form.defect)

        # Создаем клавиатуру для выбора наличия дефекта
        buttons = [
            InlineKeyboardButton(text="Да", callback_data="defect_1"),
            InlineKeyboardButton(text="Нет", callback_data="defect_0"),
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

        await message.reply("Есть ли дефект?", reply_markup=keyboard)
    except ValueError:
        await message.reply("Пожалуйста, введите число.")

# Обработка выбора наличия дефекта
@dp.callback_query(F.data.startswith("defect_"))
async def process_defect(query: types.CallbackQuery, state: FSMContext):
    defect = int(query.data.split("_")[1])
    await state.update_data(defect=defect)
    if defect:
        await state.set_state(Form.cause_of_defect)
        await query.message.edit_text("Введите причину дефекта:")
    else:
        await state.set_state(Form.notes)
        await query.message.edit_text("Введите примечания:")
    await query.answer()

# Обработка ввода причины дефекта
@dp.message(Form.cause_of_defect)
async def process_cause_of_defect(message: types.Message, state: FSMContext):
    await state.update_data(cause_of_defect=message.text)
    await state.set_state(Form.notes)
    await message.reply("Введите примечания:")

# Обработка ввода примечаний
@dp.message(Form.notes)
async def process_notes(message: types.Message, state: FSMContext):
    await state.update_data(notes=message.text)
    data = await state.get_data()

    # Сохраняем данные в Google Sheets
    try:
        new_record = [
            data["drawing_name"],
            data["operation_type"],
            data["product_count"],
            data["setup_time"],
            data["manufacturing_time"],
            data["defect"],
            data.get("cause_of_defect", ""),
            data["notes"]
        ]
        sheet.append_row(new_record)
        await message.reply("Данные успешно сохранены!")
    except Exception as e:
        await message.reply(f"Ошибка при сохранении данных: {e}")

    # Очищаем состояние
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())