import sqlite3
import datetime
import json
from pdf_settings_style import MONTH
from collections import defaultdict

# Функция для преобразования строковой даты в объект datetime
def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")

# Функция для преобразования объекта datetime в строку
def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

# Функция для проверки и перераспределения прививок
def process_vaccination_schedule(schedule):
    # Сортируем по дате
    schedule.sort(key=lambda x: parse_date(x[0]))

    # Разбиваем прививки по типам
    type_dict = defaultdict(list)
    date_dict = defaultdict(list)
    for date, vaccine_type, vaccine_category in schedule:
        date_format = parse_date(date)

        type_dict[vaccine_type].append([date_format, vaccine_category])
        date_dict[f"{date_format.year}-{date_format.month}"].append([vaccine_type, vaccine_category])

    for i in range(0, len(schedule)*5):

      for key_date, records in date_dict.items():
        # break_flag = False
        record = []
        step_list = []
        if len(records) > 3:
          # break_flag = True
          for i in range(0, len(records)):
            if len(record) != 3 and records[i] not in record:
              # print(records[i])
              counter = 0
              for j in range(0, len(records)):
                if records[i] == records[j]:
                  counter += 1
              for k in range(0, counter):

                record.append(records[i])

            else:
              step_list.append(records[i])

          date_dict[key_date] = record
          # print(record)
          #  Обрабатываем step_list, находя дубликаты в других ключах и сдвигая их
          for step_item in step_list:
              for other_key, other_records in list(date_dict.items()):
                  if other_key != key_date and step_item in other_records:
                      date_dict[other_key].remove(step_item)

                      # Вычисляем новый ключ (добавляем 1 месяц к найденному ключу)
                      year, month = map(int, other_key.split('-'))
                      new_month = month + 1
                      new_year = year
                      if new_month > 12:
                          new_month = 1
                          new_year += 1

                      new_key_date = f"{new_year}-{new_month}"

                        # Переносим step_item в новый ключ
                      date_dict[new_key_date].append(step_item)

          year, month = map(int, key_date.split('-'))
          new_month = month + 1
          new_year = year
          if new_month > 12:
              new_month = 1
              new_year += 1

          new_key_date = f"{new_year}-{new_month}"

          date_dict[new_key_date].extend(step_list)
          break

      # if not break_flag:
      #   break

    return date_dict

def update_schedule_with_keys(schedule, date_dict):
    updated_schedule = []
    for date, vaccine_type, vaccine_category in schedule:
        date_obj = parse_date(date)

        # Проверяем, есть ли такой тип вакцины в date_dict
        for key, records in date_dict.items():
            if [vaccine_type, vaccine_category] in records:
                # Заменяем дату на ключ с сохранением дня

                year, month = map(int, key.split('-'))
                if month < 10:
                  month = f"0{month}"

                new_date = f"{year}-{month}-{date_obj.day}"
                updated_schedule.append([new_date, vaccine_type, vaccine_category])
                break

    return sorted(updated_schedule)


def mont_replace(date ):
    ''' ['2024-12-23', 'грипп', 'rv'] -> ['Ноябрь 2024'] '''
    duplicat_date = date[:]
    for n in duplicat_date:
        n[0] = str(MONTH[n[0].split('-')[1]]) + ' ' + str(n[0].split('-')[0])

    return duplicat_date

def update_json_scope_work(filename, fileDB):
    ''' Обновление json сферы работы rows = ([], [], []) - [] строка запроса '''
    conn = sqlite3.connect(fileDB)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT S.name, S.vac_1, S.vac_2, S.vac_3, S.vac_4, S.vac_5, S.vac_6, S.vac_7, S.vac_8, S.vac_9, S.vac_10, S.vac_11, S.vac_12 FROM Сфера_Работы as S")
    rows = cursor.fetchall()

    with open(filename, 'r', encoding='utf-8') as f:
        loaded_dict = json.load(f) # словарь

        for i in rows:
            loaded_dict["scope_work"][i[0]] = [n for n in i[1:] if n != None]


    with open(filename, 'w', encoding='utf-8') as f: # перезапись
        json.dump(loaded_dict, f, ensure_ascii=False, indent=4)

