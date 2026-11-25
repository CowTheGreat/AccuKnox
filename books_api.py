import argparse
import json
import sqlite3
from contextlib import closing
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description="Fetch books, save them in SQLite, and show the catalog.")
    parser.add_argument("url", help="API URL returning a JSON array of books")
    parser.add_argument("--db", default="books.sqlite3")
    args = parser.parse_args()

    with urlopen(args.url, timeout=10) as response:
        books = json.load(response)

    rows = []
    for book in books:
        title = book["title"].strip()
        author = book["author"].strip()
        year = book["publication_year"]
        if not title or not author or type(year) is not int:
            raise ValueError("Each book needs a title, an author, and an integer publication year.")
        rows.append((title, author, year))

    with closing(sqlite3.connect(args.db)) as db:
        with db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER NOT NULL,
                    PRIMARY KEY (title, author, publication_year)
                )
            """)
            db.executemany("""
                INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)
                ON CONFLICT (title, author, publication_year) DO NOTHING
            """, rows)

        for title, author, year in db.execute("""
            SELECT title, author, publication_year
            FROM books ORDER BY title, author, publication_year
        """):
            print(f"{title} | {author} | {year}")


if __name__ == "__main__":
    main()
