import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

rfid = SimpleMFRC522()
channel = 17

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
                f = open("cards.txt", "w")
                f.write('\n'.join(self.card_codes))
                f.close()
                time.sleep(.1)

    def set_cards(self, cards: int = 0):
        print("### cards", cards)
        self.rfids = []
        self.card_codes = []
        self.cards_to_read = cards


    def get_card_codes(self):
        return self.card_codes

scanner = Scanner()
scanner.set_cards(5)
scanner.read_cards()