from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String(50), nullable=False)
    steam_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Game {self.name}>'
