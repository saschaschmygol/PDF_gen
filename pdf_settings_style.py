from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

def cm_to_points(cm: float):
    return cm * 28.3464567  # 1 cm = 28.3464567 points

def generate_str_vac(date):
    '''Генерация списка требуемых прививок в начале странпицы'''
    str_vac = []

    for i, n in enumerate(date['date']):
        if n and n not in str_vac:
            str_vac.append(rename_vaccine(n[1]))
        else:
            pass

    str_vac =  list(set(str_vac))
    str_vac = ' ; '.join(str_vac)

    return str_vac

STYLE = TableStyle([
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Цвет текста для заголовка
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Выравнивание текста по центру
    ('FONTNAME', (0, 0), (-1, 0), 'Times'),  # Шрифт для заголовка
    ('FONTSIZE', (0, 0), (-1, 0), 14),  # Размер шрифта для заголовка
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Отступ снизу для заголовка
    ('BACKGROUND', (0, 0), (-1, -1), colors.white),  # Заливка фона для данных
    ('FONTNAME', (0, 1), (-1, -1), 'Times'),  # Шрифт для данных
    ('FONTSIZE', (0, 1), (-1, -1), 12),  # Размер шрифта для данных
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Сетка таблицы
    ('SPAN', (2, 0), (-1, 0)),  # Объединение ячеек Header 2 и Header 3
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
])

CUSTOM_PARAGRAPH_STYLE = ParagraphStyle(
    'CustomStyle',
    fontName='Times',
    fontSize=10,
    leading=10,  # Межстрочный интервал
    textColor=colors.black,
    alignment=TA_JUSTIFY,  # Центрирование текста (0 - влево, 1 - центр, 2 - вправо, 4 - в ширину)
    spaceAfter=0,  # Отступ после абзаца
    firstLineIndent=30,  # Отступ первой строки (красная строка)
    leftIndent=cm_to_points(0.5),  # Отступ слева
    rightIndent=cm_to_points(0)  # Отступ справа
)

TAB_PARAGRAPH_STYLE = ParagraphStyle(
    'TabStyle',
    fontName='Times',
    fontSize=10,
    leading=11,  # Межстрочный интервал
    textColor=colors.black,
    alignment=4,  # Центрирование текста (0 - влево, 1 - центр, 2 - вправо, 4 - в ширину)
    spaceAfter=0,  # Отступ после абзаца
    firstLineIndent=0,  # Отступ первой строки (красная строка)
    leftIndent=cm_to_points(0),  # Отступ слева
    rightIndent=cm_to_points(0)  # Отступ справа
)

SIGNATURE_PARAGRAPH_STYLE = ParagraphStyle(
    'SignaturStyle',
    fontName='Times',
    fontSize=10,
    leading=20,  # Межстрочный интервал
    textColor=colors.black,
    alignment=4,  # Центрирование текста (0 - влево, 1 - центр, 2 - вправо, 4 - в ширину)
    spaceAfter=0,  # Отступ после абзаца
    firstLineIndent=20,  # Отступ первой строки (красная строка)
    leftIndent=cm_to_points(1),  # Отступ слева
    rightIndent=cm_to_points(0)  # Отступ справа
)

KALEND_PO_EPIDEM_PAKAZ = {'Гепатит А': 'П.12', 'Гепатит B': 'П.16', 'Клещевой энцефалит': 'П.7',
                          'Дизентерия Зонне': 'П.13', 'НКВИ': 'П.24',
                          'Ветряная оспа': 'П.22', 'Пневмококковая инфекция': 'П.20'}

NATION_KALENDAR = {'Гепатит B': 'П.16', 'Дифтерия, столбняк': 'П.15',  'Краснуха': 'П.17', 'Грипп': 'П.19', 'Корь': 'П.18'}

REGION_KALENDAR = {'Гепатит А': 'П.38', 'Гепатит B': 'П.21', 'Дифтерия, столбняк': 'П.20', 'Клещевой энцефалит': 'П.32',
                          'Краснуха': '22', 'Дизентерия Зонне': 'П.40,41', 'Грипп': 'П.24', 'НКВИ': 'П.25', 'Корь': '23', 'Коклюш': 'П.49',
                          'Ветряная оспа': 'П.47', 'Пневмококковая инфекция': 'П.44,45'}

EPIDEM_NADSOR_GEPATIT_B = {'Гепатит B': 'П.11, 11.2, 11.4'}

MONTH = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь', '07': 'Июль',
         '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь', }

MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

def rename_vaccine(data):

    # print(1)
    ''' Временная функция, flag=1 - из НКВИ в COVID19, 0 - наоборот
    # [['2121-21-21, 'Грипп'm 'RV'], ] '''
    # curr_dat = data[:]
    rename_dict = {'НКВИ': 'COVID-19', 'COVID-19': 'НКВИ'}
    if data in rename_dict:
        return rename_dict[data]
    else:
        return data
    # if flag == 1:
    #     for i, d in enumerate(curr_dat):
    #         if d[1] in rename_dict:
    #             curr_dat[i][1] = rename_dict[d[1]]
    # print(curr_dat)

