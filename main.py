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
from app_func_logic import searсh_men, mont_replace, rename_vaccine, rename_vaccine_R

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

        self.ui.change.setEnabled(False) # изначально заблокировано
        self.ui.addLineButton_2.setEnabled(False)
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

        self.ui.change.clicked.connect(self.change_tab)
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
        currentID = self.dataContainer2.currentId
        data = {'date': []}

        table_data = self.dataContainer2.rows  # Список для хранения данных
        for n, row in enumerate(table_data):
            dat = row[0].split('-')
            table_data[n][0] = str(f"{dat[2]}-{dat[1]}-{dat[0]}")
            table_data[n][1] = rename_vaccine_R(row[1])

        print(f"Данные таблицы {table_data}")

        data['name'] = (self.dataContainer2.pers_info[currentID]['name'] + ' ' +
                        self.dataContainer2.pers_info[currentID]['lastname'] + ' ' +
                        self.dataContainer2.pers_info[currentID]['firstname'])

        for dat in table_data:
            data['date'].append(dat)

        norm_dat = mont_replace(data['date']) # ['2024-12-23'] -> ['Ноябрь 2024']
        data['date'] = norm_dat[:]
        data['id'] = self.dataContainer2.currentId
        data['gender'] = self.dataContainer2.pers_info[currentID]['gender']
        print(f"перед генерацией {data}")

        print(data)
        #print(norm_dat)

        try:
            generate_pdf(data)

        except Exception as f:
            error_details = traceback.format_exc()
            print(error_details)


    def search_pacient(self, findPatients, searchPatientTextField, fnamTextField, surnameTextField):
        '''  Поиск пациента в бд '''

        findPatients.clear() # очистка предыдущего списка

        name = searchPatientTextField.toPlainText() # считываеин данных ФИО
        fname = fnamTextField.toPlainText()
        lname = surnameTextField.toPlainText()
        personInfo = [str(name).strip(), str(fname).strip(), str(lname).strip()] # список для sql запроса

        try:
            result_request = searсh_men(personInfo) # получение персональной информации в формате [('', '', '', '', ''), ()]
            self.dataContainer2.pers_info = {}  # очищаем контейнер  перс. инф. при новом поиске

            if result_request != False:
                self.dataContainer2.update_pers_info(result_request) # обновляем контейнер

                for result in result_request:
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
                self.dataController2.add_row()


    def delete_line_table(self):
        sender = self.sender()

        if sender == self.ui.deleteLineButton:
            current_row = self.ui.tableWidget.currentRow()  # Получаем индекс выбранной строки
            if current_row != -1:                           # Проверяем, что строка выбрана
                self.ui.tableWidget.removeRow(current_row)

        if sender == self.ui.deleteLineButton_2:
            self.dataController2.remove_row()

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
                self.dataContainer2.currentId = int(text.split()[1]) # обновляем выбранного пациента ID при смене

                self.ui.personInfoTable_2.setRowCount(0) #очищаем таблицу перс.инфы
                self.ui.personInfoTable_2.insertRow(0)  # вставляем новую строку
                listParametrs = ['firstname', 'name', 'lastname', 'namePos', 'division']
                for column, value in enumerate([self.dataContainer2.pers_info[self.dataContainer2.currentId][i]
                                               for i in listParametrs]):
                    self.ui.personInfoTable_2.setItem(0, column, QTableWidgetItem(value))

                self.ui.addLineButton_2.setEnabled(True)
                self.ui.deleteLineButton_2.setEnabled(True)
            else:
                self.ui.personInfoTable_2.setRowCount(0) # удаляем строки обоих таблиц
                self.dataContainer2.rows = []
                self.dataController2.load_data_to_table()

                self.ui.addLineButton_2.setEnabled(False)
                self.ui.deleteLineButton_2.setEnabled(False)

    def change_tab(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
