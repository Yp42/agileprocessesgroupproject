from flask import Blueprint, render_template, request

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
    if request.method == "POST":
        if request.form["username"] == "123" and request.form["pswd"] == "123":
            return render_template("index.html")
        else:
            return render_template("login.html", failed=True)
    else:
        return render_template("login.html")
