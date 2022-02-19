'''
    Canvas:
        * Mouse down: save the coordinates (mouseDownAt)
        * Mouse up: save the coordinates (mouseUpAt)
            * Mouse dragged = mouseDownAt != mouseUpAt
                * Yes: Pan the canvas
                * No: If active tool -> place an element
'''

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
        '''
            How do we save the canvas so that we wouldn't have to re'draw it every time we pan, zoom etc?
        '''
        startTime = time.time()
        p = QPainter()
        p.begin(self)
        self.drawBackground(p)
        self.drawCanvasElements(p)
        p.end()
        print( time.time() - startTime )

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
