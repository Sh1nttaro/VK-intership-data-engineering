import datetime
import os
import random
import string
import sys

# Список провайдеров электронной почты
EMAIL_PROVIDERS = [
    "gmail.com",
    "ya.ru",
    "mail.ru",
]

# Список возможных действий для пользователей (CRUD-операции)
ACTION_TYPES = [
    "CREATE",
    "READ",
    "UPDATE",
    "DELETE",
]


# Функция для генерации случайной строки длиной char_num символов
def random_char(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


# Функция для генерации случайного email
def generate_email():
    return f"{random_char(random.randrange(5, 15))}@{random.choice(EMAIL_PROVIDERS)}"


if __name__ == "__main__":
    dirname = sys.argv[1]  # Папка для сохранения файлов
    dt = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
    days_cnt = int(sys.argv[3])  # Количество дней для генерации данных
    emails_cnt = int(sys.argv[4])  # Количество email для генерации
    emails = [generate_email() for _ in range(emails_cnt)]
    events_cnt = int(sys.argv[5])  # Количество событий для каждого дня

    for i in range(days_cnt):
        current_dt = dt + datetime.timedelta(days=i)
        filepath = os.path.join(dirname, f"{current_dt.strftime('%Y-%m-%d')}.csv")
        with open(filepath, "w") as out:
            out.write(
                "\n".join(
                    f"{random.choice(emails)},{random.choice(ACTION_TYPES)},{current_dt + datetime.timedelta(seconds=random.randrange(0, 60*60*24))}"
                    for _ in range(events_cnt)
                )
            )
