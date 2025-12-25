from models.album import Album, db

class AlbumRepo:
    def all(self, genre=None, sort_year=None):
        query = Album.query
        if genre:
            query = query.filter_by(genre=genre)
        if sort_year:
            query = query.order_by(Album.year.desc())
        return query.all()

    def add(self, artist, title, genre, year, rating):
        album = Album(
            artist=artist,
            title=title,
            genre=genre,
            year=year,
            rating=rating
        )
        db.session.add(album)
        db.session.commit()
        return album

    def delete(self, album_id):
        album = Album.query.get(album_id)
        if album:
            db.session.delete(album)
            db.session.commit()

    def update(self, album_id, **kwargs):
        album = Album.query.get(album_id)
        if album:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(album, key, value)
            db.session.commit()
