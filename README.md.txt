# 🎌 Kurokana Tapes

> A spaced-repetition Japanese language learning web application.

## 📖 Overview
Kurokana Tapes is a full-stack web application designed to help users master Japanese Kana and JLPT N5 vocabulary. Built with Flask, it features a custom spaced-repetition algorithm that dynamically weights flashcards based on user performance, ensuring weaker areas are tested more frequently.

## ✨ Features
* **Spaced-Repetition Logic**: Automatically tracks incorrect answers and dynamically increases their frequency in the quiz queue.
* **Flashcard Management**: Users can add new vocabulary, view their entire deck, and track error counts.
* **Stateless Web Architecture**: Built on a fully routed web server capable of handling standard HTTP methods (GET/POST).

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, Jinja2 Templating
* **Data Storage:** JSON (Planning migration to SQLite)

## 🚀 How to Run Locally

1. Clone the repository:
    git clone https://github.com/salmanfarismk/SigmaJP
    cd SigmaJP

2. Install the required dependencies:
    pip install flask

3. Start the server:
    python app.py

4. Open your browser and navigate to `http://127.0.0.1:5000`

## 🧠 Key Learnings
* Architecting RESTful routes to handle web traffic and form submissions.
* Injecting dynamic Python logic into static HTML pages using Jinja2 templates.
* Managing application state and file I/O within a stateless web framework.