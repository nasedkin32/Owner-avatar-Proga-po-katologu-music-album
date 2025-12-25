from flask import Blueprint, request, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from models.album import Album, db

bp = Blueprint("albums", __name__, url_prefix="/albums")


@bp.route("/", methods=["GET", "POST"])
@login_required
def list_albums():
    if request.method == "POST":
        album = Album(
            artist=request.form["artist"],
            title=request.form["title"],
            genre=request.form["genre"],
            year=int(request.form["year"]),
            rating=request.form.get("rating")
        )
        db.session.add(album)
        db.session.commit()
        return redirect(url_for("albums.list_albums"))

    genre = request.args.get("genre")
    sort = request.args.get("sort")

    query = Album.query
    if genre:
        query = query.filter_by(genre=genre)
    if sort == "year":
        query = query.order_by(Album.year.desc())

    albums = query.all()
    return render_template("albums.html", albums=albums)

@bp.post("/delete/<int:album_id>")
@login_required
def delete_album(album_id):
    if not current_user.is_admin():
        abort(403)

    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    return redirect(url_for("albums.list_albums"))


@bp.route("/edit/<int:album_id>", methods=["GET", "POST"])
@login_required
def edit_album(album_id):
    if not current_user.is_admin():
        abort(403)

    album = Album.query.get_or_404(album_id)

    if request.method == "POST":
        album.artist = request.form["artist"]
        album.title = request.form["title"]
        album.genre = request.form["genre"]
        album.year = int(request.form["year"])
        album.rating = request.form.get("rating")

        db.session.commit()
        return redirect(url_for("albums.list_albums"))

    return render_template("edit_album.html", album=album)
