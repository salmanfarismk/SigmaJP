from flask import Flask, render_template, request, redirect, url_for
import json
import random

app = Flask(__name__)
DECK_FILE = "deck.json"

def load_deck():
    try:
        with open(DECK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def save_deck(deck):
    with open(DECK_FILE, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    deck = load_deck()
    return render_template("index.html", card_count=len(deck))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        japanese = request.form["japanese"]
        reading = request.form["reading"]
        meaning = request.form["meaning"]
        deck = load_deck()
        deck.append({"japanese": japanese, "reading": reading, "meaning": meaning, "wrongcount": 0})
        save_deck(deck)
        return redirect(url_for("index"))
    return render_template("index.html", card_count = len(load_deck()))

@app.route("/cards")
def cards():
    deck = load_deck()
    return(render_template("cards.html", cards=deck))

@app.route("/quiz")
def quiz():
    deck = load_deck()
    if not deck:
        return redirect(url_for("index"))
    weights = [1 + c["wrongcount"] for c in deck]
    card = random.choices(deck, weights = weights, k=1)[0]
    return render_template("quiz.html", card=card)

@app.route("/answer", methods=["POST"])
def answer():
    japanese = request.form["japanese"]
    reading = request.form["reading"]
    meaning = request.form["meaning"]
    user_answer = request.form["answer"].lower().strip()
    correct = user_answer == meaning.lower().strip()
    

    deck = load_deck()
    for c in deck:
        if c["japanese"] == japanese:
            if correct:
                c["wrongcount"] = max(0, c["wrongcount"] - 1)
            else:
                c["wrongcount"] += 1
            break
    save_deck(deck)
        
    return render_template("quiz.html",
                           card = {"japanese": japanese, "reading": reading, "meaning": meaning, },
                           result = correct,
                           show_result=True)    
    
    
if __name__ == "__main__":
    app.run(debug=True)    