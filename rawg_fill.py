import requests
import sqlite3

API_KEY = "4192bf9d3b2e4be194a458a00ea03629"
URL = f"https://api.rawg.io/api/games?key={API_KEY}&page_size=40"
response = requests.get(URL)
data = response.json()


def save_game(conn, title, genre, rating, image_url):
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT OR IGNORE INTO games (title, genre, rating, image_url) VALUES (?, ?, ?, ?)''', (title, genre, rating, image_url))
    conn.commit()

conn = sqlite3.connect("app.db")

for page in range(1, 15):
    url = f"{URL}&page={page}"
    response = requests.get(url)
    data = response.json()
    for game in data["results"]:
        title = game['name']
        rating = game['rating']
        genre = game['genres'][0]['name'] if game['genres'] else 'Невідомо'
        image_url = game['background_image']
        save_game(conn, title, genre, rating, image_url)

conn.close()