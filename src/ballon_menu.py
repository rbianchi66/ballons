from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math

class BallonMenu(QWidget):
    class MenuItem():
        def __init__(self, angle, caption, action):
            self.angle = angle
            self.caption = caption
            self.action = action
            self.selected = False

        def drawShadow(self, dc, pos, size):
            dc.save()
            dc.setRenderHint(QPainter.Antialiasing, True)
            color = QColor(160,160,160)
            w = size*0.54
            if self.selected:
                shadow_pos = 10
                ecolor = QColor(255,255,255,30)
                grad = QRadialGradient(pos.x(), pos.y()+shadow_pos, w, pos.x(), pos.y()+shadow_pos)
                grad.setColorAt(0.0, color)
                grad.setColorAt(0.9, color)
                grad.setColorAt(1.0, ecolor)
                dc.setPen(QPen(ecolor))
                dc.setBrush(QBrush(grad))
            else:
                shadow_pos = 3
                dc.setPen(QPen(color))
                dc.setBrush(QBrush(color))
            dc.drawEllipse(QPoint(pos.x(), pos.y()+shadow_pos), w, w)
            
            dc.restore()
            
        def drawText(self, dc, x, y, flags, text):
            size = 32767.0;
            corner = QPointF(x, y - size)
            if (flags & Qt.AlignHCenter):
                corner.setX(corner.x() - size/2.0)
            else:
                if (flags & Qt.AlignRight):
                    corner.setX(corner.x() - size)
            if (flags & Qt.AlignVCenter):
                corner.setY(corner.y() + size/2.0)
            else: 
                if (flags & Qt.AlignTop):
                    corner.setY(corner.y() + size)
                else:
                    flags |= Qt.AlignBottom
            rect = QRectF(corner.x(), corner.y(), size, size)
            dc.drawText(rect, flags, text)
            
        def draw(self, dc, pos, size):
            dc.save()
            dc.setRenderHint(QPainter.Antialiasing, True)
            w = size*0.54

            # shadow
            self.drawShadow(dc, pos, size)
            
            # background
            color = QColor(0,200,250) if self.selected else QColor(200,200,200)
            dc.setPen(QPen(color))
            dc.setBrush(QBrush(color))
            dc.drawEllipse(pos, w, w)
            
            # border
            color = QColor(120,120,120)
            dc.setPen(QPen(color))
            dc.setBrush(QBrush())
            dc.drawEllipse(pos, w, w)
            
            font = dc.font()
            font.setBold(self.selected)
            fsize = 42 if self.selected else 36
            font.setPixelSize(fsize)
            dc.setPen(QColor(0,0,0))
            w = size*0.25
            dc.setFont(font)
            
            self.drawText(dc, pos.x(), pos.y(), Qt.AlignHCenter | Qt.AlignVCenter, self.caption)
            dc.restore()
    
    def __init__(self, items):
        QWidget.__init__(self)
        self.items = items
    
    def paintEvent(self, e):
        dc = QPainter(self)
        self.draw(dc)

    def draw(self, dc):
        dc.save()
        size = min(self.width(), self.height()) / 2.0
        item_size = min(size * math.pi / len(self.items), size/2.0)
        x = self.rect().center().x()
        y = self.rect().center().y()
        for i in self.items:
            a = math.radians(i.angle-360)
            tpos = QPointF(x+math.cos(a)*size*0.7, y+math.sin(a)*size*0.7)
            i.draw(dc, tpos, item_size)
        dc.restore()


class BallonsPanel(QDialog):
    def __init__(self, **kwargs):
        QDialog.__init__(self, **kwargs)
        self.main_layout = QVBoxLayout(self)
        self.setMinimumSize(480,480)
        step = 360 / 6.0
        a = -90.0
        self.items = []
        for c in ["A","B","C","D","E","F"]:
            self.items.append(BallonMenu.MenuItem(a, c, None))
            a += step
        self.items[0].selected = True
        self.step = step
        self.main_layout.addWidget(BallonMenu(self.items))
#         c = self.rect().center()
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.updateAngles)
#         self.timer.start(50)

    def updateAngles(self):
        for i in self.items:
            i.angle += 1
            i.angle %= 360
            i.selected = 270-self.step/2 < i.angle < 270+self.step/2
        self.update()
    
       
        
def show_panel():
    pp = BallonsPanel()
    pp.setModal(True)
    pp.exec_()


if __name__ == "__main__":
    import sys
    class BallonsPanelApp(QApplication):
        def __init__(self, args):
            QApplication.__init__(self, args)
            self.setStyle(QStyleFactory.create('Cleanlooks'))
            show_panel()
            sys.exit()
    
    app = BallonsPanelApp(sys.argv)
    app.exec_()
