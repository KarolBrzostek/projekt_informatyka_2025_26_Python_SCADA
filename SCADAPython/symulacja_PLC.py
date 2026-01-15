import asyncio
import logging
import sys
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

class BlokPamieci(ModbusSequentialDataBlock):
    def __init__(self, adres, wartosci):
        super().__init__(adres, wartosci)
        self.etykiety = ["CYAN", 'MAGENTA', "YELLOW", "BLACK", "WHITE", "ROZLEW", "MIESZADLO"]

    def setValues(self, adres, wartosci):
        if adres > 0:
            adres_poprawiony = adres - 1
        else:
            adres_poprawiony = adres

        super().setValues(adres_poprawiony, wartosci)

        self.pokaz_stan()

    def pokaz_stan(self):
        try:
            aktualne_dane = self.getValues(0, 7)
        except ValueError:
            aktualne_dane = [0]*7

        elementy_linii = []

        for i, val in enumerate(aktualne_dane):
            if i < len(self.etykiety):
                nazwa = self.etykiety[i]
                if val:
                    stan = "[ON]"
                else:
                    stan = "[  ]"
                elementy_linii.append(f"{nazwa}:{stan}")

        print("  |  ".join(elementy_linii))

class SymulacjaPLC:
    def __init__(self, port = 5020):
        self.host = "localhost"
        self.port = port

        self.store = ModbusDeviceContext(
            co = BlokPamieci(0, [0]*100)
        )

        self.context = ModbusServerContext(devices = self.store, single = True)

    async def uruchom_serwer(self):
        print(f"--- PLC START ({self.host}:{self.port}) ---")
        adres = (self.host, self.port)
        await StartAsyncTcpServer(context = self.context, address = adres)

if __name__ == "__main__":
    try:
        if asyncio.get_event_loop_policy().__class__.__name__ == "WindowsProactorEventLoopPolicy":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        plc = SymulacjaPLC()
        asyncio.run(plc.uruchom_serwer())
    except KeyboardInterrupt:
        print("\n Zatrzymano serwer PLC.")