from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtWidgets import QTableWidgetItem


class DataContainer:
    def __init__(self):
        self.rows = []
        self.pers_info = {}

    def get_data(self):
        return self.rows

    def update_data(self, row, col, value):
        """Обновляет данные в конкретной ячейке"""
        if 0 <= row < len(self.rows) and 0 <= col < len(self.rows[row]):
            self.rows[row][col] = value
            #print("Updated Data:", self.rows)

    def add_row(self, index):
        """Добавляет новую пустую строку"""
        new_row = ["", "", ""]  # Пустая строка по умолчанию
        self.rows.insert(index, new_row)
        #print("Added Row:", self.rows)

    def remove_row(self, index):
        """Удаляет строку по индексу"""
        if 0 <= index < len(self.rows):
            del self.rows[index]
            #print("Removed Row:", self.rows)
        else:
            print("Invalid index for removal:", index)


class DataController:
    def __init__(self, data_container, table_widget):
        self.data_container = data_container
        self.table_widget = table_widget

        # Инициализация таблицы
        self.load_data_to_table()

        # Подключаем сигнал изменения ячейки
        self.table_widget.itemChanged.connect(self.update_data_container)

    def load_data_to_table(self):
        """Заполняет таблицу данными из DataContainer"""
        data = self.data_container.get_data()

        self.table_widget.blockSignals(True)  # Блокируем сигналы, чтобы избежать рекурсии
        self.table_widget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row_idx, col_idx, item)

        self.table_widget.blockSignals(False)  # Разблокируем сигналы

    def update_data_container(self, item):
        """Обновляет данные в DataContainer при редактировании ячейки"""
        row = item.row()
        col = item.column()
        new_value = item.text()

        # Обновляем данные в DataContainer
        self.data_container.update_data(row, col, new_value)

    def add_row(self):
        """Добавляет строку в DataContainer и обновляет таблицу"""
        self.data_container.add_row()
        self.load_data_to_table()

    def remove_row(self):
        """Удаляет выделенную строку в DataContainer и обновляет таблицу"""
        selected_items = self.table_widget.selectedItems()

        if selected_items:
            # Получаем индекс выделенной строки
            selected_row = selected_items[0].row()

            # Удаляем строку в DataContainer
            self.data_container.remove_row(selected_row)

            # Обновляем таблицу
            self.load_data_to_table()
        else:
            print("No row selected for removal.")