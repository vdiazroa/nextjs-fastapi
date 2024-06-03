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
        self.cards_to_read = 0

    def read_cards(self):
        while len(self.rfids) <= self.cards_to_read and self.cards_to_read > 0:
            id, text = rfid.read()
            if not str(id) in self.rfids:
                f = open("cards.txt", "w")
                self.rfids.append(str(id))
                print(self.rfids)
                f = open("cards.txt", "w")
                f.write('\n'.join(self.rfids))
                f.close()
                time.sleep(.1)
        self.rfids = []
        self.read_cards()

    def set_cards(self, cards: int = 0):
        self.rfids = []
        self.cards_to_read = cards

    def get_card_codes(self):
        return self.rfids

scanner = Scanner()
scanner.set_cards(5)
scanner.read_cards()