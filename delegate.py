from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox, QLineEdit


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options  # Список вариантов выбора

    def createEditor(self, parent, option, index):
        # Создаем QComboBox как редактор для ячейки
        combo_box = QComboBox(parent)
        combo_box.addItems(self.options)
        return combo_box

    def setEditorData(self, editor, index):
        # Устанавливаем начальное значение редактора из ячейки
        current_text = index.data()
        editor.setCurrentText(current_text)

    def setModelData(self, editor, model, index):
        # Сохраняем выбранное значение из редактора обратно в модель
        model.setData(index, editor.currentText())

class DateDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Создаем редактор QLineEdit
        editor = QLineEdit(parent)

        # Устанавливаем валидатор для формата "дд-мм-гггг"
        regex = QRegularExpression(r"^(0[1-9]|[12][0-9]|3[01])?(-)?(0[1-9]|1[0-2])?(-)?(\d{0,4})?$")
        validator = QRegularExpressionValidator(regex, editor)
        editor.setValidator(validator)

        # Подключаем обработку текста для автоматического добавления дефисов
        editor.textEdited.connect(self.format_date)
        return editor

    def setEditorData(self, editor, index):
        # Устанавливаем текущий текст ячейки в редактор
        editor.setText(index.data() or "")

    def setModelData(self, editor, model, index):
        # Сохраняем отредактированный текст обратно в модель
        model.setData(index, editor.text())

    def format_date(self, text):
        # Форматирование даты: автоматическое добавление дефисов
        clean_text = text.replace("-", "")  # Удаляем уже существующие дефисы
        formatted = ""

        # Автоматически добавляем дефисы после дня и месяца
        if len(clean_text) > 2:
            formatted += clean_text[:2] + "-"
            if len(clean_text) > 4:
                formatted += clean_text[2:4] + "-"
                formatted += clean_text[4:]
            else:
                formatted += clean_text[2:]
        else:
            formatted = clean_text

        self.sender().setText(formatted)  # Обновляем текст в редакторе

