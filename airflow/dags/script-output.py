import datetime
import os
import sys

import pandas as pd


# Функция для агрегации данных за один день
def aggregate_daily(input_dir, temp_dir, current_date):
    file_path = os.path.join(input_dir, f"{current_date.strftime('%Y-%m-%d')}.csv")
    temp_file_path = os.path.join(
        temp_dir, f"{current_date.strftime('%Y-%m-%d')}_daily.csv"
    )

    # Если промежуточный файл уже существует, используем его
    if os.path.exists(temp_file_path):
        print(f"Использование промежуточного файла: {temp_file_path}")
        return pd.read_csv(temp_file_path)

    # Если промежуточного файла нет, то обрабатываем данные и сохраняем
    if os.path.exists(file_path):
        print(f"Чтение исходного файла: {file_path}")
        df = pd.read_csv(file_path, names=["email", "action", "datetime"])
        aggregated = df.groupby(["email", "action"]).size().unstack(fill_value=0)
        aggregated.columns = [f"{col.lower()}_count" for col in aggregated.columns]

        # Сохранение промежуточного результата
        os.makedirs(temp_dir, exist_ok=True)
        aggregated.to_csv(temp_file_path, index=True)
        print(f"Сохранение промежуточного файла: {temp_file_path}")

        return aggregated
    else:
        print(f"Файл не найден: {file_path}, пропускаем.")
        return pd.DataFrame()


# Основная функция для агрегации данных за неделю
def aggregate_weekly(input_dir, temp_dir, output_dir, date_str):
    target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    data_frames = []

    # Обрабатываем последние 7 дней до target_date включительно
    for i in range(7):
        current_date = target_date - datetime.timedelta(days=i)
        daily_aggregated = aggregate_daily(input_dir, temp_dir, current_date)
        if not daily_aggregated.empty:
            data_frames.append(daily_aggregated)

    if not data_frames:
        print("Нет данных для агрегации.")
        return

    # Объединение всех дневных агрегатов в один недельный
    print(f"Объединение данных за неделю: {target_date.strftime('%Y-%m-%d')}")
    all_data = pd.concat(data_frames).groupby(["email"]).sum()

    # Сохраняем итоговый файл с недельной агрегацией
    output_file = os.path.join(
        output_dir, f"{target_date.strftime('%Y-%m-%d')}_weekly.csv"
    )
    all_data.to_csv(output_file, index=True)
    print(f"Недельные агрегированные данные сохранены в {output_file}")


# Точка входа в скрипт
if __name__ == "__main__":
    input_directory = sys.argv[1]
    temp_directory = sys.argv[2]
    output_directory = sys.argv[3]
    date = sys.argv[4]

    os.makedirs(output_directory, exist_ok=True)

    aggregate_weekly(input_directory, temp_directory, output_directory, date)
