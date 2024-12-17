import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QAbstractItemView, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Slot
import traceback

from ui_mainwindow import Ui_MainWindow
from file_create import generate_pdf
from file_db import date_person, searсh_men
from read_exel import process_excel_to_sqlite


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

        self.events()


    def events(self):
        self.ui.addLineButton.clicked.connect(self.add_line_table)
        self.ui.deleteLineButton.clicked.connect(self.delete_line_table)
        self.ui.generatePDF.clicked.connect(self.clic_generate)
        self.ui.searchPatientButton.clicked.connect(self.search_pacient)
        self.ui.loadTable.clicked.connect(self.tab_load)
        self.ui.preview_button.clicked.connect(self.preview_notification)


    def clic_generate(self):
        ''' Генерация pdf '''
        data = {'date': []}
        #Считать данные из QTableWidget
        rows = self.ui.tableWidget.rowCount()
        cols = self.ui.tableWidget.columnCount()
        table_data = []  # Список для хранения данных
        for row in range(rows):
            row_data = []
            for col in range(cols):
                # Получаем элемент таблицы
                item = self.ui.tableWidget.item(row, col)
                # Проверяем, что ячейка не пустая
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # Если пустая, добавляем пустую строку
            table_data.append(row_data)

        rows = self.ui.personInfoTable.rowCount()
        cols = self.ui.personInfoTable.columnCount()
        table_data_pers = []  # Список для хранения данных
        for row in range(rows):
            row_data = []
            for col in range(cols):
                # Получаем элемент таблицы
                item = self.ui.personInfoTable.item(row, col)
                # Проверяем, что ячейка не пустая
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # Если пустая, добавляем пустую строку
            table_data_pers.append(row_data)

        # Печатаем данные таблицы
        # print(table_data)
        # print(table_data_pers)
        data['name'] = table_data_pers[0][0] + ' ' + table_data_pers[0][1] + ' ' +  table_data_pers[0][2]
        for dat in table_data:
            data['date'].append(dat)

        print(data)

        try:
            generate_pdf(data)

        except Exception as f:
            error_details = traceback.format_exc()
            print(error_details)


    def search_pacient(self):
        'Поиск пациента в бд'
        self.ui.findPatients.clear()

        name = self.ui.searchPatientTextField.toPlainText() # считываеин данных ФИО
        fname = self.ui.fnamTextField.toPlainText()
        lname = self.ui.surnameTextField.toPlainText()
        personInfo = [str(name), str(fname), str(lname)] # список для sql запроса

        #print(personInfo)

        try:
            result_request = searсh_men(personInfo) # получение персональной информации [('', '', ''), ()]
            #print(result_request)
            if result_request != False:
                for result in result_request:
                    self.ui.findPatients.addItem(f"id: {result[0]} {result[1]} {result[2]}"
                                             f" {result[3]} {result[4]}")

        except Exception:
            error_details = traceback.format_exc()
            print(error_details)
            #self.ui.scrol_content.setText(f"Ошибка {error_details}")
            #self.ui.scrol_content.setText(f"Ошибка!!! Такой человек не найден в БД")


    def preview_notification(self):
        select_text = self.ui.findPatients.currentText()

        lst_select_text = select_text.split(' ') #разбиваем для выделения ID
        #print(lst_select_text)
        if len(lst_select_text[0]) != 0:
            #print(lst_select_text[1])
            id = int(lst_select_text[1])
            print(f'id:  {id}')
            date = date_person(id)
            print(date)

            row_pos_persinfo = self.ui.personInfoTable.rowCount()
            self.ui.personInfoTable.insertRow(row_pos_persinfo)
            for column, value in enumerate(date['name'].split(' ')):
                self.ui.personInfoTable.setItem(row_pos_persinfo, column, QTableWidgetItem(value))

            for column, value in enumerate(date['post_division']):
                self.ui.personInfoTable.setItem(row_pos_persinfo, column+3, QTableWidgetItem(value))

            # для нижней таблицы
            for row_data in date['date']:
                row_pos_vacinfo = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_pos_vacinfo)
                for column, value in enumerate(row_data[:-1]):
                    self.ui.tableWidget.setItem(row_pos_vacinfo, column, QTableWidgetItem(value))


    def tab_load(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*);;CSV файлы (*.csv)")
        if file_path:
            print(f"Путь к выбранному файлу: {file_path}")
            try:
                print(1)
                process_excel_to_sqlite(file_path, '1.db')
                self.ui.loadTab.setText('Таблица загружена')
            except Exception:
                self.ui.loadTab.setText('Ошибка загрузка таблицы')


    def add_line_table(self):
        row_position = self.ui.tableWidget.rowCount()  # Получаем текущее количество строк
        self.ui.tableWidget.insertRow(row_position)    # Вставляем новую строку


    def delete_line_table(self):
        current_row = self.ui.tableWidget.currentRow()  # Получаем индекс выбранной строки
        if current_row != -1:                           # Проверяем, что строка выбрана
            self.ui.tableWidget.removeRow(current_row)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())