def age_calculate(date_of_birth): # 2002-01-23
    ''' Рассчет возраста '''
    bir_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    cur_date = datetime.datetime.now()

    age = cur_date.year - bir_date.year

    if (cur_date.month, cur_date.day) < (bir_date.month, bir_date.day):
        age -= 1
    return age

def sort_mounth(date):
    ''' Сортировка месяцев в date в порядке (январь -> декабрь)
     date['date'] = [['2023-06-10', 'Дизентерия Зонне'], .....]'''
    sorted_date = sorted(date, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'))
    return sorted_date

def check_year(date, deadline_date):
    ''' date 2023-03-21 Проверка года'''
    lst_data: list = date.split('-')  # выделяем год месяц день
    year = int(lst_data[0])
    month = int(lst_data[1])
    day = int(lst_data[2])

    custom_date = datetime.datetime(year, month, day)
    if custom_date > deadline_date:
        return False
    else:
        return True
    # current_date = datetime.datetime.now()
    #
    # if (custom_date - current_date).days > 365:
    #     return False
    # else:
    #     return True

def add_time(current_date, days_to_add): # дата в формате 2024-02-21, кол-во недель
    ''' Прибавление (weeks_to_add) дней к дате '''

    lst_data: list = current_date.split('-') # выделяем год месяц день
    year = int(lst_data[0])
    month = int(lst_data[1])
    day = int(lst_data[2])

    custom_date = datetime.datetime(year, month, day)
    new_date = (custom_date + datetime.timedelta(days=days_to_add)).strftime("%Y-%m-%d") # '2023-09-21'

    # str_data = new_date.split('-')
    # new_date = MONTH[str_data[1]] + ' ' + str_data[0]                                   # 'март 2023'

    return new_date

def date_person(id, deadline_date):
    with open('data_dict.json', 'r', encoding='utf-8') as f:
        loaded_dict_json = json.load(f) # словарь

    conn = sqlite3.connect('database.db')
    age = 0
    gender = "" # переменные под пол и возраст
    date = {'name': None, 'date': [], 'id': None, 'gendedr': None}

    # обновляем словарь сферы работы json
    cursor = conn.cursor()
    # cursor.execute(f"SELECT S.name, S.vac_1, S.vac_2, S.vac_3, S.vac_4, S.vac_5, S.vac_6, S.vac_7, S.vac_8, S.vac_9, S.vac_10, S.vac_11, S.vac_12 FROM Сфера_Работы as S")
    # rows = cursor.fetchall()
    #update_json_scope_work('data_dict.json', '1.db')

    # Получение персональных данных
    cursor.execute(f"SELECT S.name, S.firstname, S.lastname, S.gender, S.dateOfBirth FROM worker as S WHERE S.ID = {id};")
    rows = cursor.fetchall()
    pers_info = rows

    age = age_calculate(pers_info[0][4])
    date['name'] = pers_info[0][1] + ' ' + pers_info[0][0] + ' ' + pers_info[0][2]  # формируем имя в строку
    gender = pers_info[0][3]
    print(age, date['name'], gender)
    date['gender'] = gender

    #Получение должности и подразделения
    cursor.execute(f"SELECT P.name, P.division FROM position as P WHERE P.ID = (SELECT W.position FROM worker as W WHERE ID={id})")
    rows = cursor.fetchall()
    pers_info_d = rows
    date['post_division'] = [pers_info_d[0][0], pers_info_d[0][1]]
    print(date['post_division'])

    #Получение сферы работы пациента
    cursor.execute(f"SELECT P.areaOfWork FROM position as P WHERE P.ID = (SELECT worker.position FROM worker WHERE worker.ID={id});")
    rows = cursor.fetchall()
    scope_of_work = rows[0][0]
    print(scope_of_work)

    # Получение необходимых вакцин по должности
    vaccineListScope = loaded_dict_json["scope_work"][scope_of_work]
    if "pertussis" in vaccineListScope:
        vaccineListScope.remove('pertussis')
    print(vaccineListScope)

    # получение списка последних вакцин в соответствии со списком по должности
    strVaccineList = ", ".join([f" '{str(vac)}'" for vac in vaccineListScope])
    cursor.execute(f"SELECT MAX(immunization.date) as date, immunization.vaccination, immunization.type FROM immunization GROUP BY immunization.workerID, immunization.vaccination HAVING immunization.workerID = {id} AND immunization.vaccination IN({strVaccineList});")
    rows = cursor.fetchall()
    lastVacList = rows
    print(f" Раньше велась {lastVacList}")

    # Валидация списка по возрасту и полу
    if gender != "w" or age > 25:# краснуха
        try:
            vaccineListScope.remove('rubella')
        except Exception:
            pass

    if scope_of_work != 'medical' and age >= 55: # гепатит B
        try:
            vaccineListScope.remove('hepatitisB')
        except Exception:
            pass

    if scope_of_work != 'medical' and age <= 60: # Пневмококковая инфекция
        try:
            vaccineListScope.remove('pneumococcalInfection')
        except Exception:
            pass

    # если раньше не велась вакцинация
    alt_lst = [i[1] for i in lastVacList] #в виде списка те, которые велись
    new_lst_vac_work = list(set(vaccineListScope) - set(alt_lst)) #список прививок для которых нужно начать схему вакцинации
    print(new_lst_vac_work)

    for i, n in enumerate(new_lst_vac_work):
        cond = '0' #начальное состояние прививки
        lastData = datetime.datetime.now().strftime("%Y-%m-%d")

        while True:
            addTime = loaded_dict_json["vaccination"][n][cond][0]
            newTime = add_time(lastData, addTime)
            #print(addTime, newTime, n)

            if check_year(newTime, deadline_date): # если укладывается в год

                if cond != loaded_dict_json["vaccination"][n][cond][1]:
                    pass
                else:
                    break

                if cond == 'k': #если выполнен последний этап - останавливаемся
                    break # ТУТ ЧТО ТО НЕ ТАК

                date['date'].append([newTime, n, loaded_dict_json["vaccination"][n][cond][1]])
                cond = loaded_dict_json["vaccination"][n][cond][1]
                lastData = newTime
            else:
                break

    # если велась прививка
    for i, n in enumerate(lastVacList):
        cond = n[2] # последнее состояние прививки
        lastData = n[0] #последняя дата прививки

        while True:
            #print(f"cond {cond}  {n[1]}")
            #print(f'{loaded_dict_json["vaccination"][n[1]][cond][0]}')
            addTime = loaded_dict_json["vaccination"][n[1]][cond][0]
            newTime = add_time(lastData, addTime)

            if check_year(newTime, deadline_date):
                if cond != loaded_dict_json["vaccination"][n[1]][cond][1] or (cond == loaded_dict_json["vaccination"][n[1]][cond][1] == 'v'): # это условие переделать
                    pass
                else:
                    break

                if cond == 'k': #если выполнен последний этап - останавливаемся
                    break # ТУТ ЧТО ТО НЕ ТАК

                date['date'].append([newTime, n[1], loaded_dict_json["vaccination"][n[1]][cond][1]])
                #print([newTime, n[1], loaded_dict_json["vaccination"][n[1]][cond][1]])
                cond = loaded_dict_json["vaccination"][n[1]][cond][1]
                lastData = newTime

            else:
                break

    slist = sorted(date['date']) # сортировка

    #processed_schedule = process_vaccination_schedule(slist)
    #updated_schedule = update_schedule_with_keys(slist, processed_schedule) # распределение по месяцам

    #date['date'] = updated_schedule[:]
    date['date'] = slist
    date['id'] = id
    #sort_mounth(date['date'])
    print(date['date'])

    # for i in date['date']:
    #     print(i[1])

    return date

#date_person(1, datetime.datetime(2026, 1, 15))

#update_json_scope_work('data_dict.json', '1.db')