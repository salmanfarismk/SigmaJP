import sqlite3
import re

def init_db(conn):
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

conn = sqlite3.connect('sigmajp.db')
init_db(conn)
conn.execute('DELETE FROM cards')

count = 0
with open('anki_export.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        
        parts = line.split('\t')
        if len(parts) < 4:
            continue
        
        col4 = parts[3].strip()
        
        # Extract "word - meaning" pattern from column 4
        # Example: 私[わたし;h]  - I
        match = re.match(r'^([\u3000-\u9fff\u3040-\u309f\u30a0-\u30ff\uff00-\uffef]+(?:\[.*?\])?)\s+-\s+(.+)$', col4)
        
        if not match:
            continue
            
        raw_japanese = match.group(1)
        meaning = match.group(2).strip()
        
        # Extract clean japanese (remove furigana)
        japanese = re.sub(r'\[.*?\]', '', raw_japanese).strip()
        
        # Extract reading from furigana
        reading_match = re.search(r'\[([^;\]]+)', raw_japanese)
        reading = reading_match.group(1).strip() if reading_match else ""
        
        # Skip sentences in meaning
        if len(meaning.split()) > 3 or ',' in meaning:
            continue
            
        if not japanese or not meaning:
            continue
            
        conn.execute(
            'INSERT INTO cards (japanese, reading, meaning) VALUES (?, ?, ?)',
            (japanese, reading, meaning)
        )
        count += 1

conn.commit()
conn.close()
print(f"Imported {count} vocab cards")