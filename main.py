import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QAbstractItemView
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


    def clic_generate(self):
        ''' Генерация pdf '''
        self.ui.scrol_content.setText(f"")

        select_text = self.ui.findPatients.currentText()

        try:
            id = int(select_text)
            date = date_person(id)
            generate_pdf(date)
            self.ui.scrol_content.setText(f"Файл сгенерирован для пациента с id = {select_text}")

        except Exception as f:
            error_details = traceback.format_exc()
            self.ui.scrol_content.setText(f"Ошибка {error_details}")

        print(1)


    def search_pacient(self):
        'Поиск пациента в бд'
        self.ui.scrol_content.setText(f"")

        text = self.ui.searchPatientTextField.toPlainText() # считываеин номера пациента
        try:
            searсh_men(int(text))
            self.ui.findPatients.addItem(text)

        except Exception:
            error_details = traceback.format_exc()
            #self.ui.scrol_content.setText(f"Ошибка {error_details}")
            self.ui.scrol_content.setText(f"Ошибка!!! Такой человек не найден в БД")


    def tab_load(self):
        try:
            print(1)
            process_excel_to_sqlite('./Baza.xlsx', '1.db')
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