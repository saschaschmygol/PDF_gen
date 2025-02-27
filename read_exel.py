import openpyxl
import pandas as pd
import sqlite3
import re
from datetime import datetime
import datetime
import locale
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
error_log = []  # Список для сбора ошибок

import json
import sqlite3
import pandas as pd
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QApplication
from PySide6.QtCore import Qt

class PositionDialog(QDialog):
    def __init__(self, data, json_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Уточнение должности")
        self.setFixedSize(800, 400)

        self.json_path = json_path
        self.data = data
        self.layout = QVBoxLayout(self)

        # Загрузка данных из JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            self.sphere_dict = json.load(file)

        # Создание таблицы
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Должность", "Тип"])

        # Заполнение таблицы данными
        for i, row in enumerate(data):
            # Проверка наличия данных в строке
            print(f"Row {i}: {row}")  # Отладочное сообщение

            # ФИО подставляются автоматически
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row.get('Фамилия', 'Неизвестно'))))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row.get('Имя', 'Неизвестно'))))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(row.get('Отчество', 'Неизвестно'))))

            # Название должности вписывается вручную
            self.tableWidget.setItem(i, 3, QTableWidgetItem(row.get('Должность', '')))

            # Тип должности выбирается из выпадающего списка
            combo = QComboBox()
            combo.addItems(["medical", "foodService", "utilityService", "nonMedical"])
            if row.get('Должность', '').lower() in self.sphere_dict:
                combo.setCurrentText(self.sphere_dict[row.get('Должность', '').lower()])
            self.tableWidget.setCellWidget(i, 4, combo)

        self.layout.addWidget(self.tableWidget)

        # Кнопка сохранения
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)
    def save_data(self):
        for i in range(self.tableWidget.rowCount()):
            position = self.tableWidget.item(i, 3).text().lower()  # Приводим к нижнему регистру
            sphere = self.tableWidget.cellWidget(i, 4).currentText()

            # Если тип не выбран, не добавляем должность в JSON
            if sphere:
                # Проверяем, существует ли уже такая должность в словаре
                if position not in self.sphere_dict:
                    # Если должность новая, добавляем её в соответствующую категорию
                    if sphere not in self.sphere_dict:
                        self.sphere_dict[sphere] = []
                    self.sphere_dict[sphere].append(position)

        # Сохранение обновленных данных в JSON
        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(self.sphere_dict, file, ensure_ascii=False, indent=4)

        self.accept()

