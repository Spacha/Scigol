import sys, random
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.Application import Ui_MainWindow


class AppState:
    def __init__(self):
        pass


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

        # App state

        self.state = AppState()
        self.state.tool = (255,0,0)

        # Actions

        self.ui.actionExit.triggered.connect(self.close)

        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.ui.canvasLayout = QVBoxLayout(self.ui.rightCol)
        self.canvas = CanvasWidget(self.state)
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
        self.ui.tool1.clicked.connect(lambda e: self.selectTool(1, e))
        self.ui.tool2.clicked.connect(lambda e: self.selectTool(2, e))
        self.ui.tool3.clicked.connect(lambda e: self.selectTool(3, e))
        self.ui.tool4.clicked.connect(lambda e: self.selectTool(4, e))
        self.ui.tool5.clicked.connect(lambda e: self.selectTool(5, e))
        self.ui.tool6.clicked.connect(lambda e: self.selectTool(6, e))


    def selectTool(self, tool, e):
        if tool == 1:
            self.state.tool = (255,0,0)
        elif tool == 2:
            self.state.tool = (0,255,0)
        elif tool == 3:
            self.state.tool = (0,0,255)
        self.statusCurrentTarget.setText("Tool " + str(tool))

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

class CanvasElement:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.x = 0
        self.y = 0
        self.enabled = False
        self.width = 40
        self.height = 40

    def place(self, x, y):
        self.setPosition(x, y)
        self.enabled = True

    def setPosition(self, x, y):
        self.x = x - self.width//2
        self.y = y - self.width//2

class CanvasWidget(QWidget):
    sigMouseMoved = pyqtSignal(QMouseEvent, name='mouseMoved')

    def __init__(self, app):
        QWidget.__init__(self)        
        self.setMouseTracking(True)
        self.app = app

        # some settings
        self.backgroundColor = QColor(20,20,20)
        self.gridColor = QColor(25,25,25)
        self.showGrid = True
        self.gridSpacing = 10

        self.elements = []

    def placeElement(self, x, y):
        lastElemId = len(self.elements)
        elem = CanvasElement("Element #"+ str(lastElemId + 1), QColor(*self.app.tool))
        elem.place(x, y) # should be: schema.place(elem)
        self.elements.append(elem)
        self.repaint()

    def paintEvent(self, e):
        ''' . '''
        p = QPainter()
        p.begin(self)
        self.drawBackground(p)
        self.drawCanvasElements(p)
        p.end()

    def drawBackground(self, p):
        size = self.size()

        # background color
        p.fillRect(0, 0, size.width(), size.height(), self.backgroundColor)

        # draw the grid
        if self.showGrid:
            # gridLines = np.array([None]*(size.width()/self.gridSpacing-1)) # number of vertical lines
            gridLines = []

            # vertical lines
            for lx in range(self.gridSpacing, size.width(), self.gridSpacing):
                gridLines.append(QLineF(lx, 0, lx, size.height()))
            # horizontal lines
            for ly in range(self.gridSpacing, size.height(), self.gridSpacing):
                gridLines.append(QLineF(0, ly, size.width(), ly))
            p.setPen(self.gridColor)
            p.drawLines(gridLines)

    def drawCanvasElements(self, p):
        for elem in self.elements:
            if elem.color != p.pen().color():
                p.setPen(elem.color)
            p.drawRect(QRectF(elem.x, elem.y, elem.width, elem.height))

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
        self.sigMouseMoved.emit(QMouseEvent)

    def mousePressEvent(self, QMouseEvent):
        ''' QMouseEvent '''
        self.mPressPos = QMouseEvent.localPos()

    def mouseReleaseEvent(self, QMouseEvent):
        ''' QMouseEvent '''
        mPos = QMouseEvent.localPos()
        if mPos == self.mPressPos:
            self.placeElement(mPos.x(), mPos.y())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
