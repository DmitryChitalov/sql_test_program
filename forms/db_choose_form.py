# -*- coding: utf-8 -*-

# Импорт модулей библиотеки
import sys
from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QGridLayout, \
    QLineEdit, QPushButton, QHBoxLayout, QFrame, QVBoxLayout, QFormLayout, \
    QFileDialog, QListWidgetItem, QTableView, QApplication
from ui_files import db_choose_py

# Разметка структуры модального окна выбора базы данных
class db_choose_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Создаем переменную главного окна со ссылкой на родителя
        global par
        par = parent

        # Создаем экземпляр интерфейса
        self.ui = db_choose_py.Ui_db_choose_class()
        # Связываем экземпляр интерфейса с данным окном
        self.ui.setupUi(self)

        # Устанавливаем фрейм параметров для Postgres невидимым
        self.ui.postgres_frame.setVisible(False)
        # Изменяем высоту окна
        self.setFixedHeight(180)
        # Изменяем высоту главного фрейма
        self.ui.form_frame.setFixedHeight(160)
        # Поднимаем кнопки
        self.ui.save_btn.move(80, 120)
        self.ui.cancel_btn.move(190, 120)

        # Привязываем обработчики нажатия на радио-кнопки
        self.ui.radio_button_1.toggled.connect(self.on_sqlite_radio_clicked)
        self.ui.radio_button_2.toggled.connect(self.on_postgres_radio_clicked)
        self.ui.pushButton.clicked.connect(self.on_push_button_clicked)
        self.ui.cancel_btn.clicked.connect(self.on_cancel_clicked)
        self.ui.save_btn.clicked.connect(self.on_save_clicked)

        print(self.ui.pushButton)

        # Указываем, что класс db_choose_class - это виджет-окно (QtCore.Qt.Window)
        # устанавливаем для окна только кнопку закрытия (QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowModality(QtCore.Qt.WindowModal)

    # Обработчик выбора СУБД SQLite
    def on_sqlite_radio_clicked(self):
        print('sqlite')
        self.ui.sqlite_frame.setVisible(True)
        self.ui.postgres_frame.setVisible(False)
        self.setFixedHeight(180)
        self.ui.form_frame.setFixedHeight(160)
        self.ui.save_btn.move(80, 120)
        self.ui.cancel_btn.move(190, 120)

    # Обработчик выбора СУБД PostgreSQL
    def on_postgres_radio_clicked(self):
        self.ui.postgres_frame.setVisible(True)
        self.ui.postgres_frame.move(20, 70)
        self.ui.sqlite_frame.setVisible(False)
        self.setFixedHeight(300)
        self.ui.form_frame.setFixedHeight(281)
        self.ui.save_btn.move(80, 240)
        self.ui.cancel_btn.move(190, 240)
        self.ui.save_btn.setEnabled(True)

    # Обработчик выбора файла БД для СУБД SQLite
    def on_push_button_clicked(self):
        #print('вах')
        global db_path
        db_path, _filter = QFileDialog.getOpenFileName(
            None, "Open Data File", '.', "(*.sqlite *db)")
        self.ui.path_edit.setText(db_path)
        self.ui.save_btn.setEnabled(True)

    # Обработчик закрытия окна
    def on_cancel_clicked(self):
        #print('да что')
        self.close()

    # Обработчик сохранения
    def on_save_clicked(self):
        print('ой')
        global db_data_table
        # Устанавливаем соединение с SQLite
        if self.ui.radio_button_1.isChecked():
            con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            con.setDatabaseName(db_path)
            con.open()

        # Устанавливаем соединение с PostgreSQL
        if self.ui.radio_button_2.isChecked():
            con = QtSql.QSqlDatabase.addDatabase('QPSQL')
            con.setDatabaseName('frukt')
            con.setUserName('postgres')
            con.setPassword('12345')
            con.setHostName('127.0.0.1')
            con.setPort(5432)
            con.open()

        # Проверяем, установлено ли соединение
        if con.isOpen():
            msg_lbl = QLabel(
                '<span style="color:#008000;">БД успешно открыта</span>')
        else:
            msg_lbl = QLabel(
                '<span style="color:#ff0000;">Не удалось открыть БД</span>')

        # Работаем с главным окном
        # добавляем верхний виджет
        par.addDockWidget(QtCore.Qt.TopDockWidgetArea, par.tdw)
        # добавляем нижний виджет
        par.addDockWidget(QtCore.Qt.BottomDockWidgetArea, par.smdw)
        # добавляем в нижний виджет созданный вглавном окне виджет-список
        par.smdw.setWidget(par.smdw_lw)
        # назначаем нижнему виджету заголовок
        par.smdw.setWindowTitle("Служебные сообщения")
        # создаем элемент списка
        par.item = QListWidgetItem()
        # добавляем его в список
        par.smdw_lw.addItem(par.item)
        # устанавливаем в качестве элемента списка виджет-надпись
        par.smdw_lw.setItemWidget(par.item, msg_lbl)

        # Формируем содержимое верхнего виджета окна для указания пути к БД
        # надпись
        tdw_lbl = QLabel('База данных:')
        tdw_lbl.setStyleSheet("border-style: none;" "font-size: 10pt;")
        # поле ввода
        tdw_path_lbl = QLineEdit()
        tdw_path_lbl.setStyleSheet("background-color: white;"
                                        "font-size: 10pt;" "color: green;")
        tdw_path_lbl.setFixedSize(500, 25)
        if self.ui.radio_button_1.isChecked():
            tdw_path_lbl.setText(db_path)
        elif self.ui.radio_button_2.isChecked():
            tdw_path_lbl.setText(self.ui.bd_name_edit.text())
        tdw_path_lbl.setEnabled(False)
        # добавляем надпись и поле ввода в сетку верхнего виджет
        par.tdw_grid.addWidget(tdw_lbl, 0, 0,
                               alignment=QtCore.Qt.AlignCenter)
        par.tdw_grid.addWidget(tdw_path_lbl, 0, 1,
                               alignment=QtCore.Qt.AlignCenter)

        # Начинаем работать над связкой: поле ввода запроса + кнопка выполнения
        # запроса, окно вывода результата. Все это в отдельном виджете database_window
        database_window = QWidget()
        database_window.setWindowTitle("Запрос-ответ")

        # Создаем главный компоновщик виджета
        database_window_vbox = QVBoxLayout()

        # Создаем элементы для компоновщика
        # надпись
        query_lbl = QLabel('Введите запрос:')
        # поле ввода
        self.query_edit = QLineEdit()
        # создаем сетку
        query_grid = QGridLayout()
        # добавляем элементы в сетку
        query_grid.addWidget(query_lbl, 0, 0)
        query_grid.addWidget(self.query_edit, 0, 1)
        # создаем фрейм
        query_grid_frame = QFrame()
        # добавляем сетку во фрейм
        query_grid_frame.setLayout(query_grid)

        # Размещаем фрейм в главном компоновщике
        database_window_vbox.addWidget(query_grid_frame)

        # Создаем кнопку для запуска запроса на выполнение
        query_run_btn = QPushButton("Выполнить запрос")
        # Назначаем обрабочтчик нажатия кнокпи запуска запроса
        query_run_btn.clicked.connect(self.on_query_run)
        # Размещаем кнопку в главном компоновщике
        database_window_vbox.addWidget(query_run_btn)

        # Создаем надпись и класс QTableView для реализации представления
        # модель-таблица и помещаем их в гланый компоновщик
        query_run_lbl = QLabel('Результат выполнения запроса:')
        database_window_vbox.addWidget(query_run_lbl)
        db_data_table = QTableView()
        database_window_vbox.addWidget(db_data_table)

        # Размещаем главный компоновщик в виджете database_window
        database_window.setLayout(database_window_vbox)
        database_window.resize(300, 250)
        # Размещаем виджет database_window в качестве центрального в главном окне
        par.setCentralWidget(database_window)
        # Закрываем текущее модальное окно
        self.close()

    # Обработчик запуска запроса на выполнение
    def on_query_run(self):
        # Создаем объект 'модель на основе запроса'
        sqm = QtSql.QSqlQueryModel(parent=db_data_table)
        # Выполняем запрос, помещаем результаты в модель
        sqm.setQuery(self.query_edit.text())
        # Помещаем модель в виджет db_data_table
        db_data_table.setModel(sqm)
