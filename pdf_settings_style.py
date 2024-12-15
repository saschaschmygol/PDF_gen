from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

def cm_to_points(cm: float):
    return cm * 28.3464567  # 1 cm = 28.3464567 points

def generate_str_vac(date):
    '''Генерация списка требуемых прививок в начале странпицы'''
    str_vac = ''
    last_n = len(date['date'])
    cur_n = 1

    for i in date['date']:
        if cur_n < last_n:
            str_vac += ' ' + i[1] + ';'
            cur_n += 1
        else:
            str_vac += ' ' + i[1] + '.'
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
    ('SPAN', (2, 0), (4, 0)),  # Объединение ячеек Header 2 и Header 3
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
    leading=14,  # Межстрочный интервал
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

KALEND_PO_EPIDEM_PAKAZ = {'Гепатит А': 'П.12', 'Гепатит B': 'П.16', 'Дифтерия': 'П.17', 'Клещевой энцефалит': 'П.7',
                          'Краснуха': '', 'Дизентерия Зонне': '', 'Грипп': '', 'НКВИ': 'П.24', 'Корь': 'П.15', 'Коклюш': '',
                          'Ветряная оспа': 'П.22', 'Пневмококковая инфекция': 'П.20'}

NATION_KALENDAR = {'Гепатит А': 'П.12', 'Гепатит B': 'П.16', 'Дифтерия': 'П.15', 'Клещевой энцефалит': 'П.7',
                          'Краснуха': 'П.17', 'Дизентерия Зонне': '', 'Грипп': 'П.19', 'НКВИ': 'П.24', 'Корь': 'П.18', 'Коклюш': 'П.10',
                          'Ветряная оспа': 'П.22', 'Пневмококковая инфекция': 'П.20'}

REGION_KALENDAR = {'Гепатит А': 'П.37', 'Гепатит B': 'П.21', 'Дифтерия': 'П.20', 'Клещевой энцефалит': 'П.32',
                          'Краснуха': '22', 'Дизентерия Зонне': 'П.38', 'Грипп': 'П.24', 'НКВИ': 'П.25', 'Корь': '', 'Коклюш': 'П.44',
                          'Ветряная оспа': 'П.42', 'Пневмококковая инфекция': 'П.40'}

MONTH = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь', '07': 'Июль',
         '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь', }

MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]