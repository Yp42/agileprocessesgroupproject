from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register")
def register():
    # Direct rendering of the choose_role.html when the REGISTER button is clicked
    return render_template("role.html")


@main.route("/login", methods=("GET", "POST"))
def login():
    # Direct rendering of the login.html when the LOGIN button is clicked
    return render_template("login.html")
