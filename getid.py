import requests

# Ваш access_token
access_token = "y0__wgBEOOP-WEYos00IIuu5YoSVJsq06bcB2gQwPAh0V1-k9QzFG8"

# Заголовки для авторизации
headers = {
    "Authorization": f"OAuth {access_token}".encode("utf-8").decode("latin-1"),
}

# URL для получения списка файлов
url = "https://cloud-api.yandex.net/v1/disk/resources/files"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    files = response.json().get("items", [])
    for file in files:
        print(f"Имя файла: {file['name']}, file_id: {file['file_id']}")
else:
    print(f"Ошибка: {response.status_code}")
    print(response.json())