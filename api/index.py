from fastapi import FastAPI
from mfrc522 import SimpleMFRC522
from multiprocessing import Process
from multiprocessing import Manager

rfid = SimpleMFRC522()
manager = Manager()

class Scanner:
    def __init__(self, cards_to_read: int = 5):
        self.rfids = manager.list()
        self.cards_to_read = cards_to_read

    def read_cards(self):
        print("here")
        while len(self.rfids) < self.cards_to_read and self.cards_to_read > 0:
            id, text = rfid.read()
            if not id in self.rfids:
                self.rfids.append(id)
                print(self.rfids)
        self.rfids = manager.list()
        self.read_cards()

    def get_card_codes(self):
        return list(self.rfids)

    def set_cards(self, cards: int = 0):
        self.cards_to_read = cards
        self.rfids = manager.list()

scanner = Scanner()
Process(target=scanner.read_cards).start()

app = FastAPI()

@app.get("/api/cards")
def get_cards():
    print("#### get_cards", scanner.get_card_codes())
    return {"status": 200, "cards": scanner.get_card_codes() }
