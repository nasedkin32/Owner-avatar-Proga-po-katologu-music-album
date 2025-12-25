
import sys
import os
import pytest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from run import app
from models.album import db , Album
def test_create_album(client):
    with app.app_context():
        db.session.add(
            Album(
                artist="Metallica",
                title="Black Album",
                genre="Metal",
                year=1991,
                rating=5
            )
        )
        db.session.commit()

    rv = client.get("/albums/")
    assert "Metallica" in rv.data.decode()

import pytest
import run
from models.album import db, Album
from models.user import User, UserRepo
from flask_login import login_user

@pytest.fixture
def client():
    run.app.config["TESTING"] = True
    run.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    run.app.config["LOGIN_DISABLED"] = True

    with run.app.test_client() as client:
        with run.app.app_context():
            db.create_all()
        yield client
        with run.app.app_context():
            db.drop_all()


def test_album_creation():
    album = Album(
        artist="Metallica",
        title="Black Album",
        genre="Metal",
        year=1991,
        rating=5
    )
    assert album.artist == "Metallica"
    assert album.rating == 5


def test_album_without_rating():
    album = Album(
        artist="Pink Floyd",
        title="Animals",
        genre="Rock",
        year=1977
    )
    assert album.rating is None


def test_album_string_representation():
    album = Album(
        artist="Daft Punk",
        title="Discovery",
        genre="Electronic",
        year=2001
    )
    assert "Daft Punk" in repr(album)


def test_album_year_is_integer():
    album = Album(
        artist="Test",
        title="Test",
        genre="Test",
        year=2000
    )
    assert isinstance(album.year, int)


def test_album_genre_not_empty():
    album = Album(
        artist="Test",
        title="Test",
        genre="Rock",
        year=2000
    )
    assert album.genre != ""


def test_album_rating_range_valid():
    album = Album(
        artist="Test",
        title="Test",
        genre="Rock",
        year=2000,
        rating=3
    )
    assert 1 <= album.rating <= 5


def test_album_long_artist_name():
    album = Album(
        artist="A" * 100,
        title="Test",
        genre="Rock",
        year=2000
    )
    assert len(album.artist) == 100


def test_album_title_special_chars():
    album = Album(
        artist="Test",
        title="!@#$%^&*()",
        genre="Rock",
        year=2000
    )
    assert "!@#$" in album.title


def test_add_album_to_db(client):
    with run.app.app_context():
        album = Album(
            artist="Muse",
            title="Origin of Symmetry",
            genre="Rock",
            year=2001,
            rating=5
        )
        db.session.add(album)
        db.session.commit()

        assert Album.query.count() == 1


def test_delete_album_from_db(client):
    with run.app.app_context():
        album = Album(
            artist="Muse",
            title="Absolution",
            genre="Rock",
            year=2003
        )
        db.session.add(album)
        db.session.commit()

        db.session.delete(album)
        db.session.commit()

        assert Album.query.count() == 0


def test_update_album_rating(client):
    with run.app.app_context():
        album = Album(
            artist="Muse",
            title="Drones",
            genre="Rock",
            year=2015
        )
        db.session.add(album)
        db.session.commit()

        album.rating = 4
        db.session.commit()

        updated = Album.query.first()
        assert updated.rating == 4


def test_multiple_albums(client):
    with run.app.app_context():
        db.session.add_all([
            Album(artist="A", title="A", genre="Rock", year=2000),
            Album(artist="B", title="B", genre="Metal", year=2001),
            Album(artist="C", title="C", genre="Jazz", year=2002),
        ])
        db.session.commit()

        assert Album.query.count() == 3


def test_filter_by_genre(client):
    with run.app.app_context():
        db.session.add_all([
            Album(artist="A", title="A", genre="Rock", year=2000),
            Album(artist="B", title="B", genre="Metal", year=2001),
        ])
        db.session.commit()

        rock = Album.query.filter_by(genre="Rock").all()
        assert len(rock) == 1


def test_sort_by_year(client):
    with run.app.app_context():
        db.session.add_all([
            Album(artist="A", title="A", genre="Rock", year=1990),
            Album(artist="B", title="B", genre="Rock", year=2000),
        ])
        db.session.commit()

        albums = Album.query.order_by(Album.year.desc()).all()
        assert albums[0].year == 2000


def test_album_query_by_artist(client):
    with run.app.app_context():
        db.session.add(
            Album(artist="Nirvana", title="Nevermind", genre="Rock", year=1991)
        )
        db.session.commit()

        album = Album.query.filter_by(artist="Nirvana").first()
        assert album is not None


def test_album_not_found(client):
    with run.app.app_context():
        album = Album.query.get(999)
        assert album is None

def test_user_creation(client):
    with run.app.app_context():
        repo = UserRepo()
        user = repo.add("testuser", "password123")
        assert user.username == "testuser"


def test_user_password_hashing(client):
    with run.app.app_context():
        repo = UserRepo()
        user = repo.add("user2", "secret")
        assert user.password_hash != "secret"


def test_user_password_check(client):
    with run.app.app_context():
        repo = UserRepo()
        user = repo.add("user3", "pass")
        assert user.check_password("pass") is True


def test_user_default_role(client):
    with run.app.app_context():
        repo = UserRepo()
        user = repo.add("user4", "pass")
        assert user.role == "user"


def test_admin_role(client):
    with run.app.app_context():
        repo = UserRepo()
        admin = repo.add("admin", "admin", role="admin")
        assert admin.is_admin()



def test_albums_page(client):
    rv = client.get("/albums/")
    assert rv.status_code in [200, 302]


def test_home_page(client):
    rv = client.get("/")
    assert rv.status_code == 200


def test_login_page(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200


def test_register_page(client):
    rv = client.get("/auth/register")
    assert rv.status_code == 200


def test_unauthorized_redirect(client):
    run.app.config["LOGIN_DISABLED"] = False
    rv = client.get("/albums/")
    assert rv.status_code in [302, 401]
