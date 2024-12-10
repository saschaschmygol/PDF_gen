import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot

from ui_mainwindow import Ui_MainWindow
from file_create import generate_pdf


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.generatePDF.clicked.connect(self.clic_generate)

    def clic_generate(self):
        date = {'name': 'III ii ii', 'date': [['10-31-31', 'Дифтерия']]}
        generate_pdf(date)
        print(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())