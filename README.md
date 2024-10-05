## Системные требования:

### Системные зависимости:

1. **Docker версии 20.10.8 или выше.**
2. **Docker Compose версии 1.29.2 или выше.**
3. **PostgreSQL версии 13 (в контейнере).**
4. **Apache Airflow версии 2.5.0 (в контейнере).**

### Пакеты и расширения:

1. **pandas**
2. **psycopg2**

## Структура проекта:

<br>├── airflow/
<br>│   ├── dags/
<br>│   │   ├── dag_aggregate.py     # Определение DAG для агрегации данных в Airflow
<br>│   │   └── script-output.py     # Скрипт для агрегации данных
<br>│   ├── input/                  # Входные данные для обработки
<br>│   ├── logs/                   # Логи выполнения задач Airflow
<br>│   ├── output/                  # Выходные данные после обработки и агрегации
<br>│   └── temp/                    # Временные файлы для промежуточных данных
<br>├── postgres-data/               # Данные PostgreSQL базы данных (используется контейнером)
<br>├── script-input.py              # Скрипт для генерации случайных данных
<br>├── docker-compose.yaml          # Конфигурация Docker для запуска Airflow и PostgreSQL
<br>└── README.md                    # Документация проекта

## Описание

Этот проект содержит два скрипта:

1. **script-input.** — генерирует тестовые данные в формате CSV с событиями для случайных пользователей.
2. **script-output** — агрегирует данные, сгенерированные скриптом генерации, по дням и неделям.

## Функционал

### script-input:
- Генерация случайных email-адресов с доменами из заранее заданного списка.
- Генерация случайных событий (CREATE, READ, UPDATE, DELETE) с временными метками.
- Сохранение сгенерированных данных в CSV-файлы, где каждое событие содержит email, тип действия и временную метку.
- Возможность указания количества дней, за которые нужно сгенерировать данные, и количества событий для каждого дня.

### script-output:
- Агрегация событий за день для каждого пользователя.
- Создание временных файлов для каждой дневной агрегации.
- Агрегация данных за неделю на основе данных по дням.
- Сохранение итогового недельного агрегированного отчета в CSV-файл.

## Как использовать

### Запуск генератора данных

1. **Клонируйте проект или загрузите файл скрипта:**

    ```bash
    git clone <URL проекта>
    cd <название папки проекта>

2. **Запустите script-input для генерации данных**

    Перейдите в папку airflow: ```cd airflow``` и запустите в терминале:
   
    ```python script-input.py <папка_для_сохранения> <стартовая_дата> <количество_дней> <количество_email> <количество_событий>```
   
    Пример:
   
    ```python script-input.py ./output 2024-09-18 7 100 500```

4. **Запуск Docker контейнера**

    Для запуска контейнеров наберите docker-compose up -d
    Для остановки контейнеров наберите docker-compose down

5. **Запуск задачи агрегации**

    Логин: admin Пароль: admin

    Откройте брайзер и перейдите на ```http://localhost:8081```

    Найди DAG с именем ```aggregate_weakly_data``` и запустите его вручную

    Агригированные данные сохраняются в папку ```./output```

    Промежуточные данные сохраняются в папку ```./temp```
