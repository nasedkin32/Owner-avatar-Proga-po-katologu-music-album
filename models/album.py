from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Album {self.artist} - {self.title}>"
