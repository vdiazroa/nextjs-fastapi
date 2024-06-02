from fastapi import FastAPI
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

rfid = SimpleMFRC522()
channel = 17

def relay_on(pin):
    GPIO.output(pin,GPIO.HIGH)

def relay_off(pin):
    GPIO.output(pin,GPIO.LOW)

class Scanner:
    def __init__(self):
        self.rfids = []
        self.card_codes = []
        self.cards_to_read = 0

    def read_cards(self):
        print("### len(rfids)", len(self.rfids))
        print("### cards_to_read", self.cards_to_read)
        print("### <", len(self.rfids) < self.cards_to_read)
        print("### >", self.cards_to_read > 0)
        while len(self.rfids) < self.cards_to_read and self.cards_to_read > 0:
            print("### 1")
            id, text = rfid.read()
            print("### id",id,text)
            if not id in self.rfids:
                print("### 2")
                self.rfids.append(id)
                print("text", text)
                self.card_codes.append(text)
                print(self.card_codes)
                time.sleep(.1)

    def set_cards(self, cards: int = 0):
        print("### cards", cards)
        self.rfids = []
        self.card_codes = []
        self.cards_to_read = cards


    def get_card_codes(self):
        return self.card_codes

    def get_reading(self):
        return len(self.card_codes) < self.cards_to_read


scanner = Scanner()

app = FastAPI()

@app.get("/api/cards/start")
def start_reading():
    print("### start_reading")
    scanner.set_cards(5)
    print("### read_cards")
    scanner.read_cards()
    print("### read_cards 2")

    return {"status": 200}


@app.get("/api/cards/stop")
def stop_reading():
    scanner.set_cards()
    return {"status": 200}

@app.get("/api/cards")
def get_cards():
    print("#### get_cards 0")
    print("#### get_cards 1",scanner.get_card_codes())
    print("#### get_cards 2",scanner.get_reading())
    return {"status": 200, "cards": scanner.get_card_codes(), "reading": scanner.get_reading() }


