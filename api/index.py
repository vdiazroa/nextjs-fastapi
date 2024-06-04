from fastapi import FastAPI
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from multiprocessing import Process
from multiprocessing import Manager

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

rfid = SimpleMFRC522()
channel = 17

manager = Manager()

class Scanner:
    def __init__(self, cards_to_read: int = 5):
        self.rfids = manager.list()
        self.cards_to_read = cards_to_read

    def read_cards(self):
        print("here")
        while len(self.rfids) <= self.cards_to_read and self.cards_to_read > 0:
            id, text = rfid.read()
            if not id in self.rfids:
                self.rfids.append(id)
                print(self.rfids)
        self.rfids = []
        self.read_cards()

    def get_card_codes(self):
        return list(self.rfids)

    def set_cards(self, cards: int = 0):
        self.cards_to_read = cards
        self.rfids = []

scanner = Scanner()
#scanner.read_cards()
p1=Process(target=scanner.read_cards)
p1.start()
#loop = asyncio.get_event_loop()
#task = loop.run_until_complete(loop.create_task(scanner.read_cards()))

#t = threading.Thread(target=scanner.read_cards, args=())

#t.start()

app = FastAPI()

@app.get("/api/cards")
def get_cards():
    print("#### get_cards", scanner.get_card_codes())
    return {"status": 200, "cards": scanner.get_card_codes() }



#p1=Process(target=scanner.read_cards)
#p1.start()

#p2=Process(target=start_api)
#p2.start()

#p1.join()
#p2.join()
#print("started!!")
#@app.get("/api/cards/start")
#def start_reading():
#    scanner.set_cards(5)
#    return {"status": 200}

#@app.get("/api/cards/stop")
#def stop_reading():
#    scanner.set_cards()
#    return {"status": 200}

