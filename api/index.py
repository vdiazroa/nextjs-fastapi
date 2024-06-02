from fastapi import FastAPI
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

rfid= SimpleMFRC522()
channel = 17

def relay_on(pin):
    GPIO.output(pin,GPIO.HIGH)

def relay_off(pin):
    GPIO.output(pin,GPIO.LOW)

rfids = []
card_codes = []
cards_to_read = 0

def read_cards():
    while len(rfids) < cards_to_read and cards_to_read > 0:
        id, text = rfid.read()
        if not id in rfids:
            rfids.append(id)
            print("text", text)
            card_codes.append(text)
            print(card_codes)
            time.sleep(.1)

def set_cards(cards: int = 0):
    rfids = []
    card_codes = []
    cards_to_read = cards

app = FastAPI()

@app.get("/api/cards/start")
def start_reading(cards: int = 5):
    read_cards(cards)
    return {"status": 200}


@app.get("/api/cards/stop")
def stop_reading():
    set_cards()
    return {"status": 200}

@app.get("/api/cards")
def get_cards():
    return {"status": 200, "cards": card_codes, "reading": len(card_codes) < cards_to_read }


