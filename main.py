import sys
import sqlite3
import traceback
import datetime

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QAbstractItemView, QFileDialog, QTableWidgetItem, \
    QTableWidget, QTextEdit, QStyledItemDelegate, QComboBox, QLineEdit
from PySide6.QtCore import Slot, QDate, Qt, QRegularExpression

from pdf_settings_style import RENAME_DICT
from ui_mainwindow import Ui_MainWindow
from file_create import generate_pdf
from file_db import date_person
from app_func_logic import searсh_men, mont_replace, rename_vaccine, rename_vaccine_R, ext_pers_info

from read_exel import process_excel_to_sqlite
from delegate import ComboBoxDelegate, DateDelegate
from data_storage import DataContainer, DataController

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.ui.messagesDatabase.setWidgetResizable(True)
        self.ui.messagesHome.setWidgetResizable(True)

        self.ui.scrol_content = QLabel()
        # self.ui.messagesDatabase.setWidget(self.ui.scrol_content)

        self.ui.loadTab = QLabel()
        self.ui.messagesHome.setWidget(self.ui.loadTab)

        self.ui.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)  # Установка редактируемости всех ячеек таблицы

        self.ui.addLineButton.setEnabled(False) # изначально заблокировано
        self.ui.addLineButton_2.setEnabled(False)
        self.ui.deleteLineButton.setEnabled(False)
        self.ui.deleteLineButton_2.setEnabled(False)
        self.ui.findPatients.currentTextChanged.connect(self.toggle_button_state) # сигнал изменения выбранного текста
        self.ui.findPatients_2.currentTextChanged.connect(self.toggle_button_state)

        # # устанавливаем делегат на колонку Инфекционное заболевание
        optionsDelegate = [k for k in RENAME_DICT.values()]
        self.combo_delegate = ComboBoxDelegate(optionsDelegate)
        self.ui.tableWidget_2.setItemDelegateForColumn(1, self.combo_delegate)

        optionsDelegateType = ['v', 'v1', 'v2', 'v3', 'rv', 'rv1']
        self.combo_delegateType = ComboBoxDelegate(optionsDelegateType)
        self.ui.tableWidget_2.setItemDelegateForColumn(2, self.combo_delegateType)

        self.date_delegate = DateDelegate(self)
        self.ui.tableWidget_2.setItemDelegateForColumn(0, self.date_delegate)

        self.dataContainer2 = DataContainer()
        self.dataController2 = DataController(self.dataContainer2, self.ui.tableWidget_2)
        self.ui.tableWidget_2.itemChanged.connect(self.dataController2.update_data_container)# обновление контейнера при редактировании таблицы

        self.events()
        self.settings_start()

    def settings_start(self):
        ''' стартовые настройки полей '''

        today_time = datetime.date.today() # получение текущей даты
        self.ui.dateEdit_2.setDate(QDate(today_time.year,  today_time.month, today_time.day)) #установка сегодняшней даты
        self.ui.dateEdit.setDate(QDate(today_time.year,  today_time.month, today_time.day))
        self.ui.personInfoTable.setEditTriggers(QTableWidget.NoEditTriggers) # отключаем редактирование таблицы с перс.и
        self.ui.personInfoTable_2.setEditTriggers(QTableWidget.NoEditTriggers)

    def events(self):

        self.ui.addLineButton.clicked.connect(self.add_line_table)
        self.ui.deleteLineButton.clicked.connect(self.delete_line_table)
        self.ui.addLineButton_2.clicked.connect(self.add_line_table)
        self.ui.deleteLineButton_2.clicked.connect(self.delete_line_table)

        self.ui.generatePDF.clicked.connect(lambda: self.clic_generate(self.ui.tableWidget,
                                                                       self.ui.personInfoTable, self.ui.findPatients))
        self.ui.generatePDF_2.clicked.connect(lambda: self.clic_generate(self.ui.tableWidget_2,
                                                                       self.ui.personInfoTable_2, self.ui.findPatients_2))

        self.ui.searchPatientButton.clicked.connect(lambda: self.search_pacient(self.ui.findPatients,
                    self.ui.searchPatientTextField, self.ui.fnamTextField, self.ui.surnameTextField))

        self.ui.searchPatientButton_2.clicked.connect(lambda: self.search_pacient(self.ui.findPatients_2,
                    self.ui.searchPatientTextField_2, self.ui.fnamTextField_2, self.ui.surnameTextField_2))

        self.ui.loadTable.clicked.connect(self.tab_load)
        self.ui.preview_button.clicked.connect(self.preview_notification)


    def clic_generate(self, tableWidget, personInfoTable, findPatients):
        ''' Генерация pdf '''

        data = {'date': []}
        #Считать данные из QTableWidget

        rows = tableWidget.rowCount()
        cols = tableWidget.columnCount()
        table_data = []  # Список для хранения данных
        for row in range(rows):
            row_data = []
            for col in range(cols):
                #print(row_data)
                item = tableWidget.item(row, col)
                # Проверяем, что ячейка не пустая
                if item is not None:
                    if col == 1:
                        row_data.append(rename_vaccine_R(item.text())) #['', '', '']
                    elif col == 0:
                        dat_lst = item.text().split('-')
                        row_data.append(str(f"{dat_lst[2]}-{dat_lst[1]}-{dat_lst[0]}"))
                    else:
                        row_data.append(item.text())
                else:
                    row_data.append("")  # Если пустая, добавляем пустую строку
            table_data.append(row_data)  #[[''''], [''''], [''''], ]

        print(f"Данные таблицы {table_data}")

        rows = personInfoTable.rowCount()
        cols = personInfoTable.columnCount()
        table_data_pers = []  # Список для хранения данных
        for row in range(rows):
            row_data = []
            for col in range(cols):
                # Получаем элемент таблицы
                item = personInfoTable.item(row, col)
                # Проверяем, что ячейка не пустая
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # Если пустая, добавляем пустую строку
            table_data_pers.append(row_data)


        select_text = findPatients.currentText()
        lst_select_text = select_text.split(' ') # разбиваем для выделения ID
        if len(lst_select_text[0]) != 0:
            id = int(lst_select_text[1])


        conn = sqlite3.connect('database.db')  # выделяем гендер
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT W.gender FROM worker as W WHERE W.ID = {id};")
        rows = cursor.fetchall()
        pers_info = rows
        gender = pers_info[0][0]

        # Печатаем данные таблицы
        # print(table_data)
        # print(table_data_pers)

        data['name'] = table_data_pers[0][0] + ' ' + table_data_pers[0][1] + ' ' +  table_data_pers[0][2]
        for dat in table_data:
            data['date'].append(dat)
        norm_dat = mont_replace(data['date'])
        data['date'] = norm_dat[:]
        data['id'] = id
        data['gender'] = gender
        print(f"перед генерацией {data}")

        #print(data)
        #print(norm_dat)

        try:
            generate_pdf(data)

        except Exception as f:
            error_details = traceback.format_exc()
            print(error_details)


    def search_pacient(self, findPatients, searchPatientTextField, fnamTextField, surnameTextField):
        'Поиск пациента в бд'

        findPatients.clear() # очистка предыдущего списка

        name = searchPatientTextField.toPlainText() # считываеин данных ФИО
        fname = fnamTextField.toPlainText()
        lname = surnameTextField.toPlainText()
        personInfo = [str(name).strip(), str(fname).strip(), str(lname).strip()] # список для sql запроса

        try:
            result_request = searсh_men(personInfo) # получение персональной информации в формате [('', '', '', '', ''), ()]
            #print(result_request)
            if result_request != False:
                for result in result_request:
                    self.dataContainer2.pers_info['id'] = result[0]
                    self.dataContainer2.pers_info['name'] = result[1]
                    self.dataContainer2.pers_info['firstname'] = result[2]
                    self.dataContainer2.pers_info['lastname'] = result[3]
                    self.dataContainer2.pers_info['birthday'] = result[4]
                    self.dataContainer2.pers_info['gender'] = result[5]

                    findPatients.addItem(f"id: {result[0]} {result[1]} {result[2]}"
                                             f" {result[3]} {result[4]}")

        except Exception:
            error_details = traceback.format_exc()
            print(error_details)
            #self.ui.scrol_content.setText(f"Ошибка {error_details}")
            #self.ui.scrol_content.setText(f"Ошибка!!! Такой человек не найден в БД")


    def preview_notification(self):
        ''' Предпросмотр уведомления '''

        deadline_date = self.ui.dateEdit.date() # получаем дату из dateEdit и приводим к формату
        lst_deadline = deadline_date.toString("yyyy-MM-dd")
        deadline_date = datetime.datetime(int(lst_deadline.split('-')[0]), int(lst_deadline.split('-')[1]), int(lst_deadline.split('-')[2]))

        self.ui.tableWidget.setRowCount(0)
        self.ui.personInfoTable.setRowCount(0) # удаляем все старые строки перед новым нажатием

        select_text = self.ui.findPatients.currentText() # строка из findPatients
        lst_select_text = select_text.split(' ') # разбиваем для выделения ID

        if len(lst_select_text[0]) != 0: #? подумать над условием
            #print(lst_select_text[1])
            id = int(lst_select_text[1])

            date = date_person(id, deadline_date) # рассчет данных (id и до какой даты (формат класса datetime))
            print('-----')
            print(date)

            row_pos_persinfo = self.ui.personInfoTable.rowCount() # получаем количество строк
            self.ui.personInfoTable.insertRow(row_pos_persinfo) # вставляем новую строку

            for column, value in enumerate(date['name'].split(' ')):
                self.ui.personInfoTable.setItem(row_pos_persinfo, column, QTableWidgetItem(value))

            for column, value in enumerate(date['post_division']):
                self.ui.personInfoTable.setItem(row_pos_persinfo, column+3, QTableWidgetItem(value))

            # для нижней таблицы
            for row_data in date['date']:
                row_pos_vacinfo = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_pos_vacinfo)

                for column, value in enumerate(row_data[:]):
                    if column == 0:
                       dat_lst = value.split('-')
                       self.ui.tableWidget.setItem(row_pos_vacinfo, column, QTableWidgetItem(str(f"{dat_lst[2]}-{dat_lst[1]}-{dat_lst[0]}")))
                    elif column == 1:
                        self.ui.tableWidget.setItem(row_pos_vacinfo, column, QTableWidgetItem(rename_vaccine(value)))
                    else:
                        self.ui.tableWidget.setItem(row_pos_vacinfo, column, QTableWidgetItem(value))


    def tab_load(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*);;CSV файлы (*.csv)")
        if file_path:
            print(f"Путь к выбранному файлу: {file_path}")
            try:
                process_excel_to_sqlite(file_path, 'database.db')
                self.ui.loadTab.setText('Таблица загружена')
            except Exception:
                self.ui.loadTab.setText('Ошибка загрузка таблицы')


    def add_line_table(self):
        sender = self.sender() # кнопка, которая вызвала функци.

        if sender == self.ui.addLineButton:
            row_position = self.ui.tableWidget.rowCount()  # Получаем текущее количество строк
            self.ui.tableWidget.insertRow(row_position)    # Вставляем новую строку

        if sender == self.ui.addLineButton_2:
            row_position = self.ui.tableWidget_2.rowCount()

            if row_position == 0: # если первый раз нажали добавить строчку
                row_position_persinfo = self.ui.personInfoTable_2.rowCount() # если еще ничего не добавлено в перс.инфо
                select_text = self.ui.findPatients_2.currentText()

                if row_position_persinfo == 0 and len(select_text) != 0:
                    id = int(select_text.split(' ')[1])  # ID
                    date = ext_pers_info(id)

                    row_pos_persinfo = self.ui.personInfoTable_2.rowCount()  # получаем количество строк
                    self.ui.personInfoTable_2.insertRow(row_pos_persinfo)  # вставляем новую строку

                    for column, value in enumerate(date['name'].split(' ')):
                        self.ui.personInfoTable_2.setItem(row_pos_persinfo, column, QTableWidgetItem(value))

                    for column, value in enumerate(date['post_division']):
                        self.ui.personInfoTable_2.setItem(row_pos_persinfo, column + 3, QTableWidgetItem(value))

            self.ui.tableWidget_2.insertRow(row_position)
            print(self.data_hands.rows)


    def delete_line_table(self):
        sender = self.sender()

        if sender == self.ui.deleteLineButton:
            current_row = self.ui.tableWidget.currentRow()  # Получаем индекс выбранной строки
            if current_row != -1:                           # Проверяем, что строка выбрана
                self.ui.tableWidget.removeRow(current_row)

        if sender == self.ui.deleteLineButton_2:
            current_row = self.ui.tableWidget_2.currentRow()
            if current_row != -1:
                self.ui.tableWidget_2.removeRow(current_row)

    def toggle_button_state(self, text):
        '''блокировка кнопок при пустом элементе списка анйденных людей'''
        sender = self.sender()

        if sender == self.ui.findPatients:
            if text.strip():
                self.ui.addLineButton.setEnabled(True)
                self.ui.deleteLineButton.setEnabled(True)
            else:
                self.ui.addLineButton.setEnabled(False)
                self.ui.deleteLineButton.setEnabled(False)

        elif sender == self.ui.findPatients_2:
            if text.strip():
                self.ui.addLineButton_2.setEnabled(True)
                self.ui.deleteLineButton_2.setEnabled(True)
            else:
                self.ui.addLineButton_2.setEnabled(False)
                self.ui.deleteLineButton_2.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
