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

from werkzeug.security import (generate_password_hash,check_password_hash)

from functools import wraps
def admin_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if not current_user.is_admin:

            flash(
                "Administrator access required.",
                "danger"
            )

            return redirect(url_for("dashboard"))

        return f(*args, **kwargs)

    return decorated_function



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

    is_admin = db.Column(
        db.Boolean,
        default=False
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


@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )

@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        existing_user = User.query.filter_by(email=email).first()

        if existing_user and existing_user.id != current_user.id:

            flash(
                "Email is already in use.",
                "danger"
            )

            return redirect(url_for("edit_profile"))

        current_user.email = email

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(url_for("profile"))

    return render_template("edit_profile.html")



@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        confirm_password = request.form["confirm_password"]

        # Check current password

        if not check_password_hash(
            current_user.password,
            current_password
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(url_for("change_password"))

        # Password length

        if len(new_password) < 8:

            flash(
                "Password must be at least 8 characters.",
                "warning"
            )

            return redirect(url_for("change_password"))

        # Match confirmation

        if new_password != confirm_password:

            flash(
                "Passwords do not match.",
                "warning"
            )

            return redirect(url_for("change_password"))

        # Optional: don't allow the same password again

        if check_password_hash(
            current_user.password,
            new_password
        ):

            flash(
                "New password must be different.",
                "warning"
            )

            return redirect(url_for("change_password"))

        current_user.password = generate_password_hash(
            new_password
        )

        db.session.commit()

        flash(
            "Password changed successfully!",
            "success"
        )

        logout_user()

        flash(
            "Password changed successfully. Please log in again.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("change_password.html")

@app.route("/admin")
@login_required
@admin_required
def admin():

    total_users = User.query.count()
    users = User.query.all()
    return render_template(
        "admin.html",
        total_users=total_users,
        users = users
    )



if __name__ == "__main__":
    app.run(debug=True)