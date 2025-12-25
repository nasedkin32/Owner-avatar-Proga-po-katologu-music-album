from flask import Flask, render_template
from flask_login import LoginManager
from models.album import db, Album
from models.user import User, UserRepo

from controllers.albums_controller import bp as albums_bp
from controllers.auth_controller import bp as auth_bp

app = Flask(__name__, template_folder="views", static_folder="static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
app.config["SECRET_KEY"] = "secret_key"

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(albums_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def index():
    albums = Album.query.all()
    return render_template("index.html", albums=albums)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    repo = UserRepo()
    if not repo.get_by_username("admin"):
        repo.add("admin", "admin123", role="admin")

if __name__ == "__main__":
    app.run(debug=True)
