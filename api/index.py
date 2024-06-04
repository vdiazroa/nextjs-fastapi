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
    def __init__(self, cards_to_read: int = 5):
        self.rfids = []
        self.cards_to_read = cards_to_read
    
    def read_cards(self):
        while len(self.rfids) <= self.cards_to_read and self.cards_to_read > 0:
            id, text = rfid.read()
            if not str(id) in self.rfids:
                self.rfids.append(str(id))
                print(self.rfids)
        self.read_cards()

    def get_card_codes(self):
        return self.rfids
    
    def set_cards(self, cards: int = 0):
        self.cards_to_read = cards
        self.rfids = []

scanner = Scanner()

app = FastAPI()

@app.get("/api/cards")
def get_cards():
    print("#### get_cards", scanner.get_card_codes())
    return {"status": 200, "cards": scanner.get_card_codes() }

@app.get("/api/cards/start")
def start_reading():
    scanner.set_cards(5)
    return {"status": 200}


@app.get("/api/cards/stop")
def stop_reading():
    scanner.set_cards()
    return {"status": 200}

scanner.read_cards()


