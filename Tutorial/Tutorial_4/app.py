from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

app.config["SECRET_KEY"] ="alksfjlj34"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )
    
with app.app_context():
    db.create_all()


@app.route("/")
def index():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Username exists?

        if User.query.filter_by(username=username).first():

            flash("Username already exists.")

            return redirect(url_for("register"))

        # Email exists?

        if User.query.filter_by(email=email).first():

            flash("Email already exists.")

            return redirect(url_for("register"))

        user = User(

            username=username,

            email=email,

            password=generate_password_hash(password)

        )

        db.session.add(user)

        db.session.commit()

        flash("Registration successful!")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash("Welcome!")

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )
    
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.")

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)