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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1078, 845)
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
        self.messagesHome = QScrollArea(self.home)
        self.messagesHome.setObjectName(u"messagesHome")
        self.messagesHome.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1034, 705))
        self.messagesHome.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.messagesHome)

        self.loadTable = QPushButton(self.home)
        self.loadTable.setObjectName(u"loadTable")

        self.verticalLayout.addWidget(self.loadTable)

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
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.nameLabel = QLabel(self.widget)
        self.nameLabel.setObjectName(u"nameLabel")

        self.horizontalLayout.addWidget(self.nameLabel)

        self.searchPatientTextField = QTextEdit(self.widget)
        self.searchPatientTextField.setObjectName(u"searchPatientTextField")
        self.searchPatientTextField.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.searchPatientTextField)

        self.fnameLabel = QLabel(self.widget)
        self.fnameLabel.setObjectName(u"fnameLabel")

        self.horizontalLayout.addWidget(self.fnameLabel)

        self.fnamTextField = QTextEdit(self.widget)
        self.fnamTextField.setObjectName(u"fnamTextField")

        self.horizontalLayout.addWidget(self.fnamTextField)

        self.surnameLabel = QLabel(self.widget)
        self.surnameLabel.setObjectName(u"surnameLabel")

        self.horizontalLayout.addWidget(self.surnameLabel)

        self.surnameTextField = QTextEdit(self.widget)
        self.surnameTextField.setObjectName(u"surnameTextField")

        self.horizontalLayout.addWidget(self.surnameTextField)

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

        self.widget_3 = QWidget(self.database)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(16777215, 30))
        self.widget_3.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.preview_button = QPushButton(self.widget_3)
        self.preview_button.setObjectName(u"preview_button")

        self.horizontalLayout_2.addWidget(self.preview_button)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(15, 16777215))
        self.label_2.setMargin(2)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.dateEdit_2 = QDateEdit(self.widget_3)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setEnabled(False)
        self.dateEdit_2.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_2.addWidget(self.dateEdit_2)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(25, 16777215))
        self.label.setMargin(5)

        self.horizontalLayout_2.addWidget(self.label)

        self.dateEdit = QDateEdit(self.widget_3)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setMaximumSize(QSize(150, 16777215))
        self.dateEdit.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.dateEdit)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.database)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.personInfoTable = QTableWidget(self.widget_2)
        if (self.personInfoTable.columnCount() < 5):
            self.personInfoTable.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.personInfoTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.personInfoTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.personInfoTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.personInfoTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.personInfoTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.personInfoTable.setObjectName(u"personInfoTable")
        self.personInfoTable.setMaximumSize(QSize(16777215, 100))
        self.personInfoTable.setStyleSheet(u"")
        self.personInfoTable.horizontalHeader().setCascadingSectionResizes(False)
        self.personInfoTable.horizontalHeader().setDefaultSectionSize(200)
        self.personInfoTable.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.personInfoTable.horizontalHeader().setStretchLastSection(True)
        self.personInfoTable.verticalHeader().setHighlightSections(True)
        self.personInfoTable.verticalHeader().setProperty(u"showSortIndicator", False)
        self.personInfoTable.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.personInfoTable)

        self.tableWidget = QTableWidget(self.widget_2)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)

        self.verticalLayout_3.addWidget(self.tableWidget)

        self.change = QPushButton(self.widget_2)
        self.change.setObjectName(u"change")

        self.verticalLayout_3.addWidget(self.change)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.tabWidget.addTab(self.database, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_5 = QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_4 = QWidget(self.tab)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 30))
        self.widget_4.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.nameLabel_2 = QLabel(self.widget_4)
        self.nameLabel_2.setObjectName(u"nameLabel_2")

        self.horizontalLayout_3.addWidget(self.nameLabel_2)

        self.searchPatientTextField_2 = QTextEdit(self.widget_4)
        self.searchPatientTextField_2.setObjectName(u"searchPatientTextField_2")
        self.searchPatientTextField_2.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_3.addWidget(self.searchPatientTextField_2)

        self.fnameLabel_2 = QLabel(self.widget_4)
        self.fnameLabel_2.setObjectName(u"fnameLabel_2")

        self.horizontalLayout_3.addWidget(self.fnameLabel_2)

        self.fnamTextField_2 = QTextEdit(self.widget_4)
        self.fnamTextField_2.setObjectName(u"fnamTextField_2")

        self.horizontalLayout_3.addWidget(self.fnamTextField_2)

        self.surnameLabel_2 = QLabel(self.widget_4)
        self.surnameLabel_2.setObjectName(u"surnameLabel_2")

        self.horizontalLayout_3.addWidget(self.surnameLabel_2)

        self.surnameTextField_2 = QTextEdit(self.widget_4)
        self.surnameTextField_2.setObjectName(u"surnameTextField_2")

        self.horizontalLayout_3.addWidget(self.surnameTextField_2)

        self.searchPatientButton_2 = QPushButton(self.widget_4)
        self.searchPatientButton_2.setObjectName(u"searchPatientButton_2")
        self.searchPatientButton_2.setMinimumSize(QSize(0, 30))
        self.searchPatientButton_2.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_3.addWidget(self.searchPatientButton_2)


        self.verticalLayout_5.addWidget(self.widget_4)

        self.findPatients_2 = QComboBox(self.tab)
        self.findPatients_2.setObjectName(u"findPatients_2")

        self.verticalLayout_5.addWidget(self.findPatients_2)

        self.generatePDF_2 = QPushButton(self.tab)
        self.generatePDF_2.setObjectName(u"generatePDF_2")

        self.verticalLayout_5.addWidget(self.generatePDF_2)

        self.widget_5 = QWidget(self.tab)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.personInfoTable_2 = QTableWidget(self.widget_5)
        if (self.personInfoTable_2.columnCount() < 5):
            self.personInfoTable_2.setColumnCount(5)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.personInfoTable_2.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.personInfoTable_2.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.personInfoTable_2.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.personInfoTable_2.setHorizontalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.personInfoTable_2.setHorizontalHeaderItem(4, __qtablewidgetitem12)
        self.personInfoTable_2.setObjectName(u"personInfoTable_2")
        self.personInfoTable_2.setMaximumSize(QSize(16777215, 100))
        self.personInfoTable_2.setStyleSheet(u"")
        self.personInfoTable_2.horizontalHeader().setCascadingSectionResizes(False)
        self.personInfoTable_2.horizontalHeader().setDefaultSectionSize(200)
        self.personInfoTable_2.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.personInfoTable_2.horizontalHeader().setStretchLastSection(True)
        self.personInfoTable_2.verticalHeader().setHighlightSections(True)
        self.personInfoTable_2.verticalHeader().setProperty(u"showSortIndicator", False)
        self.personInfoTable_2.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.personInfoTable_2)

        self.tableWidget_2 = QTableWidget(self.widget_5)
        if (self.tableWidget_2.columnCount() < 3):
            self.tableWidget_2.setColumnCount(3)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem15)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setLineWidth(1)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(False)

        self.verticalLayout_4.addWidget(self.tableWidget_2)

        self.addLineButton_2 = QPushButton(self.widget_5)
        self.addLineButton_2.setObjectName(u"addLineButton_2")

        self.verticalLayout_4.addWidget(self.addLineButton_2)

        self.deleteLineButton_2 = QPushButton(self.widget_5)
        self.deleteLineButton_2.setObjectName(u"deleteLineButton_2")

        self.verticalLayout_4.addWidget(self.deleteLineButton_2)


        self.verticalLayout_5.addWidget(self.widget_5)

        self.tabWidget.addTab(self.tab, "")

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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.loadTable.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0442\u0430\u0431\u043b\u0438\u0446\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home), QCoreApplication.translate("MainWindow", u"\u0413\u043b\u0430\u0432\u043d\u0430\u044f", None))
        self.nameLabel.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f", None))
        self.searchPatientTextField.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.fnameLabel.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.fnamTextField.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0444\u0430\u043c\u0438\u043b\u0438\u044e \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.surnameLabel.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.surnameTextField.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043e\u0442\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.searchPatientButton.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0439\u0442\u0438 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.generatePDF.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c PDF", None))
        self.preview_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e", None))
        ___qtablewidgetitem = self.personInfoTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None));
        ___qtablewidgetitem1 = self.personInfoTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f", None));
        ___qtablewidgetitem2 = self.personInfoTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None));
        ___qtablewidgetitem3 = self.personInfoTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c", None));
        ___qtablewidgetitem4 = self.personInfoTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0443\u0435\u043c\u044b\u0439 \u0441\u0440\u043e\u043a", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u0435\u043a\u0446\u0438\u043e\u043d\u043d\u043e\u0435 \u0437\u0430\u0431\u043e\u043b\u0435\u0432\u0430\u043d\u0438\u0435", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0438\u043f", None));
        self.change.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.database), QCoreApplication.translate("MainWindow", u"database.sqlite", None))
        self.nameLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f", None))
        self.searchPatientTextField_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.fnameLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.fnamTextField_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0444\u0430\u043c\u0438\u043b\u0438\u044e \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.surnameLabel_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.surnameTextField_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043e\u0442\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.searchPatientButton_2.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0439\u0442\u0438 \u043f\u0430\u0446\u0438\u0435\u043d\u0442\u0430", None))
        self.generatePDF_2.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c PDF", None))
        ___qtablewidgetitem8 = self.personInfoTable_2.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None));
        ___qtablewidgetitem9 = self.personInfoTable_2.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f", None));
        ___qtablewidgetitem10 = self.personInfoTable_2.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None));
        ___qtablewidgetitem11 = self.personInfoTable_2.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c", None));
        ___qtablewidgetitem12 = self.personInfoTable_2.horizontalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None));
        ___qtablewidgetitem13 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0443\u0435\u043c\u044b\u0439 \u0441\u0440\u043e\u043a", None));
        ___qtablewidgetitem14 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u0435\u043a\u0446\u0438\u043e\u043d\u043d\u043e\u0435 \u0437\u0430\u0431\u043e\u043b\u0435\u0432\u0430\u043d\u0438\u0435", None));
        ___qtablewidgetitem15 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0438\u043f", None));
        self.addLineButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443", None))
        self.deleteLineButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
    # retranslateUi

