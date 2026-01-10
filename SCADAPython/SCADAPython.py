import sys
from turtle import width
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

        path = QPainterPath()
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

    def punkt_gora_srodek(self):return(self.x+self.width/2, self.y)
    def punkt_dol_srodek(self):return(self.x+self.width/2, self.y+self.height)

    def draw(self, painter):

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('#F0F0F0'))
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))

        if self.poziom>0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height - h_cieczy
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.kolor_farby))
            painter.drawRect(int(self.x+2), int(y_start), int(self.width-4), int(h_cieczy-2))
        
        pen = QPen(Qt.black, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))

        painter.setPen(Qt.black)
        painter.drawText(int(self.x), int(self.y-10), self.nazwa)

        # procent = int(self.poziom*100)
        # duzyProstok = QRectF(self.x, self.y, self.width, self.height)
        # painter.drawText(duzyProstok, Qt.AlignCenter, f"{procent}%")

        procent = f"{int(self.poziom*100.0)}%"

        fm = painter.fontMetrics()
        text_rect = fm.boundingRect(procent)

        padding = 4
        bg_rect = QRectF(
            self.x+(self.width-text_rect.width())/2-padding,
            self.y + (self.height - text_rect.height())/2,
            text_rect.width()+(padding*2),
            text_rect.height()
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('#F0F0F0'))
        painter.drawRect(bg_rect)

        painter.setPen(Qt.black)
        painter.drawText(QRectF(self.x, self.y, self.width, self.height), Qt.AlignCenter, f"{procent}")


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
        painter.rotate(self.kat)

        painter.setPen(QPen(Qt.black, 4))
        painter.drawLine(-25, 0, 25, 0)
        painter.drawLine(0, -25, 0, 25)
        painter.restore()
    

class AplikacjaSCADA(QWidget):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("Mieszalnik farb CMYK")
        self.setFixedSize(1600, 800)
        self.setStyleSheet("background-color: #F0F0F0")

        #Definicja zbiornikow
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

        self.z_w = Zbiornik(850, 50, width = 200, poj = 200, kolor_farby= "#FFFFFF", nazwa= "WHITE")
        self.z_w.aktualna_ilosc=200.0
        self.z_w.aktualizuj_poziom()

        self.mikser = Zbiornik(450, 450, kolor_farby= "FFFFFF", width=200, height=140, nazwa = "MIESZALNIK", poj=200)

        self.zbiorniki = {'C': self.z_c, 'M' : self.z_m, 'Y': self.z_y, 'K': self.z_k, 'W': self.z_w}

        #Definicja rur
        p_c_start = self.z_c.punkt_dol_srodek()
        p_c_koniec = self.mikser.punkt_gora_srodek()
        mid_y = (p_c_start[1]+p_c_koniec[1])/2
        self.rura_c = Rura([p_c_start, (p_c_start[0], mid_y), (p_c_koniec[0],mid_y), p_c_koniec], kolor_farby= "#00FFFF")

        p_m_start = self.z_m.punkt_dol_srodek()
        p_m_koniec = self.mikser.punkt_gora_srodek()
        mid_y = (p_m_start[1]+p_m_koniec[1])/2
        self.rura_m = Rura([p_m_start, (p_m_start[0], mid_y),(p_m_koniec[0], mid_y), p_m_koniec], kolor_farby= "#FF00FF")

        p_y_start = self.z_y.punkt_dol_srodek()
        p_y_koniec = self.mikser.punkt_gora_srodek()
        mid_y = (p_y_start[1]+p_y_koniec[1])/2
        self.rura_y = Rura([p_y_start, (p_y_start[0], mid_y), (p_y_koniec[0],mid_y), p_y_koniec], kolor_farby= "#FFFF00")

        p_k_start = self.z_k.punkt_dol_srodek()
        p_k_koniec = self.mikser.punkt_gora_srodek()
        mid_y = (p_k_start[1]+p_k_koniec[1])/2
        self.rura_k = Rura([p_k_start, (p_k_start[0], mid_y),(p_k_koniec[0], mid_y), p_k_koniec], kolor_farby= "#000000")

        p_w_start = self.z_w.punkt_dol_srodek()
        p_w_koniec = self.mikser.punkt_gora_srodek()
        mid_y = (p_w_start[1]+p_w_koniec[1])/2
        self.rura_w = Rura([p_w_start, (p_w_start[0], mid_y),(p_w_koniec[0], mid_y), p_w_koniec], kolor_farby= "#FFFFFF")

        p_sp_start = self.mikser.punkt_dol_srodek()
        p_sp_koniec = (p_sp_start[0], p_sp_start[1]+220)
        self.rura_spustowa = Rura([p_sp_start, p_sp_koniec], kolor_farby= "")

        self.rury = {'C': self.rura_c, 'M' : self.rura_m, 'Y': self.rura_y, 'K': self.rura_k, "W": self.rura_w, "WYLEW": self.rura_spustowa}

        #Definicja zaworow
        self.zawor_c = Zawor(100, 250)
        self.zawor_m = Zawor(300, 250)
        self.zawor_y = Zawor(500, 250)
        self.zawor_k = Zawor(700, 250)
        self.zawor_w = Zawor(950, 250)
        self.zawor_spustowy = Zawor(550, 650)

        self.zawory = {'C': self.zawor_c, 'M' : self.zawor_m, 'Y': self.zawor_y, 'K': self.zawor_k, 'W': self.zawor_w, "WYLEW": self.zawor_spustowy}

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        for r in self.rury.values() : r.draw(p)
        for zb in self.zbiorniki.values() : zb.draw(p)
        for zaw in self.zawory.values() : zaw.draw(p)

        self.mikser.draw(p)
        self.zawor_c.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = AplikacjaSCADA()
    okno.show()
    sys.exit(app.exec())
