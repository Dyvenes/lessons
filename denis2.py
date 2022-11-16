from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class Choise_figure(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ВЫБОР ФИГУРЫ')
        self.verticalLayout = QVBoxLayout(self)
        self.HorLayout = QHBoxLayout(self)
        self.label = QLabel(self)
        self.label.setText('выберите фигуру, которой станет пешка:')
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout(self)
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setText('Queen')
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setText('Rook')
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setText('Knight')
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QPushButton(self)
        self.pushButton.setText('Bishop')
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.click)
        self.pushButton_3.clicked.connect(self.click)
        self.pushButton_4.clicked.connect(self.click)

    def click(self):
        pass


class Choise_color(QWidget):
    def __init__(self):
        super(Choise_color, self).__init__()
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(QLabel('Выберите цвет, за который будете играть', self))
        self.layout().addChildLayout(QHBoxLayout(self))
        self.whitebtn = QPushButton('БЕЛЫЙ', self)
        self.blackbtn = QPushButton('ЧЕРНЫЙ', self)
        self.layout().layout().addWidget(QPushButton('БЕЛЫЙ', self))
        self.layout().layout().addWidget(QPushButton('ЧЕРНЫЙ', self))
        self.whitebtn.clicked.connect(pyqtSignal('WHITE'))
        self.blackbtn.clicked.connect(pyqtSignal('BLACK'))
