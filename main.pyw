from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab
import sys, tkinter
from tools import *

# // Main PyQt Window
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tkinter.Tk()
        self.setGeometry(0, 0, root.winfo_screenwidth(), root.winfo_screenheight())
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
    
    # // Setup the UI Components
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(336, 299)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selected_color = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.selected_color.setGeometry(QtCore.QRect(20, 20, 291, 251))
        self.selected_color.setObjectName("selected_color")
        self.color_display = QtWidgets.QLabel(self.centralwidget)
        self.color_display.setGeometry(QtCore.QRect(190, 150, 101, 101))
        self.color_display.setStyleSheet("border: 2px solid black;")
        self.color_display.setText("")
        self.color_display.setObjectName("color_display")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(190, 120, 101, 23))
        self.exit_button.setObjectName("exit_button")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # // UI Translation
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Color Snipper"))
        self.selected_color.setPlainText(_translate("MainWindow", "Please select a new image"))
        self.exit_button.setText(_translate("MainWindow", "Close Image"))

    # // Select new image functions
    def paintEvent(self, _):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('blue'), 1))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))
    
    # // Check if the user is trying to close
    # // the snipper
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            cv2.destroyAllWindows()
        event.accept()

    # // Track the snip positions
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    # // Update the snip positions
    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    # // Get the image from the snip positions
    def mouseReleaseEvent(self, _):
        self.close()
        img = ImageGrab.grab(bbox=(
            min(self.begin.x(), self.end.x()),
            min(self.begin.y(), self.end.y()),
            max(self.begin.x(), self.end.x()),
            max(self.begin.y(), self.end.y())
        ))
        img.save('image.png')
        Eyedrop(self).read('image.png')
    

# // Display the UI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
