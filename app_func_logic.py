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

    #print(str_pers_info)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT S.ID, S.name, S.firstname, S.lastname, S.dateOfBirth FROM worker as S WHERE ({str_pers_info});")
    rows = cursor.fetchall()

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