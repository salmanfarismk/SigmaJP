import random 
import json

class FlashCard:
    def __init__(self, japanese, reading, meaning):
        self.japanese = japanese
        self.reading = reading
        self.meaning = meaning
        self.wrongcount = 0
        
class FlashCardDeck:
    def __init__(self):
        self.cards = []
        
    def add_card(self, japanese, reading, meaning):
        card = FlashCard(japanese, reading, meaning)
        self.cards.append(card)
        print(f"Added: {japanese} ({reading}) - {meaning}")
    
    def quiz(self):
        if not self.cards:
            print("Deck is empty!")
            return
        
        score = 0
        total = 0
        
        while True:
            weights = [1 + c.wrongcount for c in self.cards]
            card = random.choices(self.cards, weights=weights, k=1)[0]
            print(f"\nWhat is the meaning of: {card.japanese}")
            answer = input("Your answer :")
            if answer.lower() == "quit":
                print(f"\nSession over. You got {score} out of {total} correct!")
                break
            total += 1
            if answer.lower().strip() == card.meaning.lower().strip():
                print("Correct answer!")
                score += 1
            else:
                print("Wrong Answer.")
                card.wrongcount += 1
            print(f"Reading: {card.reading} | Meaning: {card.meaning}")
            
    
    def save(self, filename="deck.json"):
        data = [{"japanese": c.japanese, "reading": c.reading, "meaning": c.meaning,"wrongcount": c.wrongcount}for c in self.cards]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.cards)} cards.")
        
    def load(self, filename="deck.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.cards = [FlashCard(d["japanese"], d["reading"], d["meaning"]) for d in data]
            for i, card in enumerate(self.cards):
                card.wrongcount = data[i].get("wrongcount", 0)
            print(f"Loaded {len(self.cards)} cards")
        except FileNotFoundError:
            print("No saved deck found.")
            
    def show_cards(self):
        if not self.cards:
            print("Deck is empty.")
        else:
            print(f"---- Your Deck ({len(self.cards)} cards) ----")
            for i, card in enumerate(self.cards, 1):
                print(f"{i}. {card.japanese} ({card.reading}) - {card.meaning}")

        
def main():
    deck = FlashCardDeck()
    deck.load()
    
    while True:
        print("\n---- Japanese FlashCards ----")
        print("1. Add Cards")
        print("2. Quiz")
        print("3. Show Cards")
        print("4. Save and Exit")
        choice = input("Choice :")
        
        if choice == "1":
            j = input("Japanese :")
            r = input("Reading :")
            m = input("Meaning :")
            deck.add_card(j,r,m)
        elif choice == "2":
            deck.quiz()
        elif choice == "3":
            deck.show_cards()
        elif choice == "4":
            deck.save()
            break
        else:
            print("Invalid Input")
            
main()
        