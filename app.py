from flask import Flask, render_template, request, redirect, url_for
import json
import random
import sqlite3

app = Flask(__name__)
DECK_FILE = "deck.json"

def get_db():
    conn = sqlite3.connect('sigmajp.db')
    conn.row_factory = sqlite3.Row
    return conn 
    
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            japanese TEXT NOT NULL,
            reading TEXT NOT NULL,
            meaning TEXT NOT NULL,
            wrongcount INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def load_deck():
    conn = get_db()
    cards = conn.execute('SELECT * FROM cards').fetchall()
    conn.close()
    return [dict(card) for card in cards]

def add_card(japanese, reading, meaning):
    conn = get_db()
    conn.execute('INSERT INTO cards (japanese, reading, meaning) VALUES (? ,? ,?)', (japanese, reading, meaning))
    conn.commit()
    conn.close()

def update_wrongcount(japanese, correct):
    conn = get_db()
    if correct:
        conn.execute('UPDATE cards SET wrongcount = MAX(0, wrongcount - 1) WHERE japanese = ?', (japanese,))
    else:
        conn.execute('UPDATE cards SET wrongcount = wrongcount + 1 WHERE japanese =?', (japanese,))
    conn.commit()
    conn.close()


@app.route("/")
def index():
    deck = load_deck()
    return render_template("index.html", card_count=len(deck))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        add_card(
            request.form["japanese"],
            request.form["reading"],
            request.form["meaning"]
        )
        return redirect(url_for("index"))
    return render_template("index.html", card=len(load_deck()))

        

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

    action = request.form.get("action", "submit")
    
    if action == "flip":
        correct = False
        gave_up = True
    else:
        user_answer = request.form.get("answer", "").lower().strip()
        correct = user_answer == meaning.lower().strip()
        gave_up = False

    update_wrongcount(japanese, correct)
        
    return render_template("quiz.html",
                           card = {"japanese": japanese, "reading": reading, "meaning": meaning, },
                           result = correct,
                           show_result=True,
                           gave_up = gave_up)    
    
    
if __name__ == "__main__":
    init_db()
    app.run(debug=True)    