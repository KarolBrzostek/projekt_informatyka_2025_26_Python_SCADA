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
        self.czy_plynie = plynie
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

    def uzupenlnij_zbiornik(self):
        self.aktualna_ilosc = self.pojemnosc
        self.aktualizuj_poziom()

    def ustaw_kolor(self, kolor):
        self.kolor_farby = QColor(kolor)

    def draw(self, painter):

        rect = QRectF(self.x, self.y, self.width, self.height)
        gradient_tlo = QLinearGradient(rect.topLeft(), rect.topRight())
        gradient_tlo.setColorAt(0, QColor("#DDDDDD"))
        gradient_tlo.setColorAt(0.5, QColor("#FFFFFF"))
        gradient_tlo.setColorAt(1, QColor("#DDDDDD"))

        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(gradient_tlo)
        painter.drawRect(rect)

        if self.poziom>0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height - h_cieczy
            rect_ciecz = QRectF(self.x+1, y_start, self.width-2, h_cieczy)

            gradient_ciecz = QLinearGradient(rect_ciecz.topLeft(), rect_ciecz.topRight())
            baza = self.kolor_farby
            gradient_ciecz.setColorAt(0, baza.darker(130))
            gradient_ciecz.setColorAt(0.5, baza)
            gradient_ciecz.setColorAt(1, baza.darker(130))

            painter.setPen(Qt.NoPen)
            painter.setBrush(gradient_ciecz)
            painter.drawRect(rect_ciecz)
        

        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect)

        painter.setPen(Qt.black)
        painter.drawText(int(self.x), int(self.y-10), self.nazwa)

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
        painter.drawText(rect, Qt.AlignCenter, f"{procent}")


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
        painter.translate(self.x, self.y)
        painter.rotate(self.kat)

        painter.setPen(QPen(Qt.black, 4))
        painter.drawLine(-25, 0, 25, 0)
        painter.drawLine(0, -25, 0, 25)
        painter.restore()
    

