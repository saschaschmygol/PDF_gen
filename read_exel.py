import openpyxl
import pandas as pd
import sqlite3
import re
from datetime import datetime
import datetime
import locale


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
        "Медик": [
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
        "Пищеблок": [
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
        "Коммунальное обслуживание": [
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
        if patronymic.endswith("ич"):
            return "М"
        elif patronymic.endswith("на"):
            return "Ж"

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
        return "Не медик"

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
        cursor.execute("DELETE FROM Вакцинация")
        cursor.execute("DELETE FROM Сотрудник")
        cursor.execute("DELETE FROM Должность")
        cursor.execute("DELETE FROM Показатель_AntiHBs")
        print("Deleted all records from Вакцинация, Сотрудник, Должность, Показатель_AntiHBs.")

        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Вакцинация'")  # Для таблицы Вакцинация
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Должность'")  # Для таблицы Должность
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Показатель_AntiHBs'")  # Для таблицы Показатель_AntiHBs
        print("Reset auto-increment counters for all tables.")
    except Exception as e:
        print(f"Error deleting data from tables: {e}")
        conn.rollback()  # Откатить транзакцию в случае ошибки
        raise

    # Функция для преобразования NULL значений
    def normalize_value(value):
        return value if value is not None else 'NULL_VALUE'

    # Построение списка уникальных ключей, которые присутствуют в Excel
    unique_keys = df[['Фамилия', 'Имя', 'Отчество', 'Дата рождения']].dropna().astype(str).apply(lambda x: '|'.join(x), axis=1).tolist()

    # Удаление записей, которые не присутствуют в Excel
    cursor.execute("""
        DELETE FROM Сотрудник
        WHERE (Фамилия || '|' || Имя || '|' || Отчество || '|' || Дата_Рождения) NOT IN ({})
    """.format(','.join('?' * len(unique_keys))), unique_keys)
    print("Removed rows that are not present in the Excel file.")

    # Вставка или обновление данных в таблицу Должность
    for index, row in df.iterrows():
        name = normalize_value(row['Штатная должность']) if pd.notnull(row['Штатная должность']) else 'NULL_VALUE'
        sphere = determine_sphere(name)
        subdivision = normalize_value(row['Штатное подразделение']) if pd.notnull(row['Штатное подразделение']) else 'NULL_VALUE'
        short_name = normalize_value(row['Краткое название']) if pd.notnull(row['Краткое название']) else 'NULL_VALUE'

        try:
            print(f"Processing row {index}: name={name}, subdivision={subdivision}, short_name={short_name}, sphere={sphere}")

            # Проверка существования записи в таблице
            cursor.execute("""
                SELECT ID FROM Должность 
                WHERE name = ? AND Подразделение = ? AND Краткое_Название = ?
            """, (name, subdivision, short_name))
            existing_record = cursor.fetchone()

            if existing_record:
                # Если запись существует, обновляем только при необходимости
                cursor.execute("""
                    UPDATE Должность
                    SET Сфера_Работы = ?
                    WHERE name = ? AND Подразделение = ? AND Краткое_Название = ?
                """, (sphere, name, subdivision, short_name))
                print(f"Updated existing record: name={name}, subdivision={subdivision}, short_name={short_name}, sphere={sphere}")
            else:
                # Если записи нет, вставляем новую
                cursor.execute("""
                    INSERT INTO Должность (name, Сфера_Работы, Подразделение, Краткое_Название)
                    VALUES (?, ?, ?, ?)
                """, (name, sphere, subdivision, short_name))
                print(f"Inserted new record: name={name}, subdivision={subdivision}, short_name={short_name}, sphere={sphere}")

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError inserting or updating row {index}: {e}")
        except Exception as e:
            print(f"Error inserting or updating row {index}: {e}")

    # Вставка или обновление данных в таблицу Сотрудник
    id_counter = 1  # Счетчик для генерации ID

    for _, row in df.iterrows():  # Используем индекс "_" для пропуска индекса DataFrame
        try:
            # Проверка наличия обязательных полей
            if pd.isna(row.get('Фамилия')) or pd.isna(row.get('Имя')) or pd.isna(row.get('Отчество')) or pd.isna(
                    row.get('Дата рождения')):
                print(f"Skipping row due to NULL value in required fields: {row.to_dict()}")
                continue

            # Генерация должности ID (если есть информация о должности)
            query = "SELECT ID FROM Должность WHERE 1=1"
            params = []

            if not pd.isna(row.get('Штатная должность')):
                query += " AND name = ?"
                params.append(row['Штатная должность'])

            if not pd.isna(row.get('Штатное подразделение')):
                query += " AND Подразделение = ?"
                params.append(row['Штатное подразделение'])

            if not pd.isna(row.get('Краткое название')):
                query += " AND Краткое_Название = ?"
                params.append(row['Краткое название'])

            cursor.execute(query, params)
            result = cursor.fetchone()
            должность_id = result[0] if result else None

            # Определение пола
            gender = determine_gender(row.get('Отчество', ''))

            # Лог для проверки Статуса
            print(f"Статус для {row.get('Фамилия')} {row.get('Имя')}: {row.get('Статус')}")

            # Вставка данных сотрудника с независимым ID
            cursor.execute("""
                INSERT INTO Сотрудник (ID, Фамилия, Имя, Отчество, Пол, Дата_Рождения, Статус, Должность_Сотрудника)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ID) DO UPDATE SET
                    Фамилия = excluded.Фамилия,
                    Имя = excluded.Имя,
                    Отчество = excluded.Отчество,
                    Пол = excluded.Пол,
                    Дата_Рождения = excluded.Дата_Рождения,
                    Статус = excluded.Статус,
                    Должность_Сотрудника = excluded.Должность_Сотрудника
            """, (
                id_counter,  # Автогенерируемый ID
                row.get('Фамилия'), row.get('Имя'), row.get('Отчество'), gender,
                row.get('Дата рождения', None), row.get('Статус', None), должность_id
            ))

            print(f"Inserted or updated: ID {id_counter}, {row.get('Фамилия')}, {row.get('Имя')}")
            id_counter += 1  # Увеличение счетчика ID

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"Error: {e}")

    # Удаление некорректных записей с NULL в ключевых полях
    cursor.execute("""
        DELETE FROM Сотрудник
        WHERE Фамилия IS NULL
          OR Имя IS NULL
          OR Отчество IS NULL
          OR Дата_Рождения IS NULL
    """)
    print("Removed invalid rows with NULL in required fields.")

    # Вставка данных в таблицу Вакцинация
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
        'ГВ': 'Гепатит B',
        'Клещевой энцефалит': 'Клещевой энцефалит',
        'АДС-м': 'Дифтерия, столбняк',
        'Шигеллвак': 'Дизентерия Зонне',
        'Корь': 'Корь',
        'Краснуха': 'Краснуха',
        'Гепатит А': 'Гепатит А',
        'Грипп': 'Грипп',
        'Ветряная оспа': 'Ветряная оспа',
        'ВПЧ': 'Коклюш',
        'Пневмо': 'Пневмококковая инфекция',
        'НКВИ': 'НКВИ',
    }

    # Вставка данных в таблицу Вакцинация
    for index, row in df.iterrows():
        try:
            # Получение ID сотрудника из таблицы Сотрудник
            cursor.execute("""
                SELECT ID FROM Сотрудник
                WHERE Фамилия = ? AND Имя = ? AND Отчество = ? AND Дата_Рождения = ?
            """, (row['Фамилия'], row['Имя'], row['Отчество'], row['Дата рождения']))
            сотрудник = cursor.fetchone()
            if not сотрудник:
                print(f"Сотрудник не найден: {row['Фамилия']} {row['Имя']} {row['Отчество']}")
                continue

            сотрудник_id = сотрудник[0]

            # Определение данных вакцинации
            вакцинации = {
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

            date_pattern = r'\d{2}\.\d{2}\.\d{2,4}'
            allowed_types = {'RV', 'V', 'RV1', 'V1', 'V2', 'V3'}

            # Логика для ежегодных прививок
            ежегодные_прививки = {'НКВИ', 'Шигеллвак', 'Грипп'}

            for вакцина, данные in вакцинации.items():
                if pd.notna(данные):
                    данные = str(данные).strip()
                    прививки = re.split(r'[;\,\s]+', данные)  # Разделение строки на части

                    прививки_по_типу = {}  # Словарь для хранения дат по типам прививок
                    текущий_тип = None  # Текущий тип прививки

                    # Перебираем все элементы (даты и типы)
                    for элемент in прививки:
                        элемент = элемент.strip()
                        if not элемент:
                            continue

                        # Если элемент - допустимый тип прививки
                        if элемент.upper() in allowed_types:
                            текущий_тип = элемент.upper()
                            continue

                        # Если элемент - дата
                        if re.match(date_pattern, элемент):
                            try:
                                # Преобразование даты в формат YYYY-MM-DD
                                if len(элемент.split('.')[-1]) == 2:  # Если год записан двумя цифрами
                                    элемент = элемент[:-2] + '20' + элемент[-2:]  # Добавляем "20" перед годом
                                дата = pd.to_datetime(элемент, dayfirst=True).strftime('%Y-%m-%d')

                                if текущий_тип is None:
                                    if вакцина in ежегодные_прививки:
                                        текущий_тип = 'V'  # Автоматически присваиваем V для ежегодных прививок
                                    else:
                                        print(
                                            f"Ошибка: не указан тип прививки для даты {дата}. Сотрудник ID: {сотрудник_id}")
                                        continue

                                # Добавляем дату в словарь для текущего типа прививки
                                if текущий_тип not in прививки_по_типу:
                                    прививки_по_типу[текущий_тип] = []
                                прививки_по_типу[текущий_тип].append(дата)

                            except Exception as e:
                                print(f"Ошибка обработки даты {элемент}: {e}")
                        else:
                            print(f"Некорректный элемент прививки: {элемент}. Сотрудник ID: {сотрудник_id}")

                    # Для каждой прививки выбираем последнюю дату и записываем только её в базу
                    if прививки_по_типу:
                        последняя_дата = max(
                            дата for даты in прививки_по_типу.values() for дата in даты
                        )
                        тип = 'V' if вакцина in ежегодные_прививки else текущий_тип

                        # Получаем название прививки для вставки
                        название_прививки = vaccination_mapping.get(вакцина, вакцина)

                        # Проверка существования записи в базе данных для последней даты
                        cursor.execute("""
                            SELECT 1 FROM Вакцинация
                            WHERE ID_Сотрудника = ? AND Название_Прививки = ? AND Дата = ? AND Тип = ?
                        """, (сотрудник_id, название_прививки, последняя_дата, тип))
                        exists = cursor.fetchone()

                        if not exists:
                            cursor.execute("""
                                INSERT INTO Вакцинация (ID_Сотрудника, Название_Прививки, Дата, Тип)
                                VALUES (?, ?, ?, ?)
                            """, (сотрудник_id, название_прививки, последняя_дата, тип))
                            print(
                                f"Inserted: Сотрудник ID {сотрудник_id}, Прививка {название_прививки}, Дата {последняя_дата}, Тип {тип}")
                        else:
                            print(
                                f"Record exists: Сотрудник ID {сотрудник_id}, Прививка {название_прививки}, Дата {последняя_дата}, Тип {тип}")

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

    # Вставка данных в таблицу Показатель_AntiHBs
    for index, row in df.iterrows():
        try:
            # Получаем ID сотрудника через фамилию, имя, отчество и дату рождения
            cursor.execute("""
                SELECT ID FROM Сотрудник
                WHERE Фамилия = ? AND Имя = ? AND Отчество = ? AND Дата_Рождения = ?
            """, (row['Фамилия'].strip(), row['Имя'].strip(), row['Отчество'].strip(), row['Дата рождения']))
            сотрудник = cursor.fetchone()

            if not сотрудник:
                print(f"Сотрудник не найден: {row['Фамилия']} {row['Имя']} {row['Отчество']}")
                continue

            сотрудник_id = сотрудник[0]

            # Получаем показатель Anti-HBs
            показатель_anti_hbs = row.get('показатель anti-hbs октябрь 2023 мме/мл')

            if pd.notna(показатель_anti_hbs):  # Проверяем на nan
                if isinstance(показатель_anti_hbs, str):
                    # Обрабатываем значения с ">"
                    if ">" in показатель_anti_hbs:
                        дата = pd.to_datetime("2023-10-01", dayfirst=True, errors='coerce').strftime('%Y-%m-%d')
                        значение = 1001.0  # Преобразуем >1000 в 1001
                    else:
                        # Извлечение даты и значения из строки
                        части = показатель_anti_hbs.split()
                        if len(части) == 2:
                            дата = pd.to_datetime(части[0], dayfirst=True, errors='coerce').strftime('%Y-%m-%d')

                            # Преобразуем строку в число, обрабатывая как текст
                            try:
                                # Убираем все пробелы и заменяем запятую на точку
                                строковое_значение = части[1].replace(' ', '').replace(',', '.')

                                # Преобразуем в float, если это возможно
                                значение = float(строковое_значение)  # Преобразование в float для REAL

                                print(f"Parsed value for {сотрудник_id}: {значение}")  # Логирование
                            except ValueError as e:
                                print(
                                    f"Ошибка при преобразовании значения: {части[1]} для Сотрудник ID {сотрудник_id} - {e}")
                                continue
                        else:
                            print(f"Некорректный формат данных: {показатель_anti_hbs} для Сотрудник ID {сотрудник_id}")
                            continue
                elif isinstance(показатель_anti_hbs, (int, float)):
                    дата = '2023-10-01'
                    значение = float(показатель_anti_hbs)

                # Проверка, что значение корректное
                if isinstance(значение, (int, float)):
                    # Обновление или вставка данных в базу
                    cursor.execute("""
                        UPDATE Показатель_AntiHBs
                        SET Значение = ?
                        WHERE ID_Сотрудника = ? AND Дата = ?
                    """, (значение, сотрудник_id, дата))

                    # Если обновление не произошло, вставляем новую запись
                    if cursor.rowcount == 0:
                        cursor.execute("""
                            INSERT INTO Показатель_AntiHBs (ID_Сотрудника, Дата, Значение)
                            VALUES (?, ?, ?)
                        """, (сотрудник_id, дата, значение))

                    print(
                        f"Processed Показатель_AntiHBs for Сотрудник ID: {сотрудник_id}, Дата: {дата}, Значение: {значение}")
                else:
                    print(f"Некорректное значение для Сотрудник ID {сотрудник_id}, значение: {значение}")
            else:
                print(f"Missing data for Сотрудник ID: {сотрудник_id}, value: nan")

        except Exception as e:
            print(
                f"Error processing Показатель_AntiHBs for Сотрудник ID: {сотрудник_id}, value: {показатель_anti_hbs} - {e}")

    # Сохранение изменений в базе данных
    conn.commit()
    conn.close()

# Пример вызова функции для привязки к кнопке
if __name__ == "__main__":
    file_path = r'C:\Users\User\PycharmProjects\pdf_generation\Копия_Список_сотрудников_для_планирования_вакцинации_с_указанием.xlsx'
    base_path = r'C:\Users\User\PycharmProjects\pdf_generation\1.db'

    process_excel_to_sqlite(file_path, base_path)
