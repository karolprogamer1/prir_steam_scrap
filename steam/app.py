# app.py

from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Utwórz tabelę w bazie danych na podstawie definicji modelu
with app.app_context():
    db.create_all()

# Funkcja do pobierania danych o grach ze Steam
def fetch_steam_games(search_query):
    url = f'https://store.steampowered.com/search/?term={search_query}&category1=998'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []

    for game in soup.find_all('a', class_='search_result_row'):
        name_elem = game.find('span', class_='title')
        if name_elem:
            name = name_elem.get_text().strip()
        else:
            name = 'No name available'

        price_elem = game.find('div', class_='search_price_discount_combined')
        if price_elem:
            price_text = price_elem.get_text().strip()
            if 'Free' in price_text:
                price = 'Free'
            else:
                price = price_text
        else:
            price = 'No price available'

        release_date_elem = game.find('div', class_='search_released')
        if release_date_elem:
            release_date = release_date_elem.get_text().strip()
        else:
            release_date = 'No release date available'

        steam_url = game.get('href', '#')

        games.append({
            'name': name,
            'price': price,
            'release_date': release_date,
            'steam_url': steam_url
        })

    # Zapisz do bazy danych
    save_to_database(games)

    return games

def save_to_database(games):
    with app.app_context():
        for game in games:
            db_game = Game(
                name=game['name'],
                price=game['price'],
                release_date=game['release_date'],
                steam_url=game['steam_url']
            )
            db.session.add(db_game)

        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search_query', '')

    if search_query:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(fetch_steam_games, search_query)
            steam_games = future.result()
    else:
        steam_games = []

    return render_template('index.html', steam_games=steam_games, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
