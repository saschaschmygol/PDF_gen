# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1078, 844)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.verticalLayout = QVBoxLayout(self.home)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.loadTable = QPushButton(self.home)
        self.loadTable.setObjectName(u"loadTable")

        self.verticalLayout.addWidget(self.loadTable)

        self.messagesHome = QScrollArea(self.home)
        self.messagesHome.setObjectName(u"messagesHome")
        self.messagesHome.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1034, 704))
        self.messagesHome.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.messagesHome)

        self.tabWidget.addTab(self.home, "")
        self.database = QWidget()
        self.database.setObjectName(u"database")
        self.verticalLayout_2 = QVBoxLayout(self.database)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(self.database)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 30))
        self.widget.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.searchPatientTextField = QTextEdit(self.widget)
        self.searchPatientTextField.setObjectName(u"searchPatientTextField")
        self.searchPatientTextField.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.searchPatientTextField)

        self.searchPatientButton = QPushButton(self.widget)
        self.searchPatientButton.setObjectName(u"searchPatientButton")
        self.searchPatientButton.setMinimumSize(QSize(0, 30))
        self.searchPatientButton.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.searchPatientButton)


        self.verticalLayout_2.addWidget(self.widget)

        self.findPatients = QComboBox(self.database)
        self.findPatients.setObjectName(u"findPatients")

        self.verticalLayout_2.addWidget(self.findPatients)

        self.generatePDF = QPushButton(self.database)
        self.generatePDF.setObjectName(u"generatePDF")

        self.verticalLayout_2.addWidget(self.generatePDF)

        self.messagesDatabase = QScrollArea(self.database)
        self.messagesDatabase.setObjectName(u"messagesDatabase")
        self.messagesDatabase.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1034, 640))
        self.messagesDatabase.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_2.addWidget(self.messagesDatabase)

        self.tabWidget.addTab(self.database, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1078, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.loadTable.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home), QCoreApplication.translate("MainWindow", u"\u0413\u043b\u0430\u0432\u043d\u0430\u044f", None))
        self.searchPatientTextField.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.searchPatientButton.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0439\u0442\u0438 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.generatePDF.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c PDF", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.database), QCoreApplication.translate("MainWindow", u"database.sqlite", None))
    # retranslateUi

