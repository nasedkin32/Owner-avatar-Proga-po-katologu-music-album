from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user import UserRepo

bp = Blueprint("auth", __name__, url_prefix="/auth")
repo = UserRepo()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = repo.get_by_username(request.form["username"])

        if user and user.check_password(request.form["password"]):
            login_user(user)
            flash("Успешный вход", "success")
            return redirect(url_for("albums.list_albums"))

        flash("Неверный логин или пароль", "error")

    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if repo.get_by_username(request.form["username"]):
            flash("Пользователь уже существует", "error")
        else:
            repo.add(
                request.form["username"],
                request.form["password"]
            )
            flash("Регистрация успешна", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("auth.login"))
