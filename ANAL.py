from PyQt5 import QtCore, QtGui, QtWidgets
import cv2


class FrameGrabber(QtCore.QThread):
    def __init__(self, parent=None):
        super(FrameGrabber, self).__init__(parent)

    signal = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):
        cap = cv2.VideoCapture(2)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
                self.signal.emit(image)

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.setupUi(self.MainWindow)
        self.grabber = FrameGrabber()
        self.grabber.signal.connect(self.updateFrame)
        self.grabber.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(640, 0, 200, 480))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setHorizontalHeaderLabels(['Plate', 'ReGo', 'Sanc'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    @QtCore.pyqtSlot(QtGui.QImage)
    def updateFrame(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self, MainWindow):
         _translate = QtCore.QCoreApplication.translate
         MainWindow.setWindowTitle(_translate("MainWindow", "ANPR"))
         self.label.setText(_translate("MainWindow", "Video-Label"))


    def quitApp(self):
        QtWidgets.QApplication.quit()
        
 

from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
