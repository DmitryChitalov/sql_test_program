# -*- coding: utf-8 -*-

# Импорт модулей библиотеки
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QDockWidget, \
    QGridLayout, QFrame, QListWidget, QDesktopWidget, QApplication, QStyle

# Импорт класса модального окна
from forms.db_choose_form import db_choose_class

# Разметка структуры главного окна
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Создаем панель инструментов
        tool_bar = QToolBar()
        # Добавляем панель инструментов в окно
        self.addToolBar(QtCore.Qt.TopToolBarArea, tool_bar)
        # Создаем кнопку для панели инструментов
        database_open = QAction(self)
        # Создаем иконку для кнопки
        database_open_ico = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        # Устанавливаем иконку на кнопку
        database_open.setIcon(database_open_ico)
        # Устанавливаем подсказку на кнопку
        database_open.setToolTip('Выбрать базу данных')
        # Устанавливаем обработчик события нажатия на кнопку
        database_open.triggered.connect(self.on_database_open)
        # Добавляем кнопку на панель инструментов
        tool_bar.addAction(database_open)

        # Создаем верхний виджет главного окна
        # для выбора базы данных
        self.tdw = QDockWidget()
        # Отключаем свойства верхнего виджета (разворот, закрытие)
        self.tdw.setFeatures(self.tdw.NoDockWidgetFeatures)
        # Создаем сетку для элементов вернего виджета
        self.tdw_grid = QGridLayout()
        # Устанавливаем фактор растяжения для выравнивания содержимого виджета
        # по левому краю
        self.tdw_grid.setColumnStretch(2, 1)
        # Создаем фрейм для размещения сетки с элементами
        tdw_frame = QFrame()
        # Вызываем метод установки менеджера расположения
        # помещаем сетку во фрейм
        tdw_frame.setLayout(self.tdw_grid)
        # Помещаем фрейм в виджет
        self.tdw.setWidget(tdw_frame)

        # Создаем нижний виджет главного окна
        # для вывода служебных сообщений
        self.smdw = QDockWidget()
        # Устанавливаем размеры нижнего виджета
        self.smdw.setFixedSize(1400, 80)
        # Отключаем свойства нижнего виджета (разворот, закрытие)
        self.smdw.setFeatures(self.smdw.NoDockWidgetFeatures)
        # Создаем виджет-список
        self.smdw_lw = QListWidget()

    # Функция загрузки модального окна выбора базы данных
    def on_database_open(self):
        # Создаем экземпляр класса модального окна
        db_choose_win = db_choose_class(self)
        # Устанавливаем заголовок модального окна
        db_choose_win.setWindowTitle('Форма выбора базы данных')
        # Центрируем модальное окно
        # сначала отображаем окно
        print(db_choose_win)
        db_choose_win.show()
        # определяем геометрию экрана
        screen = QDesktopWidget().screenGeometry()
        # определяем координату x
        x = int((screen.width() - db_choose_win.width()) / 2)
        # определяем координату y
        y = int((screen.height() - db_choose_win.height()) / 2)
        # перемещаем окно (его левый верхний край в точку с координатами x,y)
        db_choose_win.move(x, y)

# Запускаем данный модуль как основную программу
if __name__ == "__main__":
    # Создаем объект приложения (экземпляр QApplication)
    # каждое приложение на PyQt5 должно создавать объект приложения
    app = QApplication(sys.argv)
    # Создаем экземпляр главного окна
    MW = MainWindow()
    # Устанавливаем заголовок главного окна
    MW.setWindowTitle('Программа для тестирования SQL запросов')
    # Фиксируем размеры главного окна
    MW.setFixedSize(700, 500)
    # Отображаем главное окна
    MW.show()
    # Вызываем класса QApplication для инициализации приложения
    sys.exit(app.exec_())
