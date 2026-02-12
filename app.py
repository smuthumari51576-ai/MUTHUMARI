from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from database import db
from models import User, Role

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create tables & predefined roles + admin
with app.app_context():
    db.create_all()

    # Create roles if not exists
    if not Role.query.first():
        admin_role = Role(name="admin")
        teacher_role = Role(name="teacher")
        student_role = Role(name="student")

        db.session.add_all([admin_role, teacher_role, student_role])
        db.session.commit()

        # Create predefined admin
        admin_user = User(username="admin", password="admin123", role_id=admin_role.id)
        db.session.add(admin_user)
        db.session.commit()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role.name

            if user.role.name == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user.role.name == "teacher":
                return redirect(url_for("teacher_dashboard"))
            else:
                return redirect(url_for("student_dashboard"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role_name = request.form["role"]

        role = Role.query.filter_by(name=role_name).first()

        new_user = User(username=username, password=password, role_id=role.id)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route("/teacher")
def teacher_dashboard():
    return render_template("teacher_dashboard.html")


@app.route("/student")
def student_dashboard():
    return render_template("student_dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
