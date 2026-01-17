# System SCADA - Symulator Mieszalni Farb

Projekt zaliczeniowy realizujący wizualizację i sterowanie procesem mieszalni farb w języku Python. Aplikacja symuluje działanie systemu SCADA, komunikując się z wirtualnym sterownikiem PLC poprzez Modbus.

## Opis projektu

Aplikacja umożliwia użytkownikowi zdefiniowanie koloru docelowego w formacie HEX. System automatycznie przelicza proporcje składowych (CMYK + biała baza), dozuje odpowiednie ilości farb do zbiornika głównego, miesza je i umożliwia zrzut gotowego produktu. Cały proces wizualizowany jest za pomocą animacji poziomu cieczy, przepływu w rurach oraz pracy urządzeń wykonawczych (zawory, mieszadło).

## Wykorzystane biblioteki

Projekt został napisany w języku Python w wersji 3.13. Wykorzystane biblioteki:
* **PyQt5** - Interfejs graficzny i obsługa zdarzeń.
* **pymodbus** - Obsługa komunikacji sieciowej Modbus TCP.
* **asyncio** - Obsługa symulatora PLC.

## Uruchomienie programu

Przed uruchomieniem programu należy upewić się, że pobrane zostały wymagane biblioteki (**PyQt5**, **pymodbus**, **asyncio**). Następnie należy uruchomić plik symulacja_PLC.py. Po otrzymaniu komunikatu --- PLC START --- można uruchomić aplikację SCADA (plik SCADAPython.py).

# Instrukcja obsługi

## 1. Start procesu:
* W polu tekstowym wpisz kod koloru w formacie HEX.
* Naciśnij przycisk **START**
* System sprawdzi dostępność składników i (jeśli to możliwe) rozpocznie dozowanie.

## 2. Monitoring:
* Obserwuj animację przepływu i zmiany poziomów w zbiornikach.
* Kliknij przycisk **DZIENNIK POWIADOMIEN** aby otworzyć okno z historią operacji i ewentualnymi błędami.

## Obsługa błędów i uzupełnianie:
* Jeżeli zabraknie farby, proces nie wystartuje a w dzienniku pojawi się alarm. Pojawienie się alarmu automatycznie wyświetli dziennik użytkownikowi.
* Kliknij przycisk **UZUPELNIJ**, aby otworzyć panel umożliwiający uzupełnianie lub opróżnianie zbiorników źródłowych. Przycisk ten jest aktywny tylko wtedy, gdy program oczekuje na podanie kodu HEX, więc otworzenie tego panelu w trakcie procesu mieszania jest niemożliwe.


## Autor

Karol Brzostek,
numer albumu: 203970
Automatyka, Robotyka i Systemy Sterowania, semestr 3
Wydział Automatyki i Elektrotechniki Politechniki Gdańskiej
