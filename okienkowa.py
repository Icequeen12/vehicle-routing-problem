from __future__ import print_function
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QComboBox
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5 import QtCore

from obliczanie import main


class okienkowa(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def dzialanie(self):

        try:
            url = self.adresEdt.text()
            method = self.combo.currentText()
            time = int(self.timeEdt.text())
            trucks = int(self.trucksEdt.text())
            self.close()
            main(url, method, time, trucks)

        except ValueError:
            QMessageBox.warning(self, "Błąd", "złe dane", QMessageBox.Ok)

    def interfejs(self):

        etykieta1 = QLabel("Podaj adres url Pliku", self)
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1)

        self.adresEdt = QLineEdit()
        ukladT.addWidget(self.adresEdt)

        etykieta2 = QLabel("Wybierz metahaurestyke", self)
        ukladT.addWidget(etykieta2)
        etykieta4 = QLabel("wpisz liczbę pojazdów", self)
        ukladT.addWidget(etykieta4)
        self.trucksEdt = QLineEdit()
        self.trucksEdt.setText('10')
        ukladT.addWidget(self.trucksEdt)

        self.combo = QComboBox(self)
        self.combo.addItem("FIRST_SOLUTION")
        self.combo.addItem("AUTOMATIC")
        self.combo.addItem("GREEDY_DESCENT")
        self.combo.addItem("GUIDED_LOCAL_SEARCH")
        self.combo.addItem("SIMULATED_ANNEALING")
        self.combo.addItem("TABU_SEARCH")
        ukladT.addWidget(self.combo)

        etykieta3 = QLabel("Wpisz czas", self)
        ukladT.addWidget(etykieta3)
        self.timeEdt = QLineEdit()
        self.timeEdt.setText('30')
        ukladT.addWidget(self.timeEdt)

        policzBtn = QPushButton("&Policz", self)
        ukladT.addWidget(policzBtn)

        policzBtn.clicked.connect(self.dzialanie)

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.setLayout(ukladT)
        self.resize(500, 150)
        self.setWindowTitle("VPR")
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = okienkowa()
    sys.exit(app.exec_())
