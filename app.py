import os
import csv

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, send_file, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///food.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show history of transactions"""
    return render_template("index.html")



@app.route("/today")
@login_required
def today():
    foods = db.execute("SELECT * FROM food WHERE user_id = ?",session["user_id"])
    summ = [0,0,0,0]
    for food in foods:
        summ[0] += int(float(food["energy"]))
        summ[1] += float(food["protein"])
        summ[2] += float(food["fat"])
        summ[3] += float(food["carbs"])
    for i in range(1,4):
        summ[i] = "{:.2f}".format(summ[i])
    return render_template("today.html",foods = foods, summ = summ)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("food"):
            return apology("must provide a food name", 400)
        elif not request.form.get("categories"):
            return apology("What type of food", 400)
        elif not lookup(request.form.get("food"), int(request.form.get("categories"))):
            return apology("food not found", 400)
        category = int(request.form.get("categories"))
        query = request.form.get("food")
        foods = lookup(request.form.get("food"),category)
        return render_template("looked.html",foods = foods)
    else:
        return render_template("add.html",show = False)


@app.route("/tolist")
@login_required
def add_to_list():
    food = request.args["add_button"]
    food = list(food.split("/"))
    db.execute("INSERT INTO food(id,user_id,description,energy,protein,fat,carbs) VALUES(?,?,?,?,?,?,?)",food[0],session["user_id"],food[1],food[2],food[3],food[4],food[5])
    return render_template("add.html",show = True)


@app.route("/remove")
@login_required
def remove():
    food = request.args["remove_btn"]
    db.execute("DELETE FROM food WHERE id = ? AND user_id = ?",food,session["user_id"])
    return redirect("/today")


@app.route("/download")
@login_required
def download():
    table = db.execute("SELECT description,energy,protein,fat,carbs FROM food WHERE user_id = ?",session["user_id"])
    fields = ["description","energy",'protein',"fat","carbs"]
    summ = {"energy" : 0 ,"protein" : 0 , "fat" : 0 , "carbs" : 0 , "description" : "sum"}
    for food in table:
        summ["energy"] += int(float(food["energy"]))
        summ["protein"] += float(food["protein"])
        summ["fat"] += float(food["fat"])
        summ["carbs"] += float(food["carbs"])
    with open("output.csv", "w", newline="") as csvfile:
        # Create a CSV writer using the field/column names
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Write the header row (column names)
        writer.writeheader()
        # Write the data
        for row in table:
            writer.writerow(row)
        writer.writerow(summ)
    path = "output.csv"
    return send_file(path,as_attachment=True)


@app.route("/reset")
@login_required
def reset():
    db.execute("DELETE FROM food WHERE user_id = ?",session["user_id"])
    return redirect("/today")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm your password", 400)
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("must check your password again", 400)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if rows:
            return apology("username already used", 400)
        db.execute(
            "INSERT INTO users (username,hash) VALUES (?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )
        number = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = number[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")
