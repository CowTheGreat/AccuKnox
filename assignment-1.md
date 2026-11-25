# Assignment 1

## 1. Fetch books from an API and store them in SQLite

[Python script](books_api.py) · [Sample books](assets/books.json)

I assume the API returns a JSON array with `title`, `author`, and an integer `publication_year`. The script saves the books in SQLite and prints the saved catalog in the terminal. An identical title, author, and year counts as the same record on repeat runs.

## 2. Fetch student scores and generate a bar chart

[Python script](student_scores.py) · [Sample scores](assets/student_scores.json)

I assume the API returns one entry per student with a `name` and a numeric `score` from 0 to 100. The script prints the arithmetic mean and saves a bar chart as a PNG. The sample data has an average of 84.

## 3. Import users from CSV into SQLite

[Python script](import_users.py) · [Sample CSV](assets/users.csv)

The script expects a UTF-8 CSV with `name` and `email` columns. It trims and lowercases email addresses. If an email appears more than once, it keeps the name from the last row.

## 4. Most complex Python code

[Whisper audio recorder and transcriber](https://github.com/CowTheGreat/Real-Time-Audio-Recorder-and-Transcriber-using-Whisper-AI)

## 5. Most complex database code

[EQPMS database sample](assets/DB%20Code.txt) · [EQPMS repository](https://github.com/CowTheGreat/EQPMS)

## Run the scripts

From the project folder, use Python 3.10 or newer and install Matplotlib for the scores script.

```powershell
python -m pip install matplotlib
```

Start a local server to serve the sample JSON files.

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory assets
```

Open another terminal in the project folder and run the scripts.

```powershell
python books_api.py http://127.0.0.1:8000/books.json
python student_scores.py http://127.0.0.1:8000/student_scores.json
python import_users.py assets/users.csv
```

The API scripts also accept external REST API URLs if the responses match the fields above.
