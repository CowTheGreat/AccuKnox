import argparse
import csv
import sqlite3
from contextlib import closing


def main():
    parser = argparse.ArgumentParser(description="Import names and emails from a CSV file into SQLite.")
    parser.add_argument("csv_file")
    parser.add_argument("--db", default="users.sqlite3")
    args = parser.parse_args()

    rows = []
    with open(args.csv_file, encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not {"name", "email"}.issubset(reader.fieldnames or []):
            raise ValueError("The CSV must have name and email columns.")
        for row in reader:
            name = (row["name"] or "").strip()
            email = (row["email"] or "").strip().lower()
            if not name or not email:
                raise ValueError(f"Missing name or email on CSV line {reader.line_num}.")
            rows.append((name, email))

    with closing(sqlite3.connect(args.db)) as db:
        with db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    name TEXT NOT NULL,
                    email TEXT PRIMARY KEY NOT NULL
                )
            """)
            db.executemany("""
                INSERT INTO users (name, email) VALUES (?, ?)
                ON CONFLICT (email) DO UPDATE SET name = excluded.name
            """, rows)
        count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    print(f"Processed {len(rows)} CSV rows. The database contains {count} unique users.")


if __name__ == "__main__":
    main()
