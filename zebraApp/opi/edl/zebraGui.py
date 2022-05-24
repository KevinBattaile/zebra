#!/bin/env dls-python2.7

from PyQt4.Qt import *

class Connection(QGraphicsPathItem):
    def __init__(self, port, x, y):
        # add connection from port to gate
        QGraphicsPathItem.__init__(self)
        self.x = x
        self.y = y
        self.port = port
        self.port.gate.scene.addItem(self)
        self.calcPath()
        
    def calcPath(self):
        start = self.port.gate.pos() + QPointF(self.x,self.y)
        end = self.port.pos()
        dist = abs(start.x() - end.x()) / 5
        mid1 = QPointF(start.x() - dist, start.y() + dist)
        mid2 = QPointF(end.x() + dist, end.y() + dist) 
        path = QPainterPath(start)
        path.cubicTo(mid1, mid2, end)
        self.setPath(path)
        
class InPort(QGraphicsEllipseItem):
    def __init__(self, gate, x, y):
        # add an input or output port
        QGraphicsEllipseItem.__init__(self, -10, -10, 20, 20)
        self.gate = gate        
        self.gate.scene.addItem(self)                
        self.setPos(QPointF(x, y) + self.gate.pos())        
        self.setStartAngle(135*16)
        self.setSpanAngle(90*16)
        self.setPen(QColor(160, 160, 50))
        self.setBrush(QColor(160, 160, 50, 100))
        self.setFlag(self.ItemIsMovable, True)    
        self.setFlag(self.ItemSendsGeometryChanges, True)
        self.connection = Connection(self, x, y)
        
    def itemChange(self, change, value):
        if change==self.ItemPositionHasChanged:
            self.connection.calcPath()
        return QGraphicsEllipseItem.itemChange(self, change, value)

class Gate(QGraphicsRectItem):
    LineColor = QColor(0, 0, 0)
    FillColor = QColor(255, 255, 255)        
    
    def __init__(self, scene, name):
        QGraphicsRectItem.__init__(self, 0, 0, 200, 100)
        self.scene = scene        
        self.scene.addItem(self)        
        self.setPos(100, 200)        
        self.setFlag(self.ItemIsMovable, True)    
        self.setFlag(self.ItemSendsGeometryChanges, True)
        self.setPen(self.LineColor)
        self.setBrush(self.FillColor)
        # Add a label
        self.name = name        
        text = QGraphicsTextItem(self)
        text.setPlainText(name)
        text.setPos(100-text.boundingRect().width()/2,0)
        self.addPorts()

    def addPorts(self):
        pass

class AndGate(Gate):
    LineColor = QColor("#a42")
    FillColor = QColor("#e63")        

    def addPorts(self):
        # add invert buttons
        setValue = QPushButton("Invert 1")
        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(setValue)
        proxy.setPos(100-proxy.boundingRect().width()/2, 20)
        self.inp1 = InPort(self, 10, 20)

    def itemChange(self, change, value):
        if change==self.ItemPositionHasChanged:
            self.inp1.connection.calcPath()
        return QGraphicsEllipseItem.itemChange(self, change, value)
        
class GateScene(QGraphicsScene):
    def __init__(self, P, *args):
        QGraphicsScene.__init__(self, *args)
        self.P = P
        self.setSceneRect(0, 0, 1024, 768)
        AndGate(self, "AND1")

if __name__ == "__main__":
    app = QApplication([])
    scene = GateScene(P = "TESTZEBRA:ZEBRA")
    view = QGraphicsView(scene)
    view.show()
    app.exec_()

