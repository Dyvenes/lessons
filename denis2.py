from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup
from PyQt5.QtCore import pyqtSignal
from choise_color import Ui_Form


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


class Choise_color(QWidget, Ui_Form):
    color = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        self.color.emit(btn.text())
        self.close()
