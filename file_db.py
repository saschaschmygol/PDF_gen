import sqlite3
import datetime
import json
from pdf_settings_style import MONTH

def mont_replace(date ):
    ''' ['2024-12-23', 'грипп', 'rv'] '''
    duplicat_date = date[:]
    for n in duplicat_date:
        n[0] = str(MONTH[n[0].split('-')[1]]) + ' ' + str(n[0].split('-')[0])

    return duplicat_date


def searсh_men(personInfo: list):
    ''' Проверка наличия пациента в базе '''
    request_bd = ["S.Имя =  '", "S.Фамилия = '", "S.Отчество = '"] # для поиска по набору параметров Ф_И_О
    str_pers_info = ''

    if any(personInfo): # если список не пустой
        for i, n in enumerate(personInfo):
            if  personInfo[i] != '':
                if str_pers_info == '':
                    str_pers_info +=  f"{request_bd[i]}{personInfo[i]}'"
                else:
                    str_pers_info += f" AND {request_bd[i]}{personInfo[i]}'"
    else:
        str_pers_info = 'false'

    #print(str_pers_info)

    conn = sqlite3.connect('1.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT S.ID, S.Имя, S.Фамилия, S.Отчество, S.Дата_Рождения FROM Сотрудник as S WHERE ({str_pers_info});")
    rows = cursor.fetchall()

    if len(rows) == 0:
        return False
    else:
        return rows


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

def check_year(date):
    ''' date 2023-03-21 Проверка года'''
    lst_data: list = date.split('-')  # выделяем год месяц день
    year = int(lst_data[0])
    month = int(lst_data[1])
    day = int(lst_data[2])
    custom_date = datetime.datetime(year, month, day)
    if year > 2025:
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

def date_person(id):
    with open('data_dict.json', 'r', encoding='utf-8') as f:
        loaded_dict_json = json.load(f) # словарь

    conn = sqlite3.connect('1.db')
    age = 0
    gender = "" # переменные под пол и возраст
    date = {'name': None, 'date': []}

    # обновляем словарь сферы работы json
    cursor = conn.cursor()
    # cursor.execute(f"SELECT S.name, S.vac_1, S.vac_2, S.vac_3, S.vac_4, S.vac_5, S.vac_6, S.vac_7, S.vac_8, S.vac_9, S.vac_10, S.vac_11, S.vac_12 FROM Сфера_Работы as S")
    # rows = cursor.fetchall()
    update_json_scope_work('data_dict.json', '1.db')

    # Получение персональных данных
    cursor.execute(f"SELECT S.Имя, S.Фамилия, S.Отчество, S.Пол, S.Дата_Рождения FROM Сотрудник as S WHERE S.ID = {id};")
    rows = cursor.fetchall()
    pers_info = rows

    age = age_calculate(pers_info[0][4])
    date['name'] = pers_info[0][1] + ' ' + pers_info[0][0] + ' ' + pers_info[0][2]  # формируем имя в строку
    gender = pers_info[0][3]
    print(age, date['name'], gender)

    #Получение должности и подразделения
    cursor.execute(f"SELECT Д.name, Д.Подразделение FROM Должность as Д WHERE Д.ID = (SELECT S.Должность_Сотрудника FROM Сотрудник as S WHERE ID={id})")
    rows = cursor.fetchall()
    pers_info_d = rows
    date['post_division'] = [pers_info_d[0][0], pers_info_d[0][1]]

    #Получение сферы работы пациента
    cursor.execute(f"SELECT S.Сфера_Работы FROM Должность as S WHERE S.ID = (SELECT Сотрудник.Должность_Сотрудника FROM Сотрудник WHERE Сотрудник.ID={id});")
    rows = cursor.fetchall()
    scope_of_work = rows[0][0]
    print(scope_of_work)

    # Получение необходимых вакцин по должности
    vaccineListScope = loaded_dict_json["scope_work"][scope_of_work]
    print(vaccineListScope)

    # получение списка последних вакцин в соответствии со списком по должности
    strVaccineList = ", ".join([f" '{str(vac)}'" for vac in vaccineListScope])
    cursor.execute(f"SELECT MAX(Вакцинация.Дата) as Дата, Вакцинация.Название_Прививки, Вакцинация.Тип FROM Вакцинация  GROUP BY Вакцинация.ID_Сотрудника, Вакцинация.Название_Прививки HAVING Вакцинация.ID_Сотрудника = {id} AND Название_Прививки IN({strVaccineList});")
    rows = cursor.fetchall()
    lastVacList = rows
    print(f" Раньше велась {lastVacList}")

    # Валидация списка по возрасту и полу
    if gender != "Ж" or age > 25:# краснуха
        try:
            vaccineListScope.remove('Краснуха')
        except Exception:
            pass

    if scope_of_work != 'Медик' and age >= 55: # гепатит B
        try:
            vaccineListScope.remove('Гепатит B')
        except Exception:
            pass

    if scope_of_work != 'Медик' and age <= 60: # Пневмококковая инфекция
        try:
            vaccineListScope.remove('Пневмококковая инфекция')
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

            if check_year(newTime): # если укладывается в год

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
            print(f"cond {cond}  {n[1]}")
            print(f'{loaded_dict_json["vaccination"][n[1]][cond][0]}')
            addTime = loaded_dict_json["vaccination"][n[1]][cond][0]
            newTime = add_time(lastData, addTime)

            if check_year(newTime):
                if cond != loaded_dict_json["vaccination"][n[1]][cond][1]:
                    pass
                else:
                    break

                if cond == 'k': #если выполнен последний этап - останавливаемся
                    break # ТУТ ЧТО ТО НЕ ТАК

                date['date'].append([newTime, n[1], loaded_dict_json["vaccination"][n[1]][cond][1]])
                cond = loaded_dict_json["vaccination"][n[1]][cond][1]
                lastData = newTime

            else:
                break

    #print(date['date'])
    slist = sorted(date['date'])
    date['date'] = slist[:]
    date['id'] = id
    #sort_mounth(date['date'])
    print(slist)

    return date

#date_person(1)

#update_json_scope_work('data_dict.json', '1.db')