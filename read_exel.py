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



def process_excel_to_sqlite(file_path, base_path):
    # Чтение данных из Excel файла
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        raise

    # Приведение всех имен столбцов к нижнему регистру для унификации
    df.columns = df.columns.str.strip().str.lower()  # Убираем пробелы и приводим к нижнему регистру
    print("Columns after normalization:", df.columns)
    print(df.columns)
    # Проверка наличия столбцов с "unnamed"
    unnamed_columns = [col for col in df.columns if 'unnamed' in col]
    if unnamed_columns:
        for unnamed_col in unnamed_columns:
            # Переименовываем столбец 'unnamed' в более осмысленное имя, например 'статус'
            df.rename(columns={unnamed_col: 'статус'}, inplace=True)
        print(f"Renamed columns {unnamed_columns} to 'статус'.")
    else:
        print("No unnamed columns found.")

    # Проверка наличия столбца 'статус'
    if 'статус' not in df.columns:
        print("Столбец 'Статус' не найден в Excel. Используется значение по умолчанию.")
        df['статус'] = None  # Если столбца 'статус' нет, добавляем с пустыми значениями

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

    sphere_dict = {
        "medical": [
            "Врач-челюстно-лицевой хирург",
            "Врач-офтальмолог",
            "Врач-невролог",
            "Врач-анестезиолог-реаниматолог",
            "Врач-акушер-гинеколог",
            "Врач-оториноларинголог",
            "Врач-педиатр",
            "Врач-методист",
            "Врач-физиотерапевт",
            "Врач-специалист",
            "Врач-психиатр",
            "Врач-сурдолог-оториноларинголог",
            "Заведующий стоматологической поликлиникой, врач-стоматолог детский",
            "Врач-ортодонт",
            "Врач-стоматолог",
            "Заведующий консультативно-диагностической поликлиникой№1, врач -педиатр",
            "Заведующий отделением, врач-педиатр",
            "Медицинская сестра палатная",
            "Врач-травматолог-ортопед",
            "Заведующий отделением, врач-невролог",
            "Инструктор-методист по лечебной физкультуре",
            "Врач-пластический хирург",
            "Заведующий отделением, врач по лечебной физкультуре",
            "Врач по спортивной медицине и лечебной физкультуре",
            "Медицинская сестра",
            "Медицинская сестра-анестезист",
            "Медицинская сестра процедурной",
            "Медицинская сестра палатная",
            "Медицинская сестра по физиотерапии",
            "Медицинская сестра диетическая",
            "Медицинская сестра функциональной диагностики",
            "Медицинская сестра операционная",
            "Старшая медицинская сестра",
            "Медицинский брат",
            "Медицинский брат по массажу",
            "Медицинский лабораторный техник",
            "Логопед",
            "Инструктор-методист по ЛФК",
            "Инструктор методист",
            "Клинический психолог",
            "Санитарка",
            "Массажист",
            "Заместитель главного врача по лечебной работе",
            "Помощник врача-эпидемиолога",
            "Заведующий отделением, врач-офтальмолог",
            "Заведующий отделением, врач-физиотерапевт",
            "Заведующий отделением, врач-анестезиолог -реаниматолог",
            "Заведующий отделением, врач функциональной диагностики",
            "Заведующий отделением функциональной диагностики, врач функциональной диагностики",
            "Старшая операционная  медицинская сестра",
            "Главный врач",
            "Заведующий отделением, врач-методист",
            "Врач функциональной диагностики",
            "Медицинская сестра по массажу",
            "Врач-стоматолог-ортопед",
            "Заведующий отделением, врач-анестезиолог -реаниматолог",
            "Врач",
            "Врач функциональной диагностики",
            "Главная медицинская сестра",
            "Врач-стажёр",
            "Врач-стоматолог-детский",
            "Врач-дерматовенеролог",
            "Сурдопедагог",
            "Медицинский психолог",
            "Врач-эндокринолог",
            "Врач-кардиолог",
            "Врач-хирург",
            "Врач-терапевт",
            "Врач-инфекционист",
            "Врач-генетик",
            "Врач-диетолог",
            "Врач-уролог",
            "Врач-реаниматолог",
            "Врач-аллерголог",
            "Врач-гематолог"
        ],
        "foodService": [
            "Кухонный рабочий",
            "Повар",
            "Буфетчик",
            "Заведующий производством",
            "Мойщик посуды",
            "Технолог общественного питания",
            "Консервщик",
            "Пекарь",
            "Кондитер",
            "кух.рабочий"
        ],
        "utilityService": [
            "Подсобный рабочий",
            "Уборщик произ и служеб помещений",
            "Уборщик производственных помещений",
            "Уборщик производственных и служебных помещений",
            "Гардеробщик",
            "Вахтер",
            "Дворник",
            "Слесарь-сантехник",
            "Кастелянша",
            "Плотник",
            "Кочегар",
            "Машинист котельной (кочегар)",
            "Заведующий хозяйством",
            "Разнорабочий",
            "Электромонтер по ремонту и обслуживанию",
            "Маляр",
            "Штукатур",
            "Электрик",
            "Столяр",
            "Техник по обслуживанию зданий",
            "Заведующий складом"
            "Контролёр технического состояния"

        ],
    }

    # Определение пола по отчеству
    def determine_gender(patronymic):
        # Если отчество состоит из двух слов (например, "Камил оглы" или "Фирдоси кызы")
        if "оглы" in patronymic:
            return "m"
        elif "кызы" in patronymic:
            return "w"
        # Если отчество заканчивается на "ич" (например, "Александрович")
        elif patronymic.endswith("ич"):
            return "m"
        # Если отчество заканчивается на "на" (например, "Александровна")
        elif patronymic.endswith("на"):
            return "w"
        return "Неизвестно"  # На всякий случай на случай некорректных данных

    # Преобразуем все профессии в словаре в нижний регистр
    sphere_dict_lower = {
        sphere: [profession.lower() for profession in professions]
        for sphere, professions in sphere_dict.items()
    }

    # Функция для определения сферы по должности
    def determine_sphere(name):
        name = name.lower()  # Приводим входное значение к нижнему регистру
        for sphere, professions in sphere_dict_lower.items():
            if name in professions:
                return sphere
        return "nonMedical"

    # Словарь для преобразования текстовых месяцев в числа
    month_mapping = {
        'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04',
        'май': '05', 'июнь': '06', 'июль': '07', 'август': '08',
        'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'
    }

    # Функция парсинга текстовых дат
    def parse_custom_date(record):
        for month, num in month_mapping.items():
            if month in record.lower():
                year_match = re.search(r'(\d{4})', record)
                if year_match:
                    return f"01.{num}.{year_match.group(1)}"
        return None


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

        cursor.execute("DELETE FROM sqlite_sequence WHERE name='immunization'")  # Для таблицы Вакцинация
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='worker'")  # Для таблицы Должность
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='indicatorAntiHBs'")  # Для таблицы Показатель_AntiHBs
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='position'")  # Для таблицы Показатель_AntiHBs

        print("Reset auto-increment counters for all tables.")
    except Exception as e:
        print(f"Error deleting data from tables: {e}")
        conn.rollback()  # Откатить транзакцию в случае ошибки
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
        # Приведение значений к ожидаемым форматам
        name = normalize_value(row['Штатная должность']) if pd.notnull(row['Штатная должность']) else None
        area_of_work = determine_sphere(name) if name else None
        division = normalize_value(row['Штатное подразделение']) if pd.notnull(row['Штатное подразделение']) else None
        short_title = normalize_value(row['Краткое название']) if pd.notnull(row['Краткое название']) else None

        try:
            print(
                f"Processing row {index}: name={name}, division={division}, short_title={short_title}, area_of_work={area_of_work}")

            # Проверка существования записи в таблице position
            cursor.execute("""
                SELECT ID FROM position
                WHERE name = ? AND division = ? AND shortTitle = ?
            """, (name, division, short_title))
            existing_record = cursor.fetchone()

            if existing_record:
                # Если запись существует, обновляем при необходимости
                cursor.execute("""
                    UPDATE position
                    SET areaOfWork = ?
                    WHERE name = ? AND division = ? AND shortTitle = ?
                """, (area_of_work, name, division, short_title))
                print(
                    f"Updated existing record: name={name}, division={division}, short_title={short_title}, area_of_work={area_of_work}")
            else:
                # Если записи нет, вставляем новую
                cursor.execute("""
                    INSERT INTO position (name, areaOfWork, division, shortTitle)
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
        'осн': 'key',  # Пример: "осн" преобразуется в "key"
        'врем': 'notKey',  # Если есть "врем", преобразуется в "notKey"
        'совм': 'notKey',
        'вне': 'notKey',
        'омн': 'notKey',
    }

    # Вставка или обновление данных в таблицу worker
    id_counter = 1  # Счётчик для генерации ID

    for _, row in df.iterrows():
        try:
            # Проверка наличия обязательных полей
            if pd.isna(row.get('Фамилия')) or pd.isna(row.get('Имя')) or pd.isna(row.get('Отчество')) or pd.isna(
                    row.get('Дата рождения')):
                print(f"Skipping row due to NULL value in required fields: {row.to_dict()}")
                continue

            # Приведение значения "Статус" к допустимым
            status = row.get('Статус')
            if status in status_mapping:
                status = status_mapping[status]  # Преобразуем значение через словарь
            elif status not in ['key', 'notKey']:
                print(f"Invalid status value: {status} in row: {row.to_dict()}")
                continue  # Пропускаем строки с некорректными значениями

            # Генерация ID должности (если информация о должности есть)
            query = "SELECT ID FROM position WHERE 1=1"
            params = []

            if not pd.isna(row.get('Штатная должность')):
                query += " AND name = ?"
                params.append(
                    row['Штатная должность'])  # Поле "Штатная должность" соответствует "name" в таблице position

            if not pd.isna(row.get('Штатное подразделение')):
                query += " AND division = ?"
                params.append(row['Штатное подразделение'])  # Поле "Штатное подразделение" соответствует "division"

            if not pd.isna(row.get('Краткое название')):
                query += " AND shortTitle = ?"
                params.append(row['Краткое название'])  # Поле "Краткое название" соответствует "shortTitle"

            # Выполнение запроса для определения позиции
            cursor.execute(query, params)
            position = cursor.fetchone()
            position_id = position[0] if position else None  # Получение ID должности или None, если запись не найдена

            # Определение пола
            gender = determine_gender(row.get('Отчество', ''))  # Функция определяет пол на основе отчества

            # Вставка или обновление данных сотрудника
            cursor.execute("""
                INSERT INTO worker (ID, firstname, lastname, name, gender, dateOfBirth, status, position)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ID) DO UPDATE SET
                    firstname = excluded.firstname,
                    lastname = excluded.lastname,
                    name = excluded.name,
                    gender = excluded.gender,
                    dateOfBirth = excluded.dateOfBirth,
                    status = excluded.status,
                    position = excluded.position
            """, (
                id_counter,  # Генерация ID
                row.get('Имя'),  # firstname
                row.get('Фамилия'),  # lastname
                row.get('Отчество'),  # name
                gender,  # gender
                row.get('Дата рождения'),  # dateOfBirth
                status,  # status
                position_id  # position (ID должности)
            ))

            print(f"Inserted or updated: ID {id_counter}, {row.get('Фамилия')}, {row.get('Имя')}")
            id_counter += 1  # Увеличение счётчика ID

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
                WHERE lastname = ? AND firstname = ? AND name = ? AND dateOfBirth = ?
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
                'Гепатит А': row['Гепатит А'],
                'Грипп': row['Грипп'],
                'Ветряная оспа': row['Ветряная оспа'],
                'ВПЧ': row['ВПЧ'],
                'Пневмо': row['Пневмо'],
                'НКВИ': row['НКВИ'],
            }

            annual_vaccinations = {'НКВИ', 'Шигеллвак', 'Грипп'}

            date_pattern = r'\d{2}\.\d{2}\.\d{2,4}'  # Паттерн для обычных дат
            month_year_pattern = r'\d{2}\.\d{4}'  # Паттерн для месяца и года
            year_pattern = r'\d{4}'  # Паттерн для только года
            allowed_types = {'rv', 'v', 'rv1', 'v1', 'v2', 'v3'}

            def is_valid_date(date_str):
                """Проверка на корректность даты и форматирование в YYYY-MM-DD"""
                try:
                    # Пробуем распарсить дату
                    parsed_date = pd.to_datetime(date_str, dayfirst=True)
                    # Возвращаем дату в формате YYYY-MM-DD
                    return parsed_date.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"Invalid date format: {date_str} Error: {e}")
                    return None

            for vaccine, data in vaccinations.items():
                if pd.notna(data):
                    data = str(data).strip()
                    records = re.split(r'[;\,\s]+', data)

                    vaccine_dates = []
                    current_type = None
                    last_valid_date = None
                    last_valid_type = None
                    invalid_data_found = False  # Флаг для некорректных данных в строке

                    for record in records:
                        record = record.strip()
                        if not record:
                            continue

                        # Обработка текста без дат (например, "отказ", "антитела")
                        if re.search(
                                r'отказ|не получено|нет данных|\+|переболела|м/о|положительные|антитела|ат|результат антител|перенес|положительные|со слов не болела',
                                record, re.IGNORECASE):
                            last_date = '2001-01-01'
                            last_type = 'ant'

                        # Если это тип прививки
                        elif record.lower() in allowed_types:
                            current_type = record.lower()
                            continue

                        # Обработка строки с датой и типом RV (например, RV21.04.2022)
                        if re.match(r'(rv|v|rv1|v1|v2|v3|rv2|rv3)(\d{2}\.\d{2}\.\d{4})', record, re.IGNORECASE):
                            type_match = re.match(r'(rv|v|rv1|v1|v2|v3)', record, re.IGNORECASE)
                            date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', record)
                            if type_match and date_match:
                                date_parsed = is_valid_date(date_match.group(1))
                                if date_parsed:
                                    last_valid_date = date_parsed
                                    last_valid_type = type_match.group(1).lower()

                        # Ошибочное добавление частей даты "01-01" в конец
                        if re.match(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}',
                                    record):  # Обнаружена ошибка с добавлением лишних частей
                            print(f"Error: Incorrect date format detected: {record}")
                            # Исправляем формат даты
                            record = record[:10]  # Оставляем только корректный формат "yyyy-mm-dd"
                            date_parsed = is_valid_date(record)
                            if date_parsed:
                                last_valid_date = date_parsed
                                last_valid_type = current_type
                            else:
                                print(f"Skipped due to invalid date format: {record}")
                                continue  # Пропускаем эту запись

                        # Если это дата
                        try:
                            if re.match(date_pattern, record):
                                # Для двухзначных годов
                                if len(record.split('.')[-1]) == 2:
                                    record = record[:-2] + '20' + record[-2:]

                                # Проверяем на корректность даты перед её обработкой
                                date_parsed = is_valid_date(record)
                                if date_parsed:
                                    last_valid_date = date_parsed  # Обновляем последнюю валидную дату
                                    last_valid_type = current_type  # Обновляем тип для последней валидной даты
                                else:
                                    invalid_data_found = True  # Найдена некорректная дата
                                    break  # Прерываем обработку, чтобы пропустить эту строку

                            # Если это месяц и год (например, "12.2000"), то добавляем только месяц и год
                            elif re.search(month_year_pattern, record):
                                month, year = record.split('.')
                                date_parsed = f"{year}-{month.zfill(2)}-01"
                                last_valid_date = date_parsed
                                last_valid_type = current_type

                            # Если это только год (например, "2000"), добавляем только год с месяцем и днем = 01
                            elif re.search(year_pattern, record):
                                date_parsed = f"{record}-01-01"
                                last_valid_date = date_parsed
                                last_valid_type = current_type

                            # Обработка строки типа "переболела 12.2000. Запись в ПС"
                            elif re.search(r'переболела|переболел|антитела|полож|со слов|отказ|сертификат|данные',
                                           record, re.IGNORECASE):
                                # Пытаемся найти дату в формате "день.месяц.год" или "месяц.год"
                                date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', record)
                                if date_match:
                                    # Если дата в формате "день.месяц.год" (например, "12.2000")
                                    date_parsed = is_valid_date(date_match.group(1))
                                    if date_parsed:
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'
                                else:
                                    # Если нет полной даты, ищем только месяц и год (например, "12.2000")
                                    date_match = re.search(r'(\d{2}\.\d{4})', record)
                                    if date_match:
                                        month, year = date_match.group(1).split('.')
                                        date_parsed = f"{year}-{month.zfill(2)}-01"  # Форматируем в "yyyy-mm-01"
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'
                                    else:
                                        # Если нет даты вообще, ставим дефолтную дату
                                        date_parsed = '2001-01-01'  # Если нет даты, ставим дефолтную дату
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'

                                # Дополнительная проверка для строк, содержащих только год (например, "1982")
                                if not last_valid_date:
                                    year_match = re.search(r'(\d{4})', record)
                                    if year_match:
                                        year = year_match.group(1)
                                        date_parsed = f"{year}-01-01"  # Если только год, ставим "yyyy-01-01"
                                        last_valid_date = date_parsed
                                        last_valid_type = 'ant'

                        except Exception as e:
                            print(f"Error processing date {record}: {e}")

                    # Если найдена некорректная дата в последней ячейке, пропускаем запись
                    if invalid_data_found:
                        print(f"Skipped: Invalid data found in vaccine {vaccine}")
                        continue  # Пропускаем всю запись, если найдена некорректная дата

                    # После получения даты, перед её вставкой в базу данных, проверяем и исправляем формат
                    # После получения даты, перед её вставкой в базу данных, проверяем и исправляем формат
                    # После получения даты, перед её вставкой в базу данных, проверяем и исправляем формат
                    if last_valid_date:
                        # Выводим дату перед вставкой только для работника с ID 6
                        if worker_id == 6:
                            print(
                                f"Prepared for insert - Worker ID: {worker_id}, Vaccine: {vaccine}, Date: {last_valid_date}, Type: {last_valid_type}")

                        # Убираем лишние части из даты, если они присутствуют, но только для ежегодных дат вида "yyyy-mm-dd-01-01"
                        # Эта проверка должна срабатывать только для ежегодных прививок, таких как тип 'v'
                        if len(last_valid_date) > 10 and last_valid_date[-5:] == "-01-01" and last_valid_type:
                            last_valid_date = last_valid_date[:10]  # Оставляем только первую часть "yyyy-mm-dd"

                        # Если это ежегодная прививка, тип должен быть 'v', если не указано иначе
                        if vaccine in annual_vaccinations and not last_valid_type:
                            last_valid_type = 'v'

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
                                last_type = 'v1'
                        elif match[1]:  # Обработка обычных дат и типов
                            try:
                                record = match[1].strip()
                                type_match = re.search(r'^(V|V1|V2|RV|RV1|RV2)', record, re.IGNORECASE)
                                date_match = re.search(r'(\d{2}\.\d{2}\.\d{2,4})', record)
                                if date_match:
                                    date_parsed = pd.to_datetime(date_match.group(1), dayfirst=True).strftime(
                                        '%Y-%m-%d')
                                    current_type = type_match.group(1).lower() if type_match else 'v'

                                    if last_date is None or date_parsed > last_date:
                                        last_date = date_parsed
                                        last_type = current_type
                            except Exception as e:
                                error_msg = f"Error processing record {record} in data: {data}, Error: {e}"
                                logging.error(error_msg)
                                error_log.append(error_msg)

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
                WHERE lastname = ? AND firstname = ? AND name = ? AND dateOfBirth = ?
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

# Пример вызова функции для привязки к кнопке
if __name__ == "__main__":
    file_path = r'C:\Users\User\PycharmProjects\pdf_generation\Копия_Список_сотрудников_для_планирования_вакцинации_с_указанием.xlsx'
    base_path = r'C:\Users\User\PycharmProjects\pdf_generation\database.db'
    process_excel_to_sqlite(file_path, base_path)

def print_errors():
    if error_log:
        print("\nErrors during processing:")
        for error in error_log:
            print(error)
    else:
        print("No errors during processing.")
print_errors()


