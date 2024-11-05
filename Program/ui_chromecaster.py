from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Chromecaster(object):
    def setupUi(self, Chromecaster):
        Chromecaster.setObjectName("Chromecaster")
        Chromecaster.resize(557, 389)
        self.centralwidget = QtWidgets.QWidget(Chromecaster)
        self.centralwidget.setObjectName("centralwidget")
        self.btnVideo = QtWidgets.QPushButton(self.centralwidget)
        self.btnVideo.setGeometry(QtCore.QRect(300, 70, 93, 28))
        self.btnVideo.setObjectName("btnVideo")
        self.btnSRT = QtWidgets.QPushButton(self.centralwidget)
        self.btnSRT.setGeometry(QtCore.QRect(300, 130, 93, 28))
        self.btnSRT.setObjectName("btnSRT")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(120, 200, 271, 28))
        self.btnStart.setObjectName("btnStart")
        self.txtVideo = QtWidgets.QTextEdit(self.centralwidget)
        self.txtVideo.setGeometry(QtCore.QRect(120, 70, 161, 31))
        self.txtVideo.setAutoFillBackground(False)
        self.txtVideo.setObjectName("txtVideo")
        self.txtSRT = QtWidgets.QTextEdit(self.centralwidget)
        self.txtSRT.setGeometry(QtCore.QRect(120, 130, 161, 31))
        self.txtSRT.setObjectName("txtSRT")
        Chromecaster.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Chromecaster)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 557, 26))
        self.menubar.setObjectName("menubar")
        Chromecaster.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Chromecaster)
        self.statusbar.setObjectName("statusbar")
        Chromecaster.setStatusBar(self.statusbar)

        self.retranslateUi(Chromecaster)
        QtCore.QMetaObject.connectSlotsByName(Chromecaster)

    def retranslateUi(self, Chromecaster):
        _translate = QtCore.QCoreApplication.translate
        Chromecaster.setWindowTitle(_translate("Chromecaster", "MainWindow"))
        self.btnVideo.setText(_translate("Chromecaster", "Välj"))
        self.btnSRT.setText(_translate("Chromecaster", "Välj"))
        self.btnStart.setText(_translate("Chromecaster", "Starta"))
        self.txtVideo.setPlaceholderText(_translate("Chromecaster", "Film"))
        self.txtSRT.setPlaceholderText(_translate("Chromecaster", "Text"))