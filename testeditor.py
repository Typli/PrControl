import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Укажите путь к JSON-файлу с ключами
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
])

# Авторизация
client = gspread.authorize(creds)

# Открытие таблицы по названию
sheet = client.open("Products").sheet1

# Чтение данных
data = sheet.get_all_records()
print("Данные из таблицы:")
for row in data:
    print(row)

# Добавление новой записи
new_record = [
    "Н910-01-101 Стойка",  # drawing name
    "Резка",     # operation type
    10,            # number of products
    5.5,           # machine setup time
    15.0,          # manufacturing time
    1,             # defect
    "Tool wear",   # cause of defect
    "No issues"    # notes
]
sheet.append_row(new_record)

print("Запись успешно добавлена!")