def process_excel_to_sqlite(file_path, base_path, tableWidget=None):
    """
    Обрабатывает данные из Excel и сохраняет их в SQLite.
    Если передан tableWidget, данные отображаются в таблице.
    """
    # Путь к JSON файлу (можно вынести в конфигурацию)
    json_path = "positions.json"

    # Чтение данных из Excel файла
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        raise

    # Приведение всех имен столбцов к нижнему регистру для унификации
    df.columns = df.columns.str.strip().str.lower()
    print("Columns after normalization:", df.columns)

    # Проверка наличия столбцов с "unnamed"
    unnamed_columns = [col for col in df.columns if 'unnamed' in col]
    if unnamed_columns:
        for unnamed_col in unnamed_columns:
            df.rename(columns={unnamed_col: 'статус'}, inplace=True)
        print(f"Renamed columns {unnamed_columns} to 'статус'.")
    else:
        print("No unnamed columns found.")

    # Проверка наличия столбца 'статус'
    if 'статус' not in df.columns:
        print("Столбец 'Статус' не найден в Excel. Используется значение по умолчанию.")
        df['статус'] = None

    # Словарь для приведения столбцов из нижнего регистра к нужному виду
    columns_map = {
        'фамилия': 'Фамилия',
        'имя': 'Имя',
        'отчество': 'Отчество',
        'дата рождения': 'Дата рождения',
        'штатная должность': 'Штатная должность',
        'штатное подразделение': 'Штатное подразделение',
        'краткое название': 'Краткое название',
        'статус': 'Статус',
    }

    # Применяем соответствие столбцов
    df = df.rename(columns=columns_map)

    # Обработка даты рождения
    df['Дата рождения'] = pd.to_datetime(df['Дата рождения'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')

    # Загрузка данных из JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        sphere_dict = json.load(file)

    # Преобразуем JSON в словарь для быстрого поиска
    position_to_type = {}
    for sphere, positions in sphere_dict.items():
        for position in positions:
            position_to_type[position.lower()] = sphere  # Приводим к нижнему регистру


    # Определение пола по отчеству
    def determine_gender(patronymic):
        if "оглы" in patronymic:
            return "m"
        elif "кызы" in patronymic:
            return "w"
        elif patronymic.endswith("ич"):
            return "m"
        elif patronymic.endswith("на"):
            return "w"
        return "Неизвестно"

    # Преобразуем столбец 'Штатная должность' в строки и заменяем NaN на пустую строку
    df['Штатная должность'] = df['Штатная должность'].astype(str).replace('nan', '')

    # Функция для определения сферы по должности
    def determine_sphere(name):
        if not name:  # Если строка пустая
            return None
        name = name.lower()  # Приводим к нижнему регистру
        return position_to_type.get(name)  # Возвращаем тип из JSON или None, если должность не найдена

    # Определение типа для каждой должности
    df['Тип'] = df['Штатная должность'].apply(determine_sphere)

    # Сбор уникальных должностей из Excel
    unique_positions = df['Штатная должность'].dropna().str.lower().unique()

    # Поиск должностей, которых нет в JSON
    missing_positions = [pos for pos in unique_positions if pos not in position_to_type]


    # Если есть отсутствующие должности, вызываем диалоговое окно
    if missing_positions:
        # Приводим missing_positions к нижнему регистру и убираем дубликаты
        missing_positions = list(set(pos.lower() for pos in missing_positions))

        # Формируем dialog_data с данными из DataFrame
        dialog_data = []
        added_positions = set()  # Множество для отслеживания уже добавленных должностей

        for _, row in df.iterrows():  # Перебираем строки DataFrame
            position = row.get('Штатная должность', '').lower()  # Приводим должность к нижнему регистру

            # Если должность есть в missing_positions и ещё не добавлена
            if position in missing_positions and position not in added_positions:
                dialog_data.append({
                    'Фамилия': row.get('Фамилия', 'Неизвестно'),  # Если фамилия отсутствует, используем 'Неизвестно'
                    'Имя': row.get('Имя', 'Неизвестно'),  # Если имя отсутствует, используем 'Неизвестно'
                    'Отчество': row.get('Отчество', 'Неизвестно'),  # Если отчество отсутствует, используем 'Неизвестно'
                    'Должность': position  # Используем должность в нижнем регистре
                })
                added_positions.add(position)  # Добавляем должность в множество, чтобы избежать дубликатов

        # Проверка данных перед передачей в диалог
        print(f"Dialog data: {dialog_data}")

        # Создание и отображение диалога
        dialog = PositionDialog(dialog_data, json_path)
        if dialog.exec() == QDialog.Accepted:
            # После закрытия диалога обновляем position_to_type
            with open(json_path, 'r', encoding='utf-8') as file:
                sphere_dict = json.load(file)
                for sphere, positions in sphere_dict.items():
                    for position in positions:
                        position_to_type[position.lower()] = sphere

    # Определение типа для каждой должности
    df['Тип'] = df['Штатная должность'].apply(determine_sphere)

    # Подключение к базе данных SQLite
    try:
        conn = sqlite3.connect(base_path)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to SQLite database: {e}")
        raise

    # Начало транзакции
    conn.execute('BEGIN TRANSACTION')

    # Удаление всех данных из таблиц перед загрузкой новых
    try:
        cursor.execute("DELETE FROM immunization")
        cursor.execute("DELETE FROM worker")
        cursor.execute("DELETE FROM position")
        cursor.execute("DELETE FROM indicatorAntiHBs")
        print("Deleted all records from immunization, worker, position, indicatorAntiHBs.")

        cursor.execute("DELETE FROM sqlite_sequence WHERE name='immunization'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='worker'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='indicatorAntiHBs'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='position'")

        print("Reset auto-increment counters for all tables.")
    except Exception as e:
        print(f"Error deleting data from tables: {e}")
        conn.rollback()
        raise

    # Функция для преобразования NULL значений
    def normalize_value(value):
        return value if value is not None else 'NULL_VALUE'

    # Построение списка уникальных ключей, которые присутствуют в Excel
    unique_keys = df[['Фамилия', 'Имя', 'Отчество', 'Дата рождения']].dropna().astype(str).apply(lambda x: '|'.join(x),
                                                                                                 axis=1).tolist()

    # Удаление записей, которые не присутствуют в Excel
    cursor.execute("""
        DELETE FROM worker
        WHERE (firstname || '|' || name || '|' || lastname || '|' || dateOfBirth) NOT IN ({})
    """.format(','.join('?' * len(unique_keys))), unique_keys)
    print("Removed rows that are not present in the Excel file.")

    # Вставка или обновление данных в таблицу position
    for index, row in df.iterrows():
        name = normalize_value(row['Штатная должность']) if pd.notnull(row['Штатная должность']) else None
        area_of_work = row['Тип']  # Тип из JSON или None
        division = normalize_value(row['Штатное подразделение']) if pd.notnull(row['Штатное подразделение']) else None
        short_title = normalize_value(row['Краткое название']) if pd.notnull(row['Краткое название']) else None

        try:
            print(
                f"Processing row {index}: name={name}, division={division}, short_title={short_title}, area_of_work={area_of_work}")

            # Проверка существования записи в таблице position
            cursor.execute("""
                SELECT ID FROM position
                WHERE name_pos = ? AND division = ? AND shortTitle = ?
            """, (name, division, short_title))
            existing_record = cursor.fetchone()

            if existing_record:
                cursor.execute("""
                    UPDATE position
                    SET areaOfWork = ?
                    WHERE name_pos = ? AND division = ? AND shortTitle = ?
                """, (area_of_work, name, division, short_title))
                print(
                    f"Updated existing record: name={name}, division={division}, short_title={short_title}, area_of_work={area_of_work}")
            else:
                cursor.execute("""
                    INSERT INTO position (name_pos, areaOfWork, division, shortTitle)
                    VALUES (?, ?, ?, ?)
                """, (name, area_of_work, division, short_title))
                print(
                    f"Inserted new record: name={name}, division={division}, short_title={short_title}, area_of_work={area_of_work}")

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError inserting or updating row {index}: {e}")
        except Exception as e:
            print(f"Error inserting or updating row {index}: {e}")

    # Словарь для приведения значений "Статус" к допустимым
    status_mapping = {
        'осн': 'key',
        'врем': 'notKey',
        'совм': 'notKey',
        'вне': 'notKey',
        'омн': 'notKey',
    }

    # Вставка или обновление данных в таблицу worker
    id_counter = 1

    for _, row in df.iterrows():
        try:
            if pd.isna(row.get('Фамилия')) or pd.isna(row.get('Имя')) or pd.isna(row.get('Отчество')) or pd.isna(
                    row.get('Дата рождения')):
                print(f"Skipping row due to NULL value in required fields: {row.to_dict()}")
                continue

            status = row.get('Статус')
            if isinstance(status, str):
                status = status.strip()
                if status in status_mapping:
                    status = status_mapping[status]
                elif status not in ['key', 'notKey']:
                    print(f"Invalid status value: {status} in row: {row.to_dict()}")
                    continue
            else:
                status = None

            query = "SELECT ID FROM position WHERE 1=1"
            params = []

            if not pd.isna(row.get('Штатная должность')):
                query += " AND name_pos = ?"
                params.append(row['Штатная должность'])

            if not pd.isna(row.get('Штатное подразделение')):
                query += " AND division = ?"
                params.append(row['Штатное подразделение'])

            if not pd.isna(row.get('Краткое название')):
                query += " AND shortTitle = ?"
                params.append(row['Краткое название'])

            cursor.execute(query, params)
            position = cursor.fetchone()
            position_id = position[0] if position else None

            gender = determine_gender(row.get('Отчество', ''))

            cursor.execute("""
                INSERT INTO worker (ID, firstname, name, lastname, gender, dateOfBirth, status, position)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ID) DO UPDATE SET
                    firstname = excluded.firstname,
                    name = excluded.name,
                    lastname = excluded.lastname,
                    gender = excluded.gender,
                    dateOfBirth = excluded.dateOfBirth,
                    status = excluded.status,
                    position = excluded.position
            """, (
                id_counter,
                row.get('Фамилия'),
                row.get('Имя'),
                row.get('Отчество'),
                gender,
                row.get('Дата рождения'),
                status,
                position_id
            ))

            print(f"Inserted or updated: ID {id_counter}, {row.get('Фамилия')}, {row.get('Имя')}")
            id_counter += 1

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"Error: {e}")

    # Удаление некорректных записей с NULL в ключевых полях
    cursor.execute("""
        DELETE FROM worker
        WHERE firstname IS NULL OR lastname IS NULL OR name IS NULL OR dateOfBirth IS NULL
    """)
    print("Removed invalid rows with NULL in required fields.")

    # Вставка данных в таблицу Вакцинация
    # Переименование колонок в DataFrame (остается без изменений, так как Excel не меняется)
    df.rename(columns={
        'гв': 'ГВ',
        'клещевой энцефалит': 'Клещевой энцефалит',
        'адс-м': 'АДС-м',
        'шигеллвак (ежегодная вакцинация)': 'Шигеллвак',
        'корь': 'Корь',
        'краснуха': 'Краснуха',
        'гепатит а': 'Гепатит А',
        'грипп (ежегодная вакцинация)': 'Грипп',
        'ветряная оспа': 'Ветряная оспа',
        'впч': 'ВПЧ',
        'пневмо': 'Пневмо',
        'нкви': 'НКВИ',
        'гиг.аттестация': 'Гиг. аттестация'
    }, inplace=True)

    # Лог для проверки
    print(f"Columns after renaming: {df.columns}")

    # Словарь соответствий названий прививок
    vaccination_mapping = {
        'ГВ': 'hepatitisB',
        'Клещевой энцефалит': 'cleshEncephalit',
        'АДС-м': 'diphteriaTetanus',
        'Шигеллвак': 'sonneDysentery',
        'Корь': 'measles',
        'Краснуха': 'rubella',
        'Гепатит А': 'hepatitisA',
        'Грипп': 'gripp',
        'Ветряная оспа': 'chickenPox',
        'ВПЧ': 'pertussis',
        'Пневмо': 'pneumococcalInfection',
        'НКВИ': 'nkwi',
    }

    # Вставка данных в таблицу immunization
    for index, row in df.iterrows():
        try:
            # Получение ID сотрудника из таблицы worker
            cursor.execute("""
                SELECT ID FROM worker
                WHERE firstname = ? AND name = ? AND lastname = ? AND dateOfBirth = ?
            """, (row['Фамилия'], row['Имя'], row['Отчество'], row['Дата рождения']))
            worker = cursor.fetchone()
            if not worker:
                print(f"Worker not found: {row['Фамилия']} {row['Имя']} {row['Отчество']}")
                continue

            worker_id = worker[0]

            # Определение данных вакцинации
            vaccinations = {
                'ГВ': row['ГВ'],
                'Клещевой энцефалит': row['Клещевой энцефалит'],
                'АДС-м': row['АДС-м'],
                'Шигеллвак': row['Шигеллвак'],
                'Корь': row['Корь'],
                'Краснуха': row['Краснуха'],
                'Грипп': row['Грипп'],
                'Ветряная оспа': row['Ветряная оспа'],
                'ВПЧ': row['ВПЧ'],
                'НКВИ': row['НКВИ'],
            }

            annual_vaccinations = {'НКВИ', 'Шигеллвак', 'Грипп'}

            date_pattern = r'^\d{2}[./]\d{2}[./]\d{2,4}$'  # Для форматов дд.мм.гггг и дд/мм/гггг
            month_year_pattern = r'\d{2}\.\d{4}'  # Паттерн для месяца и года
            year_pattern = r'\d{4}(г\.?)?'
            allowed_types = {'rv', 'v', 'rv1', 'v1', 'v2', 'v3'}

            def is_valid_date(date_str):
                """Проверка на корректность даты и форматирование в YYYY-MM-DD"""
                try:
                    # Убираем лишние пробелы
                    date_str = date_str.strip()

                    # Обработка двухзначного года (например, 97 → 1997 или 02 → 2002)
                    if re.match(r'\d{2}\.\d{2}\.\d{2}$', date_str):  # Формат dd.mm.yy
                        day, month, year = date_str.split('.')
                        year = f"19{year}" if int(year) > 30 else f"20{year}"  # До 2030 года считаем 20xx
                        date_str = f"{day}.{month}.{year}"

                    # Попытка преобразовать дату с указанием dayfirst=True
                    parsed_date = pd.to_datetime(date_str, dayfirst=True, errors='coerce')
                    if pd.isna(parsed_date):
                        raise ValueError(f"Date parsing failed for: {date_str}")

                    # Возвращаем дату в формате YYYY-MM-DD
                    return parsed_date.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"Invalid date format: {date_str}. Error: {e}")
                    return None

            def fix_excel_date_format(date_str):
                """
                Исправление формата даты, если присутствуют лишние части, такие как '-01-01' или время.
                """
                if isinstance(date_str, str):
                    # Убираем всё после 10-го символа (YYYY-MM-DD), если дата имеет лишние части
                    if len(date_str) > 10:
                        # Убираем время (например, '2020-09-25 00:00' или '2020-09-25-01-01')
                        if ' ' in date_str or '-' in date_str[-5:]:
                            # Убираем '-01-01' или время
                            date_str = date_str[:10]
                        # Убираем лишнюю точку, если она есть в конце (например, "12.1987.")
                        if date_str[-1] == '.':
                            date_str = date_str[:-1]
                return date_str

            def remove_time_from_date(data):
                """
                Убирает время из дат, если оно присутствует, и возвращает только дату в формате YYYY-MM-DD.
                """
                if isinstance(data, pd.Timestamp):
                    return data.strftime('%Y-%m-%d')
                if isinstance(data, str):
                    data = fix_excel_date_format(data)  # Убираем суффикс "-01-01" и время
                    if '/' in data:  # Если дата записана через "/", меняем разделитель
                        data = data.replace('/', '.')
                return data

            # Функция для определения типа RV
            def normalize_rv_type(vaccine_type):
                """
                Преобразует типы RV с числами в общий тип RV, если число не равно 1.
                """
                match = re.match(r'(?i)(rv)(\d+)', vaccine_type)  # Ищем RV с числом
                if match:
                    base_type, number = match.groups()
                    if number != "1":  # Если число не равно 1
                        return base_type.lower()  # Преобразуем в RV
                return vaccine_type.lower()  # Возвращаем исходный тип в верхнем регистре

            # Основной цикл обработки данных
            for vaccine, data in vaccinations.items():
                if pd.notna(data):
                    data = str(data).strip()
                    records = re.split(r'[;\,\s]+', data)

                    vaccine_dates = []
                    current_type = None
                    last_valid_date = None
                    last_valid_type = None
                    invalid_data_found = False

                    for record in records:
                        record = record.strip()
                        if not record:
                            continue

                        # Убираем время из записи
                        record = remove_time_from_date(record)

                        # Если это тип прививки
                        if re.match(r'(?i)rv\d+|rv|v\d+|v', record):  # Поиск типа RV или V с числом
                            current_type = normalize_rv_type(record)  # Нормализуем тип RV
                            continue

                        # Если это дата
                        try:
                            if re.match(date_pattern, record):
                                # Для двухзначных годов
                                if len(record.split('.')[-1]) == 2:
                                    record = record[:-2] + '20' + record[-2:]

                                # Проверяем на корректность даты перед её обработкой
                                date_parsed = is_valid_date(record)
                                if date_parsed:
                                    last_valid_date = date_parsed
                                    last_valid_type = current_type  # Используем текущий тип
                                    print(f"Parsed valid date: {last_valid_date}")
                                else:
                                    invalid_data_found = True
                                    print(f"Invalid date detected: {record}")
                                    break

                            # Если это месяц и год (например, "12.2000"), то добавляем только месяц и год
                            elif re.search(month_year_pattern, record):
                                month, year = record.split('.')
                                date_parsed = f"{year}-{month.zfill(2)}-01"
                                last_valid_date = date_parsed
                                last_valid_type = current_type
                                print(f"Parsed month/year date: {last_valid_date}")

                            # Если это только год с "г" или без него
                            elif re.search(year_pattern, record):
                                record = record.strip('.').replace('г', '').strip()  # Убираем "г"
                                date_parsed = f"{record}-01-01"
                                last_valid_date = date_parsed
                                last_valid_type = current_type
                                print(f"Parsed year-only date: {last_valid_date}")

                            # Обработка строки типа "переболела 12.2000. Запись в ПС"
                            elif re.search(r'переболела|переболел|антитела|полож|со слов|отказ|сертификат|данные|ат',
                                           record, re.IGNORECASE):
                                # Пытаемся найти дату в формате "день.месяц.год" или "месяц.год"
                                date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', record)
                                if date_match:
                                    # Если дата в формате "день.месяц.год" (например, "12.2000")
                                    date_parsed = is_valid_date(date_match.group(1))
                                    if date_parsed:
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'
                                        print(f"Parsed date from 'переболела': {last_valid_date}")
                                else:
                                    # Если нет полной даты, ищем только месяц и год (например, "12.2000")
                                    date_match = re.search(r'(\d{2}\.\d{4})', record)
                                    if date_match:
                                        month, year = date_match.group(1).split('.')
                                        date_parsed = f"{year}-{month.zfill(2)}-01"  # Форматируем в "yyyy-mm-01"
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'
                                        print(f"Parsed month/year date from 'переболела': {last_valid_date}")
                                    else:
                                        # Если нет даты вообще, ставим дефолтную дату
                                        date_parsed = '2001-01-01'  # Если нет даты, ставим дефолтную дату
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'
                                        print(f"Set default date '2001-01-01' for record: {record}")

                                    # Дополнительная проверка для строк, содержащих только год (например, "1982")
                                    if not last_valid_date:
                                        year_match = re.search(r'(\d{4})', record)
                                        if year_match:
                                            year = year_match.group(1)
                                            date_parsed = f"{year}-01-01"  # Если только год, ставим "yyyy-01-01"
                                            last_valid_date = date_parsed
                                            last_valid_type = 'ant'
                                            print(f"Set default date 'yyyy-01-01' for record with only year: {record}")

                        except Exception as e:
                            print(f"Error processing date {record}: {e}")

                    # Если найдена некорректная дата в последней ячейке, пропускаем запись
                    if invalid_data_found:
                        print(f"Skipped: Invalid data found in vaccine {vaccine}")
                        continue  # Пропускаем всю запись, если найдена некорректная дата

                    # После получения даты, перед её вставкой в базу данных, проверяем и исправляем формат
                    if last_valid_date:
                        # Если прививка относится к ежегодным, ставим тип "v", если тип не был указан
                        if vaccine in annual_vaccinations and last_valid_type is None:
                            last_valid_type = 'v'

                        # Обработка данных для НКВИ
                        if vaccine == 'НКВИ':
                            last_valid_type = 'v'  # Устанавливаем тип 'v' для НКВИ, если тип не указан

                        # Добавляем тип 'ant' для записей, где нет типа
                        if last_valid_type is None:
                            last_valid_type = 'ant'

                        # Выводим дату перед вставкой только для работника с ID 6
                        if worker_id == 6:
                            print(
                                f"Prepared for insert - Worker ID: {worker_id}, Vaccine: {vaccine}, Date: {last_valid_date}, Type: {last_valid_type}")

                        # Убираем лишние части из даты, если они присутствуют
                        last_valid_date = fix_excel_date_format(last_valid_date)

                        # Если дата записана в формате "dd.mm.yyyy", преобразуем её в "yyyy-mm-dd"
                        if re.match(r'\d{2}\.\d{2}\.\d{4}', last_valid_date):
                            day, month, year = last_valid_date.split('.')
                            last_valid_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                            print(f"Converted date to 'yyyy-mm-dd': {last_valid_date}")

                        # Убедимся, что дата имеет правильный формат "yyyy-mm-dd"
                        if len(last_valid_date) != 10 or not re.match(r'^\d{4}-\d{2}-\d{2}$', last_valid_date):
                            print(
                                f"Invalid date format detected for Worker ID {worker_id}, Vaccine {vaccine}, Date {last_valid_date}")
                            continue  # Пропускаем запись с некорректной датой

                        # Проверяем, существует ли запись в базе данных
                        vaccine_name = vaccination_mapping.get(vaccine, vaccine)
                        cursor.execute(""" 
                            SELECT 1 FROM immunization
                            WHERE workerID = ? AND vaccination = ? AND date = ? AND type = ? 
                        """, (worker_id, vaccine_name, last_valid_date, last_valid_type))
                        exists = cursor.fetchone()

                        # Если записи нет, вставляем новую
                        try:
                            if not exists:
                                cursor.execute(""" 
                                    INSERT INTO immunization (workerID, vaccination, date, type) 
                                    VALUES (?, ?, ?, ?) 
                                """, (worker_id, vaccine_name, last_valid_date, last_valid_type))
                                print(
                                    f"Inserted: Worker ID {worker_id}, Vaccine {vaccine}, Date {last_valid_date}, Type {last_valid_type}")
                        except Exception as e:
                            print(f"Error inserting data: {e}")

                    # Если найдена некорректная дата в последней ячейке, пропускаем запись
                    if invalid_data_found:
                        print(f"Skipped: Invalid data found in vaccine {vaccine}")
                        continue  # Пропускаем всю запись, если найдена некорректная дата

                    # После получения даты, перед её вставкой в базу данных, проверяем и исправляем формат
                    if last_valid_date:
                        # Если прививка относится к ежегодным, ставим тип "v", если тип не был указан
                        if vaccine in annual_vaccinations and last_valid_type is None:
                            last_valid_type = 'v'

                        # Обработка данных для НКВИ
                        if vaccine == 'НКВИ':
                            last_valid_type = 'v'  # Устанавливаем тип 'v' для НКВИ, если тип не указан

                        # Выводим дату перед вставкой только для работника с ID 6
                        if worker_id == 6:
                            print(
                                f"Prepared for insert - Worker ID: {worker_id}, Vaccine: {vaccine}, Date: {last_valid_date}, Type: {last_valid_type}")

                        # Убираем лишние части из даты, если они присутствуют
                        last_valid_date = fix_excel_date_format(last_valid_date)

                        # Если дата записана в формате "dd.mm.yyyy", преобразуем её в "yyyy-mm-dd"
                        if re.match(r'\d{2}\.\d{2}\.\d{4}', last_valid_date):
                            day, month, year = last_valid_date.split('.')
                            last_valid_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                            print(f"Converted date to 'yyyy-mm-dd': {last_valid_date}")

                        # Убедимся, что дата имеет правильный формат "yyyy-mm-dd"
                        if len(last_valid_date) != 10 or not re.match(r'^\d{4}-\d{2}-\d{2}$', last_valid_date):
                            print(
                                f"Invalid date format detected for Worker ID {worker_id}, Vaccine {vaccine}, Date {last_valid_date}")
                            continue  # Пропускаем запись с некорректной датой

                        # Проверяем, существует ли запись в базе данных
                        vaccine_name = vaccination_mapping.get(vaccine, vaccine)
                        cursor.execute(""" 
                            SELECT 1 FROM immunization
                            WHERE workerID = ? AND vaccination = ? AND date = ? AND type = ? 
                        """, (worker_id, vaccine_name, last_valid_date, last_valid_type))
                        exists = cursor.fetchone()

                        # Если записи нет, вставляем новую
                        try:
                            if not exists:
                                cursor.execute(""" 
                                    INSERT INTO immunization (workerID, vaccination, date, type)
                                    VALUES (?, ?, ?, ?) 
                                """, (worker_id, vaccine_name, last_valid_date, last_valid_type))
                                print(
                                    f"Inserted: Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_valid_date}, Type {last_valid_type}")
                            else:
                                print(
                                    f"Record exists: Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_valid_date}, Type {last_valid_type}")
                        except Exception as e:
                            print(
                                f"Error inserting data into DB: {e} for Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_valid_date}, Type {last_valid_type}")
                        except Exception as e:
                            print(
                                f"Error inserting data into DB: {e} for Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_valid_date}, Type {last_valid_type}")


            # --- Обработка столбца "Гепатит А" ---
            if pd.notna(row['Гепатит А']):
                data = str(row['Гепатит А']).strip()

                # Инициализация значений
                last_date = None
                last_type = None

                # Проверка на даты в формате ДД.ММ.ГГГГ или ДД.ММ.ГГ
                if re.search(r'\d{2}\.\d{2}\.\d{2,4}', data):  # Если есть даты (двух- или четырехзначный год)
                    matches = re.findall(r'(\b(?:V|V1|V2|V3|RV|RV1|RV2)\b)?\s*(\d{2}\.\d{2}\.\d{2,4})', data)
                    for type_, date in matches:
                        try:
                            if date:
                                # Проверка года и преобразование в четырехзначный формат
                                day, month, year = date.split('.')
                                if len(year) == 2:
                                    year = '20' + year  # Добавляем 20 перед двухзначным годом
                                date_parsed = pd.to_datetime(f"{day}.{month}.{year}", dayfirst=True).strftime(
                                    '%Y-%m-%d')

                                if not type_:  # Если тип не указан, задаём тип по умолчанию
                                    type_ = 'ant'
                                else:
                                    type_ = type_.lower()

                                # Обновление последней даты и типа
                                if last_date is None or date_parsed > last_date:
                                    last_date = date_parsed
                                    last_type = type_
                        except Exception as e:
                            error_msg = f"Error processing date {date} in data: {data}, Error: {e}"
                            logging.error(error_msg)
                            error_log.append(error_msg)

                # Проверка на строки с годом и месяцем (например, "10.2018" или "от 02.2019")
                if not last_date:
                    # Ищем год и месяц, например "10.2018"
                    month_year_match = re.search(r'(\d{2})\.(\d{4})', data)
                    if month_year_match:
                        month, year = month_year_match.groups()
                        last_date = f"{year}-{month}-01"  # Формируем дату вида ГГГГ-ММ-01
                        last_type = 'ant'
                    else:
                        # Ищем только год, например "2018" или "2019"
                        year_match = re.search(r'(\d{4})', data)
                        if year_match:
                            year = year_match.group(1)
                            last_date = f"{year}-01-01"  # Формируем дату вида ГГГГ-01-01
                            last_type = 'ant'
                        else:
                            # Если нет даты, года или месяца, ставим дату по умолчанию
                            if re.search(r'отказ|не получено|нет данных|\+|переболела|м/о', data, re.IGNORECASE):
                                last_date = '2001-01-01'  # Устанавливаем дефолтную дату
                                last_type = 'ant'
                            elif re.search(r'антитела обнаружены|ат положительные|ат \+|антитела \+|положительные',
                                           data, re.IGNORECASE):
                                last_date = '2001-01-01'
                                last_type = 'ant'

                # Добавление данных в таблицу
                if last_date and last_type:
                    vaccine_name = 'hepatitisA'

                    cursor.execute(
                        """SELECT 1 FROM immunization WHERE workerID = ? AND vaccination = ? AND date = ? AND type = ?""",
                        (worker_id, vaccine_name, last_date, last_type))
                    exists = cursor.fetchone()

                    if not exists:
                        cursor.execute(
                            """INSERT INTO immunization (workerID, vaccination, date, type) VALUES (?, ?, ?, ?)""",
                            (worker_id, vaccine_name, last_date, last_type))
                        logging.info(
                            f"Inserted: Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_date}, Type {last_type}")
                else:
                    # Логируем ошибку, если не удается найти дату или тип
                    error_msg = f"Failed to process data for Worker ID {worker_id}. Data: {data}"
                    logging.warning(error_msg)
                    error_log.append(error_msg)
            else:
                # Если значение NaN, игнорируем
                logging.info(f"Skipped empty or NaN value for Worker ID {worker_id}")

            # --- Обработка столбца "Пневмо" ---
            if pd.notna(row['Пневмо']):
                data = str(row['Пневмо']).strip()

                # Преобразование данных с удалением времени
                if isinstance(row['Пневмо'], pd.Timestamp):
                    data = row['Пневмо'].strftime('%Y-%m-%d')
                elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', data):
                    data = data.split(' ')[0]

                # Маппинг месяцев
                month_mapping = {
                    'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04', 'май': '05',
                    'июнь': '06', 'июль': '07', 'август': '08', 'сентябрь': '09', 'октябрь': '10',
                    'ноябрь': '11', 'декабрь': '12'
                }

                # Регулярные выражения для проверки форматов
                text_date_pattern = re.compile(
                    r'(\b(?:RV|V|RV1|V1|V2|V3)\b)?\s*(\(?ППВ-23\)?)?\s*([а-яА-Я]+)\s*(\d{4})', re.IGNORECASE)
                standard_date_pattern = re.compile(r'(\b(?:RV|V|RV1|V1|V2|V3)\b)?\s*(\d{2}\.\d{2}\.\d{2,4})')
                combined_date_pattern = re.compile(r'(\d{2}\.\d{2}\.\d{2,4})(?:,?\s*(\d{2}\.\d{2}\.\d{2,4}))?')
                iso_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

                # Переменные для хранения последней даты и типа
                last_date = None
                last_type = None

                # Проверка строк, содержащих только время
                if re.fullmatch(r'\d{2}:\d{2}:\d{2}', data) or data == '00:00:00':
                    logging.warning(f"Invalid vaccine record (time only): {data}. Worker ID: {worker_id}")
                    continue

                # Обработка дат в формате ISO
                if iso_date_pattern.match(data):
                    last_date = data
                    last_type = last_type or 'v1'

                # Обработка дат с текстовыми месяцами
                for match in text_date_pattern.finditer(data):
                    type_ = match.group(1)
                    month_text = match.group(3).lower()
                    year = match.group(4)

                    if month_text in month_mapping:
                        month = month_mapping[month_text]
                        date_parsed = f"{year}-{month}-01"
                        type_ = type_.lower() if type_ else 'v1'

                        if last_date is None or date_parsed > last_date:
                            last_date = date_parsed
                            last_type = type_

                # Обработка стандартных дат
                for match in standard_date_pattern.finditer(data):
                    type_ = match.group(1)
                    date = match.group(2)

                    try:
                        if len(date.split('.')[-1]) == 2:
                            date = date[:-2] + '20' + date[-2:]
                        date_parsed = pd.to_datetime(date, dayfirst=True).strftime('%Y-%m-%d')
                        type_ = type_.lower() if type_ else 'v1'

                        if last_date is None or date_parsed > last_date:
                            last_date = date_parsed
                            last_type = type_
                    except Exception as e:
                        error_msg = f"Error processing date {date} in data: {data}, Error: {e}"
                        logging.error(error_msg)
                        error_log.append(error_msg)

                # Обработка комбинированных дат
                for match in combined_date_pattern.finditer(data):
                    for date in match.groups():
                        if date:
                            try:
                                if len(date.split('.')[-1]) == 2:
                                    date = date[:-2] + '20' + date[-2:]
                                date_parsed = pd.to_datetime(date, dayfirst=True).strftime('%Y-%m-%d')

                                if last_date is None or date_parsed > last_date:
                                    last_date = date_parsed
                                    last_type = 'v1'
                            except Exception as e:
                                error_msg = f"Error processing date {date} in data: {data}, Error: {e}"
                                logging.error(error_msg)
                                error_log.append(error_msg)

                # Проверка на наличие валидных данных
                if last_date and last_type:
                    vaccine_name = 'pneumococcalInfection'

                    cursor.execute("""
                        SELECT 1 FROM immunization
                        WHERE workerID = ? AND vaccination = ? AND date = ? AND type = ?
                    """, (worker_id, vaccine_name, last_date, last_type))
                    exists = cursor.fetchone()

                    if not exists:
                        cursor.execute("""
                            INSERT INTO immunization (workerID, vaccination, date, type)
                            VALUES (?, ?, ?, ?)
                        """, (worker_id, vaccine_name, last_date, last_type))
                        logging.info(
                            f"Inserted: Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_date}, Type {last_type}")
                else:
                    if not last_date:
                        error_msg = f"Invalid date format or missing date: {data}. Worker ID: {worker_id}"
                    elif not last_type:
                        error_msg = f"Missing type for date {last_date}. Data: {data}. Worker ID: {worker_id}"
                    logging.warning(error_msg)
                    error_log.append(error_msg)

                # Обработка столбца "НКВИ"
                if pd.notna(row['НКВИ']):
                    data = str(row['НКВИ']).strip()

                    # Инициализация значений
                    last_date = None
                    last_type = None

                    # Обработка значений "НКВИ"
                    matches = re.findall(
                        r'(ковид \d{2}\.\d{2}\.\d{4}г\. 1 компонент)|((?:V|V1|V2|RV|RV1|RV2)?\s*\d{2}\.\d{2}\.\d{2,4})',
                        data)
                    for match in matches:
                        if match[0]:  # Обработка текста "ковид"
                            covid_data = match[0]
                            date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', covid_data)
                            if date_match:
                                date_parsed = pd.to_datetime(date_match.group(1), dayfirst=True).strftime('%Y-%m-%d')
                                last_date = date_parsed
                                last_type = 'v'

                    # Добавление данных в базу
                    if last_date and last_type:
                        vaccine_name = 'nkwi'
                        cursor.execute(
                            """SELECT 1 FROM immunization WHERE workerID = ? AND vaccination = ? AND date = ? AND type = ?""",
                            (worker_id, vaccine_name, last_date, last_type))
                        exists = cursor.fetchone()

                        if not exists:
                            cursor.execute(
                                """INSERT INTO immunization (workerID, vaccination, date, type) VALUES (?, ?, ?, ?)""",
                                (worker_id, vaccine_name, last_date, last_type))
                            logging.info(
                                f"Inserted: Worker ID {worker_id}, Vaccine {vaccine_name}, Date {last_date}, Type {last_type}")
                    else:
                        error_msg = f"Failed to process data for Worker ID {worker_id}. Data: {data}"
                        logging.warning(error_msg)
                        error_log.append(error_msg)



        except Exception as e:
            print(f"Error processing row {index}: {e}")

    # Установим локаль для корректной обработки чисел с запятой
    locale.setlocale(locale.LC_NUMERIC, 'ru_RU.UTF-8')  # или используйте локаль вашей системы

    # Проверяем, существует ли столбец с показателями
    if 'показатель anti-hbs октябрь 2023 мме/мл' in df.columns:
        # Очистка и преобразование значений столбца в числовой формат
        def convert_to_numeric(value):
            try:
                if pd.isna(value):
                    return value  # Пропускаем NaN
                if isinstance(value, str):
                    value = value.replace(' ', '').replace(',', '.').replace('>', '')  # Убираем пробелы и запятые
                return pd.to_numeric(value, errors='coerce')  # Преобразуем в число или NaN
            except Exception as e:
                print(f"Ошибка преобразования значения: {value} - {e}")
                return None

        df['показатель anti-hbs октябрь 2023 мме/мл'] = df['показатель anti-hbs октябрь 2023 мме/мл'].apply(
            convert_to_numeric)
    else:
        print("Столбец 'показатель anti-hbs октябрь 2023 мме/мл' отсутствует в данных.")

    # Вставка данных в таблицу indicatorAntiHBs
    for index, row in df.iterrows():
        try:
            # Получаем ID сотрудника через фамилию, имя, отчество и дату рождения
            cursor.execute("""
                SELECT ID FROM worker
                WHERE firstname = ? AND name = ? AND lastname = ? AND dateOfBirth = ?
            """, (row['Фамилия'].strip(), row['Имя'].strip(), row['Отчество'].strip(), row['Дата рождения']))
            worker = cursor.fetchone()

            if not worker:
                print(f"Worker not found: {row['Фамилия']} {row['Имя']} {row['Отчество']}")
                continue

            worker_id = worker[0]

            # Получаем показатель Anti-HBs
            anti_hbs_indicator = row.get('показатель anti-hbs октябрь 2023 мме/мл')

            if pd.notna(anti_hbs_indicator):  # Проверяем на nan
                if isinstance(anti_hbs_indicator, str):
                    # Обрабатываем значения с ">"
                    if ">" in anti_hbs_indicator:
                        date = pd.to_datetime("2023-10-01", dayfirst=True, errors='coerce').strftime('%Y-%m-%d')
                        value = 1001.0  # Преобразуем >1000 в 1001
                    else:
                        # Извлечение даты и значения из строки
                        parts = anti_hbs_indicator.split()
                        if len(parts) == 2:
                            date = pd.to_datetime(parts[0], dayfirst=True, errors='coerce').strftime('%Y-%m-%d')

                            # Преобразуем строку в число, обрабатывая как текст
                            try:
                                # Убираем все пробелы и заменяем запятую на точку
                                value_str = parts[1].replace(' ', '').replace(',', '.')

                                # Преобразуем в float, если это возможно
                                value = float(value_str)  # Преобразование в float для REAL

                                print(f"Parsed value for {worker_id}: {value}")  # Логирование
                            except ValueError as e:
                                print(f"Ошибка при преобразовании значения: {parts[1]} для Worker ID {worker_id} - {e}")
                                continue
                        else:
                            print(f"Некорректный формат данных: {anti_hbs_indicator} для Worker ID {worker_id}")
                            continue
                elif isinstance(anti_hbs_indicator, (int, float)):
                    date = '2023-10-01'
                    value = float(anti_hbs_indicator)

                # Проверка, что значение корректное
                if isinstance(value, (int, float)):
                    # Обновление или вставка данных в базу
                    cursor.execute("""
                        UPDATE indicatorAntiHBs
                        SET value = ?
                        WHERE workerID = ? AND date = ?
                    """, (value, worker_id, date))

                    # Если обновление не произошло, вставляем новую запись
                    if cursor.rowcount == 0:
                        cursor.execute("""
                            INSERT INTO indicatorAntiHBs (workerID, date, value)
                            VALUES (?, ?, ?)
                        """, (worker_id, date, value))

                    print(f"Processed indicatorAntiHBs for Worker ID: {worker_id}, Date: {date}, Value: {value}")
                else:
                    print(f"Некорректное значение для Worker ID {worker_id}, значение: {value}")
            else:
                print(f"Missing data for Worker ID: {worker_id}, value: nan")

        except Exception as e:
            print(f"Error processing indicatorAntiHBs for Worker ID: {worker_id}, value: {anti_hbs_indicator} - {e}")

    # Сохранение изменений в базе данных
    conn.commit()
    conn.close()

    # Обновление таблицы в интерфейсе, если передан tableWidget
    # Обновление таблицы в интерфейсе, если передан tableWidget
    if tableWidget:
        tableWidget.setRowCount(len(df))
        tableWidget.setColumnCount(7)
        tableWidget.setHorizontalHeaderLabels(
            ["Фамилия", "Имя", "Отчество", "Должность", "Подразделение", "Краткое название", "Статус"]
        )

        for i, row in df.iterrows():
            tableWidget.setItem(i, 0, QTableWidgetItem(str(row['Фамилия'])))
            tableWidget.setItem(i, 1, QTableWidgetItem(str(row['Имя'])))
            tableWidget.setItem(i, 2, QTableWidgetItem(str(row['Отчество'])))
            tableWidget.setItem(i, 3, QTableWidgetItem(str(row['Штатная должность'])))
            tableWidget.setItem(i, 4, QTableWidgetItem(str(row['Штатное подразделение'])))
            tableWidget.setItem(i, 5, QTableWidgetItem(str(row['Краткое название'])))
            tableWidget.setItem(i, 6, QTableWidgetItem(str(row['Статус'])))


# Пример использования
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    file_path = r'C:\Users\User\PycharmProjects\pdf_generation\Копия_Список_сотрудников_для_планирования_вакцинации_с_указанием1.xlsx'
    base_path = r'C:\Users\User\PycharmProjects\PDF_gen3\database.db'

    # Пример вызова функции с tableWidget
    tableWidget = QTableWidget()  # Создаем таблицу для примера
    process_excel_to_sqlite(file_path, base_path, tableWidget)

    # Отображение таблицы (для примера)
    tableWidget.show()
    sys.exit(app.exec())

def print_errors():
    if error_log:
        print("\nErrors during processing:")
        for error in error_log:
            print(error)
    else:
        print("No errors during processing.")
print_errors()


