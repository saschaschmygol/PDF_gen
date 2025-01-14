import sqlite3

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

