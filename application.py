from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")
# db1 = SQL("sqlite:///books.db")


@app.route("/")
#@login_required
def index():
    """Show portfolio of stocks"""


    return render_template("main.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=hash)

        # unique username constraint violated?
        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))

@app.route("/library")
# @login_required
def library():
    """Show library"""

    return render_template("library.html")

@app.route("/kafka")
# @login_required
def kafka():
    """Show Kafka"""

    return render_template("kafka.html")

@app.route("/kam")
# @login_required
def kam():
    """Show Camus"""

    return render_template("kam.html")

@app.route("/hesse")
# @login_required
def hesse():
    """Show Hesse"""

    return render_template("hesse.html")

@app.route("/sartre")
# @login_required
def sartre():
    """Show Sartre"""

    return render_template("sartre.html")

@app.route("/strugat")
# @login_required
def strugat():
    """Show Strugatsky"""

    return render_template("strugat.html")


@app.route("/poe")
# @login_required
def poe():
    """Show Poe"""

    return render_template("poe.html")

@app.route("/dost")
# @login_required
def dost():
    """Show Dostoevskiy"""

    return render_template("dost.html")


@app.route("/order", methods=["GET", "POST"])
# @login_required
def order():
    """Request Books"""
    # return render_template("order.html")
    if request.method == "GET":
        return render_template("order.html")
    else:
        title = request.form.get("title")
        author = request.form.get("author")
        db.execute("INSERT INTO books (user_id, title, author) VALUES (:user_id, :title, :author)", user_id=session["user_id"], title=title, author=author)
        return redirect("/history")

# @app.route("/history")
# #@login_required
# def history():
#     books = db.execute("SELECT title, author FROM books WHERE user_id = :user_id", user_id=session["user_id"])
#     return render_template("history.html", books=books)

@app.route("/history")
# @login_required
def history():
    rows = db.execute("SELECT  title, author, status, MAX(date) as date FROM books WHERE user_id = :user_id GROUP BY title  ORDER BY date DESC", user_id=session["user_id"])
    return render_template("history.html", rows=rows)