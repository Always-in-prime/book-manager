import json
import os

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def add_book(title, author, year):
    # Валидация
    if not title or not author:
        raise ValueError("Название и автор не могут быть пустыми")
    
    try:
        year = int(year)
    except ValueError:
        raise ValueError("Год должен быть числом")

    if year < 0 or year > 2026:
        raise ValueError("Некорректный год издания")

    books = load_books()
    new_book = {
        "title": title.strip(),
        "author": author.strip(),
        "year": year
    }
    books.append(new_book)
    save_books(books)
    return new_book

def filter_books(query):
    books = load_books()
    if not query:
        return books
    
    query_lower = query.lower()
    filtered = [
        b for b in books 
        if query_lower in b["title"].lower() or query_lower in b["author"].lower()
    ]
    return filtered