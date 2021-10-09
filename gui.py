import sys, random

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.Application import Ui_MainWindow

'''
Wrapper for the main window UI.
'''
class MainWindow(QMainWindow):
    APPLICATION_VERSION = "0.0.1"

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setTitle()

        # Actions

        self.ui.actionExit.triggered.connect(self.close)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.ui.canvasLayout = QVBoxLayout(self.ui.rightCol)
        self.canvas = CanvasWidget()
        self.canvas.setSizePolicy(size)
        self.ui.canvasLayout.addWidget(self.canvas)

        # Status Bar

        self.statusCurrentTarget = QLabel()
        self.statusMPos = QLabel()
        self.ui.statusBar.addPermanentWidget(self.statusCurrentTarget, 5)
        self.ui.statusBar.addPermanentWidget(self.statusMPos, 1)
        self.statusCurrentTarget.setText("")
        self.statusMPos.setText("")

        # Signals

        self.canvas.sigMouseMoved.connect(self.setMouseCoords) # connect mouse movement from the canvas


    @pyqtSlot('QMouseEvent')
    def setMouseCoords(self, QMouseEvent):
        mPos = QMouseEvent.localPos()
        self.statusMPos.setText("({},{})".format(int(mPos.x()), int(mPos.y())))

    def setTitle(self, title_add=""):
        ''' Set the window title with the base title and some additional text after. '''
        title = "Scigol {}".format(self.APPLICATION_VERSION)
        if len(title_add) > 0:
            title += " – " + title_add

        self.setWindowTitle(title)


class CanvasWidget(QWidget):
    sigMouseMoved = pyqtSignal(QMouseEvent, name='mouseMoved')

    def __init__(self):
        QWidget.__init__(self)        
        self.setMouseTracking(True)

    def paintEvent(self, e):
        ''' . '''
        p = QPainter()
        p.begin(self)
        self.drawElements(p)
        p.end()

    def drawPoints(self, p):
        p.setPen(Qt.red)
        size = self.size()

        if size.height() <= 1 or size.height() <= 1:
            return

        p.fillRect(0, 0, size.width(), size.height(), QColor(0,0,0))

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            p.drawPoint(x, y)

    def mouseMoveEvent(self, QMouseEvent):
        ''' QMouseEvent '''
        mPos = QMouseEvent.localPos()
        print(mPos.x(), mPos.y())
        self.sigMouseMoved.emit(QMouseEvent)

    def keyPressEvent(self, QKeyEvent):
        ''' QKeyEvent '''
        print("key!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