class AplikacjaSCADA(QWidget):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("Mieszalnia farb")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("background-color: #F0F0F0")

        #Definicja zbiornikow
        self.z_c = Zbiornik(50, 50, kolor_farby = "#00FFFF", nazwa="CYAN")
        self.z_c.aktualna_ilosc = 50.0
        self.z_c.aktualizuj_poziom()

        self.z_m = Zbiornik(250, 50, kolor_farby = "#FF00FF", nazwa= "MAGENTA")
        self.z_m.aktualna_ilosc = 50.0
        self.z_m.aktualizuj_poziom()

        self.z_y = Zbiornik(450, 50, kolor_farby = "#FFFF00", nazwa= "YELLOW")
        self.z_y.aktualna_ilosc = 50.0
        self.z_y.aktualizuj_poziom()

        self.z_k = Zbiornik(650, 50, kolor_farby = "#000000", nazwa= "BLACK")
        self.z_k.aktualna_ilosc = 50.0
        self.z_k.aktualizuj_poziom()

        self.z_w = Zbiornik(850, 50, width=200, poj=400, kolor_farby= "#FFFFFF", nazwa= "WHITE")
        self.z_w.aktualna_ilosc=200.0
        self.z_w.aktualizuj_poziom()

        self.mikser = Zbiornik(400, 450, kolor_farby= "FFFFFF", width=200, height=140, nazwa = "MIESZALNIK", poj=200)

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
        self.zawor_spustowy = Zawor(500, 650)

        self.zawory = {'C': self.zawor_c, 'M' : self.zawor_m, 'Y': self.zawor_y, 'K': self.zawor_k, 'W': self.zawor_w, "WYLEW": self.zawor_spustowy}

        self.mieszadlo = Mieszadlo(500, 520)

        #Panel sterowania
        self.panel = QFrame(self)
        self.panel.setGeometry(1100, 0, 299, 799)
        self.panel.setStyleSheet("background-color: #D0D0D0; border: 1px solid #A0A0A0;")

        self.kolor_info = QLabel("Podaj kolor HEX:", self.panel)
        self.kolor_info.move(20,20)

        self.hex_wejsciowy = QLineEdit("#", self.panel)
        self.hex_wejsciowy.setGeometry(20, 40, 250, 30)

        self.przycisk_start = QPushButton("START", self.panel)
        self.przycisk_start.setGeometry(20, 90, 250, 50)
        self.przycisk_start.setStyleSheet("background-color: green; color: white; font-size:15px; font-weight: bold;")
        self.przycisk_start.clicked.connect(self.start_proces)

        self.status = QLabel("Status: OCZEKIWANIE", self.panel)
        self.status.setGeometry(20, 160, 250, 50)
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("font-weight: bold; font-size: 12px;")

        self.proporcje_kolorow = QLabel("", self.panel)
        self.proporcje_kolorow.setGeometry(20, 230, 250, 80)
        # self.proporcje_kolorow.setAlignment(Qt.AlignCenter)
        self.proporcje_kolorow.setStyleSheet("font-size: 10px;")

        self.przycisk_uzupelnij = QPushButton("UZUPELNIJ", self.panel)
        self.przycisk_uzupelnij.setGeometry(20, 660 , 250, 50)
        self.przycisk_uzupelnij.setStyleSheet("background-color: green; color: white; font-size:15px; font-weight: bold;")
        self.przycisk_uzupelnij.clicked.connect(self.uzupelnij_farby)

        self.przycisk_rozlej = QPushButton("ROZLEJ", self.panel)
        self.przycisk_rozlej.setGeometry(20, 730, 250, 50 )
        self.przycisk_rozlej.setStyleSheet("background-color: grey; color: black; font-size: 15px; font-weight: bold;")
        self.przycisk_rozlej.clicked.connect(self.rozpocznij_wylewanie)

        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_symulacji)

        self.stan = "OCZEKIWANIE"
        self.cel_skladniki = {}
        self.skladniki_dodane = {}
        self.licznik_czasu = 0
        self.kolor_koncowy = QColor(0, 0, 0)

        self.indeks_skladnika = 0
        self.kolejnosc = ['C', 'M', 'Y', 'K', 'W']

    def hex_na_cmyk(self, kod_hex):
        try:
            h = kod_hex.lstrip('#')
            if len(h) != 6: return None
            r = int(h[0:2], 16)/255.0
            g = int(h[2:4], 16)/255.0
            b = int(h[4:6], 16)/255.0
        except ValueError:
            return None

        k = 1 - max(r, g, b)
        if k == 1: return 0,0,0,1
        c = (1-r-k)/(1 - k)
        m = (1-g-k)/(1-k)
        y = (1-b-k)/(1-k)
        return c, m, y, k

    def start_proces(self):
        if self.stan != "OCZEKIWANIE": return

        kod = self.hex_wejsciowy.text()
        wynik = self.hex_na_cmyk(kod)

        if wynik is None:
            self.status.setText("Blad! Zly kod HEX!")
            return

        c, m, y, k = wynik
        calkowita_objetosc = 200.0

        pigment_max = 20.0
        ilosc_c = c*pigment_max
        ilosc_m = m*pigment_max
        ilosc_y = y*pigment_max
        ilosc_k = k*pigment_max

        suma_pigmentow = ilosc_c + ilosc_m + ilosc_y + ilosc_k
        ilosc_w = calkowita_objetosc - suma_pigmentow

        if ilosc_w < 0: ilosc_w = 0

        self.cel_skladniki = {'C': ilosc_c, 'M' : ilosc_m, 'Y': ilosc_y, 'K': ilosc_k, 'W': ilosc_w}
        self.skladniki_dodane = {'C': 0, 'M': 0, 'Y': 0, 'K': 0, 'W': 0}

        self.mikser.aktualna_ilosc = 0
        self.mikser.aktualizuj_poziom()
        self.mikser.ustaw_kolor(QColor(255, 255, 255))
        self.kolor_koncowy = QColor(f"#{kod.lstrip('#')}")

        ilosc_farb = (f"C: {ilosc_c:.1f}\n"
                      f"M: {ilosc_m:.1f}\n"
                      f"Y: {ilosc_y:.1f}\n"
                      f"K: {ilosc_k:.1f}\n"
                      f"W: {ilosc_w:.1f}"
                      )
        self.proporcje_kolorow.setText(ilosc_farb)

        self.stan = "DOZOWANIE"
        self.status.setText("Status: DOZOWANIE")
        self.timer.start(50)

    def rozpocznij_wylewanie(self):
        if self.stan == "WYMIESZANO":
            self.stan = "ROZLEWANIE"
            self.status.setText("Status: ROZLEWANIE")

    def logika_symulacji(self):
        if self.stan == "DOZOWANIE":
            self.przycisk_start.setStyleSheet("background-color: grey; color: black; font-size: 15px; font-weight: bold;")
            if self.indeks_skladnika >= len(self.kolejnosc):
                self.stan = "MIESZANIE"
                self.licznik_czasu = 0
                self.status.setText("MIESZANIE")
                return

            klucz = self.kolejnosc[self.indeks_skladnika]
            cel = self.cel_skladniki[klucz]
            obecnie = self.skladniki_dodane[klucz]
            predkosc = 1.0

            if obecnie < cel:
                ilosc = min(predkosc, cel - obecnie)
                pobrane = self.zbiorniki[klucz].usun_ciecz(ilosc)

                if pobrane > 0:
                    self.skladniki_dodane[klucz] += pobrane
                    self.mikser.dodaj_ciecz(pobrane)

                    self.zawory[klucz].ustaw_stan(True)
                    self.rury[klucz].ustaw_przeplyw(True, self.zbiorniki[klucz].kolor_farby)
                    self.status.setText(f"Status: DOZOWANIE SKLADNIKA {klucz}")
                    self.update()
                else:
                    self.zawory[klucz].ustaw_stan(False)
                    self.rury[klucz].ustaw_przeplyw(False)
                    self.indeks_skladnika += 1
            else:
                self.zawory[klucz].ustaw_stan(False)
                self.rury[klucz].ustaw_przeplyw(False)

                self.indeks_skladnika += 1
            
        elif self.stan == "MIESZANIE":
            self.licznik_czasu += 1
            self.mieszadlo.aktywne = True
            self.mieszadlo.aktualizuj()

            if self.licznik_czasu > 20:
                self.mikser.ustaw_kolor(self.kolor_koncowy)

            if self.licznik_czasu > 60:
                self.stan = "WYMIESZANO"
                self.status.setText("Status: WYMIESZANO")
                self.przycisk_rozlej.setStyleSheet("background-color: green; color: white; font-size: 15px; font-weight: bold;")
                self.mieszadlo.aktywne = False

        elif self.stan == "ROZLEWANIE":
            predkosc_wylewania = 2.0
            usunieto = self.mikser.usun_ciecz(predkosc_wylewania)

            if usunieto > 0:
                self.zawor_spustowy.ustaw_stan(True)
                self.rura_spustowa.ustaw_przeplyw(True, self.mikser.kolor_farby)
            else:
                self.zawor_spustowy.ustaw_stan(False)
                self.rura_spustowa.ustaw_przeplyw(False)
                self.stan = "OCZEKIWANIE"
                self.status.setText("Status: ZAKONCZONO")
                self.przycisk_start.setStyleSheet("background-color: green; color: white; font-size: 15px; font-weight: bold;")
                self.przycisk_rozlej.setStyleSheet("background-color: grey; color: black; font-size: 15px; font-weight: bold;")
                self.hex_wejsciowy.setText("#")
                self.timer.stop()

                self.indeks_skladnika = 0

        self.update()


    def uzupelnij_farby(self):
        if self.stan == "OCZEKIWANIE" or self.stan == "ZAKONCZONO":
            for zb in self.zbiorniki.values(): zb.uzupenlnij_zbiornik()
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        for r in self.rury.values() :
            if not r.czy_plynie:
                r.draw(p)

        for r in self.rury.values():
            if r.czy_plynie:
                r.draw(p)

        for zb in self.zbiorniki.values() : zb.draw(p)
        for zaw in self.zawory.values() : zaw.draw(p)

        self.mikser.draw(p)
        self.mieszadlo.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = AplikacjaSCADA()
    okno.show()
    sys.exit(app.exec())
