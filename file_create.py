from pdf_settings_style import *
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from file_db import date_person
import json
import os

pdfmetrics.registerFont(TTFont('Times', 'timesnewromanpsmt.ttf'))
pdfmetrics.registerFont(TTFont('TimesBold', 'TimesNewRomanBold.ttf'))

def format_date_table(s1, s2, date, TAB_PARAGRAPH_STYLE, KALEND_PO_EPIDEM_PAKAZ, NATION_KALENDAR, REGION_KALENDAR, col_widths):
    ''' Создание списка данных для заполнения таблицы #->список [['', ''], ['', ''], [''..]] '''

    lst_info = [['1' for i in range(len(col_widths))] for i in range(len(date['date']))]
    for i, n in enumerate(date['date']):
        lst_info[i][0] = n[0]
        lst_info[i][1] = n[1] + '  (' + n[2] + ')'
        lst_info[i][2] = REGION_KALENDAR[n[1]]
        lst_info[i][3] = NATION_KALENDAR[n[1]]
        lst_info[i][4] = KALEND_PO_EPIDEM_PAKAZ[n[1]]

        if len(col_widths) == 6:
            lst_info[i][5] = EPIDEM_NADSOR_GEPATIT_B[n[1]]

    stroka_table_words = [[] for i in lst_info] # делаем стиль Paragraph
    for i, x in enumerate(lst_info):
        for n in x:
            a = Paragraph(n, TAB_PARAGRAPH_STYLE)
            stroka_table_words[i].append(a)

    lst_date = [s1, s2]                                # первые 2 строки таблицы

    for i in stroka_table_words:
        lst_date.append(i)

    return lst_date

def generate_pdf(date):
    output_folder = "PDF_files"
    output_path = os.path.join(output_folder, str(date['name']) + ' ' + str(date['id']) + " example.pdf")
    os.makedirs(output_folder, exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=cm_to_points(1), leftMargin=cm_to_points(1))

    with open('data_dict.json', 'r', encoding='utf-8') as f: # json файл с текстом
        loaded_dict = json.load(f)

    col_widths = [cm_to_points(1.9), cm_to_points(3), cm_to_points(4.5), cm_to_points(4.7),
                  cm_to_points(4.5)] if 'Гепатит B' not in [n[1] for n in date['date']] else [cm_to_points(1.9), cm_to_points(3), cm_to_points(4.5), cm_to_points(3.5),
                  cm_to_points(3.5), cm_to_points(3.0)]  # ширина колонок

    loaded_dict['text_top'][1] += 'ый ' if date['gender'] == 'м' else 'ая '
    loaded_dict['text_top'][1] += str(f"{date['name']}! </para>") # добавляем к тексту имя
    loaded_dict['text_top'][2] += str(f"{generate_str_vac(date)} ") # добавляем к тексту список прививок


    if len(col_widths) == 6:
        stroka_table_words = [[] for i in loaded_dict['table_header']] # если есть геп. B
        tab_head = loaded_dict['table_header']
    else:
        stroka_table_words = [[] for i in loaded_dict['table_header']]
        tab_head = [loaded_dict['table_header'][i][:-1] for i in range(len(loaded_dict['table_header']))]

    for i, x in enumerate(tab_head): # первые 2 строки таблицы делаем стили
        for n in x:
            a = Paragraph(n, TAB_PARAGRAPH_STYLE)
            stroka_table_words[i].append(a)

    stroka_top = [Paragraph(i, CUSTOM_PARAGRAPH_STYLE) for i in loaded_dict['text_top'][:]]
    stroka_bot = [Paragraph(i, SIGNATURE_PARAGRAPH_STYLE) for i in loaded_dict['text_bot']] # перед и после таблицы
    stroka_bot2 = [Paragraph(i, CUSTOM_PARAGRAPH_STYLE) for i in loaded_dict['text_bot2']]  # перед и после таблицы

    lst_date = format_date_table(stroka_table_words[0], stroka_table_words[1], date, TAB_PARAGRAPH_STYLE, KALEND_PO_EPIDEM_PAKAZ, NATION_KALENDAR, REGION_KALENDAR, col_widths)

    table = Table(lst_date, colWidths=col_widths) #создание таблицы и применение стиля
    table.setStyle(STYLE)
    table.hAlign = 'LEFT' # выравнивание по левому краю

    # Добавляем отступы с помощью Spacer
    content_table = [Spacer(1, cm_to_points(0.5)), table, Spacer(1, cm_to_points(0.5))]
    content: list = stroka_top + content_table + stroka_bot + [Spacer(1, cm_to_points(0.5))] + stroka_bot2

    doc.build(content) # Добавляем данные в документ

if __name__== '__main__':
    date = {'name': 'III ii ii', 'date': [['10-31-31', 'Гепатит А', 'rv']], 'gender': 'м', 'id' : 5543}
    #date = data_person(1)
    #print(date)
    #date = date_person(1)
    generate_pdf(date)
