import os, sqlite3, re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__, static_url_path='',
            static_folder='templates',
            template_folder='templates')
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
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

#Configure CS50 Library to use SQLite database
db = SQL("sqlite:///stuffsaver.db")


@app.route("/")
#@login_required
def home():
    return render_template("homepage.html")



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Add a new item
    if request.method == "POST":
        pass
    else:
        # Retrieving the username
        username = session.get("username")

        rows = db.execute("SELECT DISTINCT category FROM " + username + "")


        return render_template("add.html", rows=rows)

@app.route("/add/existing", methods=["POST"])
@login_required
def add_existing():

    # Checking the fields are filled out
    if not request.form.get("field_1"):
        flash("Please fill out all fields.")
        return render_template("add_existing.html")
    elif not request.form.get("field_2"):
        flash("Please fill out all fields.")
        return render_template("add_existing.html")
    elif not request.form.get("field_3"):
        flash("Please fill out all fields.")
        return render_template("add_existing.html")

    # Storing user input into variables
    field_1 = request.form.get("field_1")
    field_2 = request.form.get("field_2")
    field_3 = request.form.get("field_3")
    category = request.form.get("category")

    # Retrieving the username to insert data in the user's table
    username = session.get("username")
    rows = db.execute("SELECT category FROM " + username + "")

    db.execute("INSERT INTO " + username + """
    (user_id, category, field_1, field_2, field_3)
    VALUES
    (:user_id, :category, :field_1, :field_2, :field_3)
    """,
    user_id = session["user_id"],
    category=category,
    field_1=field_1,
    field_2=field_2,
    field_3=field_3)

    flash("Succesfully added!")
    return redirect("/summary")


@app.route("/add/existing/<category>", methods=["GET"])
@login_required
def add_already_existing(category):


    return render_template("add_existing.html", category=category)


@app.route("/add/custom", methods=["GET", "POST"])
@login_required
def custom():
    if request.method == "POST":

        # Checking the fields are filled out
        if not request.form.get("category"):
            flash("Please fill out all fields.")
            return render_template("add_custom.html")
        elif not request.form.get("field_1"):
            flash("Please fill out all fields.")
            return render_template("add_custom.html")
        elif not request.form.get("field_2"):
            flash("Please fill out all fields.")
            return render_template("add_custom.html")
        elif not request.form.get("field_3"):
            flash("Please fill out all fields.")
            return render_template("add_custom.html")

        else:

            # Storing user input into variables
            category = request.form.get("category")
            field_1 = request.form.get("field_1")
            field_2 = request.form.get("field_2")
            field_3 = request.form.get("field_3")

            # Retrieving the username to insert data in the user's table
            username = session.get("username")


            # Storing user input in DB
            db.execute("INSERT INTO " + username + """
            (user_id, category, field_1, field_2, field_3)
            VALUES (:user_id, :category, :field_1, :field_2, :field_3)""",
            user_id = session["user_id"],
            category=category,
            field_1=field_1,
            field_2=field_2,
            field_3=field_3)


            flash("Successfully added!")
            return redirect("/summary")
    else:
        return render_template("add_custom.html")

@app.route("/summary")
@login_required
def summary():
    #Show an overview of what the user has added so far

    username = session.get("username")
    rows = db.execute("SELECT category, field_1, field_2, field_3, date_time FROM " + username + "")



    return render_template("summary.html", rows=rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
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
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = username


        # Redirect user to home page
        flash("Login successful!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # if submitting the form
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password")

        # Creating variables for data input

        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirmation")

        # Checking passwords match
        if password != password_confirm:
            return apology("Passwords do not match. Please try again.")

        # Hashing password
        hashed_pw = generate_password_hash(password)

        # Store username and password in database
        username_and_password = db.execute("INSERT INTO users(username, hash) VALUES (:username, :hashed_pw)",
                                username=username, hashed_pw=hashed_pw)
        # New code

        db.execute("CREATE TABLE " + username + """
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        field_1 TEXT NOT NULL,
        field_2 TEXT NOT NULL,
        field_3 TEXT NOT NULL,
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) )""")

        session["username"] = username

        flash("Successfully registered! To log in, click on Log In.")
        return redirect("/")

    # If this is a GET request
    else:
        return render_template("register.html")

    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
