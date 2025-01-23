import sqlite3

from pdf_settings_style import MONTH, RENAME_DICT


def searсh_men(personInfo: list):
    ''' Проверка наличия пациента в базе '''
    request_bd = ["S.name =  '", "S.firstname = '", "S.lastname = '"] # для поиска по набору параметров Ф_И_О
    str_pers_info = ''

    if any(personInfo): # если список не пустой
        for i, n in enumerate(personInfo):
            if personInfo[i] != '':
                if str_pers_info == '':
                    str_pers_info += f"{request_bd[i]}{personInfo[i]}'"
                else:
                    str_pers_info += f" AND {request_bd[i]}{personInfo[i]}'"
    else:
        str_pers_info = 'false'

    print(str_pers_info)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT S.ID, S.name, S.firstname, S.lastname, S.dateOfBirth FROM worker as S WHERE ({str_pers_info});")
    rows = cursor.fetchall()
    print(rows)
    if len(rows) == 0:
        return False
    else:
        return rows

def mont_replace(date ):
    ''' ['2024-12-23', 'грипп', 'rv'] -> ['Ноябрь 2024'] '''
    duplicat_date = date[:]
    for n in duplicat_date:
        n[0] = str(MONTH[n[0].split('-')[1]]) + ' ' + str(n[0].split('-')[0])

    return duplicat_date

def rename_vaccine(data):
    ''' переводим названия в читаемый вид'''
    ren_vac = RENAME_DICT.get(data, '-')
    return ren_vac

def rename_vaccine_R(data):
    ren_vac = next((k for k, v in RENAME_DICT.items() if v == data), None)
    return ren_vac

def ext_pers_info(id):
    date = {}
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # cursor.execute(f"SELECT S.name, S.vac_1, S.vac_2, S.vac_3, S.vac_4, S.vac_5, S.vac_6, S.vac_7, S.vac_8, S.vac_9, S.vac_10, S.vac_11, S.vac_12 FROM Сфера_Работы as S")
    # rows = cursor.fetchall()
    # update_json_scope_work('data_dict.json', '1.db')

    # Получение персональных данных
    cursor.execute(
        f"SELECT S.name, S.firstname, S.lastname, S.gender, S.dateOfBirth FROM worker as S WHERE S.ID = {id};")
    rows = cursor.fetchall()
    pers_info = rows

    date['name'] = pers_info[0][1] + ' ' + pers_info[0][0] + ' ' + pers_info[0][2]  # формируем имя в строку
    gender = pers_info[0][3]
    date['gender'] = gender

    # Получение должности и подразделения
    cursor.execute(
        f"SELECT P.name, P.division FROM position as P WHERE P.ID = (SELECT W.position FROM worker as W WHERE ID={id})")
    rows = cursor.fetchall()
    pers_info_d = rows
    date['post_division'] = [pers_info_d[0][0], pers_info_d[0][1]]
    return date
