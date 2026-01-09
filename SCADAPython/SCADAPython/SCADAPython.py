import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QFrame
from PyQt5.QtCore import QRectF, Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QLinearGradient, QPolygonF

class Rura:
    def __init__ (self, punkty, kolor_farby, grubosc = 12, kolor_rury=Qt.gray):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = kolor_rury
        self.kolor_cieczy = QColor(kolor_farby)
        self.czy_plynie = False

    def ustaw_przeplyw(self, plynie, kolor=""):
        self.czy_plynie = True
        if kolor:
            self.kolor_cieczy = kolor

    def draw(self, painter):
        if len(self.punkty)<2:
            return

        path.QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)

        pen_rura = QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen_rura)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc-4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_ciecz)
            painter.drawPath(path)

class Zbiornik:
    def __init__ (self, x, y, kolor_farby = "" , width = 100, height = 140, nazwa = "", poj = 100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.kolor_farby = QColor(kolor_farby)
        self.nazwa = nazwa
        self.pojemnosc = float(poj)
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0

    def dodaj_ciecz (self, ilosc):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_ciecz(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc/self.pojemnosc

    def czy_pusty(self):
        return self.aktualna_ilosc <= 0.1
    def czy_pelny(self):
        return self.aktualna_ilosc >= self.pojemnosc-0.1

    #def punkt_gora_srodek(self):return(self.x+self.width/2, self.y)
    def punkt_dol_srodek(self):return(self.x+self.width/2, self.y+self.height)

    def draw(self, painter):
        if self.poziom>0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height - h_cieczy
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.kolor_farby))
            painter.drawRect(int(self.x+3), int(y_start), int(self.width-6), int(h_cieczy-2))
        
        pen = QPen(Qt.white, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))

        painter.setPen(Qt.black)
        painter.drawText(int(self.x), int(self.y-10), self.nazwa)

        procent = int(self.poziom*100)
        painter.drawText(QRectF(self.x, self.y, self.width, self.height), Qt.AlignCenter, f"{procent}%")


class Zawor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.otwarty = False

        def ustaw_stan(self, otwarty):
            self.otwarty = otwarty

        def draw(self, painter):
            cx = self.x
            cy = self.y
            w = 18
            h = 15
            
            kolor = QColor("#00FF00") if self.otwarty else QColor("#FF0000")

            painter.setPen(QPen(Qt.black, 1))
            painter.setBrush(kolor)

            trojkat_lewy = QPolygonF([
                QPointF(cx, cy),
                QPointF(cx-w, cy - h),
                QPointF(cx - w, cy + h)
            ])

            painter.drawPolygon(trojkat_lewy)

            trojkat_prawy = QPolygonF([
                QPointF(cx, cy),
                QPointF(cx + w, cy - h),
                QPointF(cx + w, cy + h)
            ])
            painter.drawPolygon(trojkat_prawy)

class Mieszadlo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.kat = 0
        self.aktywne = False

        def aktualizuj(self):
            if self.aktywne:
                self.kat = (self.kat + 20 ) % 360
        
        def draw(self, painter):
            painter.save()
    

class AplikacjaSCADA(QWidget):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("Mieszalnik farb CMYK")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color: #F0F0F0")

        self.z_c = Zbiornik(50, 50, kolor_farby = "#00FFFF", nazwa="CYAN")
        self.z_c.aktualna_ilosc = 100.0
        self.z_c.aktualizuj_poziom()

        self.z_y = Zbiornik(250, 50, kolor_farby = "#FF00FF", nazwa= "YELLOW")
        self.z_y.aktualna_ilosc = 100.0
        self.z_y.aktualizuj_poziom()

        self.z_m = Zbiornik(450, 50, kolor_farby = "#FFFF00", nazwa= "MAGENTA")
        self.z_m.aktualna_ilosc = 100.0
        self.z_m.aktualizuj_poziom()

        self.z_k = Zbiornik(650, 50, kolor_farby = "#000000", nazwa= "BLACK")
        self.z_k.aktualna_ilosc = 100.0
        self.z_k.aktualizuj_poziom()

        self.mikser = Zbiornik(275, 350, kolor_farby= "FFFFFF", width=200, height=140, nazwa = "MIESZALNIK", poj=200)

        self.zbiorniki = {'C': self.z_c, 'M' : self.z_m, 'Y': self.z_y, 'K': self.z_k}


    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        for z in self.zbiorniki.values() : z.draw(p)
        self.mikser.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = AplikacjaSCADA()
    okno.show()
    sys.exit(app.exec())

