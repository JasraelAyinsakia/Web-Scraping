import requests
import selectorlib
import smtplib, ssl
import os
import  time
import sqlite3

"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2024.07.03')"
"SELECT * FROM events WHERE date='2024.09.03'"

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("data.db")

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def  extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "apuseyinejake011@gmail.com"
    password = "caceyrodfsxwsvap"

    receiver = "apuseyinejake011@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
    connection.commit()


def read(extracted):
    # Handle empty or None data
    if not extracted or extracted.strip() == "":
        print("No data to process")
        return []

    try:
        row = extracted.split(",")
        row = [item.strip() for item in row]

        # Debug output
        print(f"Processing: '{extracted}'")
        print(f"Split into {len(row)} parts: {row}")

        # Validate we have exactly 3 parts
        if len(row) != 3:
            print(f"WARNING: Expected format 'band, city, date' but got {len(row)} parts")
            return []

        band, city, date = row

        # Validate none of the parts are empty
        if not all([band, city, date]):
            print("WARNING: One or more fields are empty")
            return []

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(f"Error processing data: {e}")
        return []


def store(extracted):
    try:
        row = extracted.split(",")
        row = [item.strip() for item in row]

        if len(row) != 3:
            print(f"Cannot store: Expected 3 values, got {len(row)}")
            return False

        cursor = connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error storing data: {e}")
        return False

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No Upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey, new event was found")
        time.sleep(2)
