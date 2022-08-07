import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    # get user cash total
    u_id=session["user_id"]
    result = db.execute("SELECT cash FROM users WHERE id=?", u_id)
    cash = result[0]['cash']
    # pull all transactions belonging to user
    portfolio = db.execute("SELECT stock, quantity FROM portfolio")
    if not portfolio:
        return apology("sorry you have no holdings")
    grand_total = cash
    # determine current price, stock total value and grand total value
    for stock in portfolio:
        price = lookup(stock['stock'])['price']
        total = stock['quantity'] * price
        stock.update({'price': price, 'total': total})
        grand_total += total
    return render_template("index.html", stocks=portfolio, cash=cash, total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if (not request.form.get("stock")) or (not request.form.get("shares")) :
            return apology("must provide stock name or number of shares")
        if int(request.form.get("shares"))<=0:
            return apology("Invalid number of shares")
        #if valid
        quote=lookup(request.form.get("stock"))
        if quote==None:
            return apology("Stock symbol not valid, please try again")
        cost=int(request.form.get("shares"))*quote["price"]
        #check if enough cash
        u_id=session["user_id"]
        result = db.execute("SELECT cash FROM users WHERE id=?",u_id)
        if cost > result[0]["cash"]:
            return apology("you do not have enough cash for this transaction")
        # update cash amount in users database
        db.execute("UPDATE users SET cash=cash-:cost WHERE id=:id", cost=cost, id=session["user_id"]);

        # add transaction to transaction database
        add_transaction = db.execute("INSERT INTO data (user_id, stock, qty, price, date) VALUES (:user_id, :stock, :qty, :price, :date)",
            user_id=session["user_id"], stock=quote["symbol"], qty=int(request.form.get("shares")), price=quote['price'], date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # pull number of shares of symbol in portfolio
        curr_portfolio = db.execute("SELECT quantity FROM portfolio WHERE stock=:stock", stock=quote["symbol"])

        # add to portfolio database
        # if symbol is new, add to portfolio
        if not curr_portfolio:
            db.execute("INSERT INTO portfolio (stock, quantity) VALUES (:stock, :quantity)",
                stock=quote["symbol"], quantity=int(request.form.get("shares")))

        # if symbol is already in portfolio, update quantity of shares and total
        else:
            db.execute("UPDATE portfolio SET quantity=quantity+:quantity WHERE stock=:stock",
                quantity=int(request.form.get("shares")), stock=quote["symbol"]);

        return redirect("/")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    u_id=session["user_id"]
    portfolio = db.execute("SELECT stock, qty, price, date FROM data WHERE user_id=?", u_id)
    if not portfolio:
        return apology("sorry you have no transactions on record")
    return render_template("history.html", stocks=portfolio)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("get_stock"):
            return apology("Enter stock name")
        quote=lookup(request.form.get("get_stock"))
        if quote==None:
            return apology("Invalid Symbol")
        else:
            return render_template("quoted.html", quote=quote)
    else:
         return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide username")
        elif not request.form.get("password") and not request.form.get("confirm_password"):
            return apology("Must provide password")
        elif ( request.form.get("password") != request.form.get("confirm_password")):
            return apology("password do not match")
        else:
            username=request.form.get("username")
            #generating password hash
            pw_hash=generate_password_hash(request.form.get("password"))
            #checking if username already exists
            rows=db.execute("SELECT * FROM users WHERE username = ?",username)
            if len(rows)!=0:
                return apology("User already Created")
            #add current user
            curr_user=db.execute("INSERT INTO users(username,hash) VALUES(?,?)",username,pw_hash)
            #remembering current user
            session["user_id"] = curr_user
            return redirect("/")
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if (not request.form.get("stock")) or (not request.form.get("shares")) :
            return apology("must provide stock name or number of shares")
        if int(request.form.get("shares"))<=0:
            return apology("Invalid number of shares")
        available = db.execute("SELECT quantity FROM portfolio WHERE stock=?",request.form.get("stock"))

        # check that number of shares being sold does not exceed quantity in portfolio
        if int(request.form.get("shares")) > available[0]['quantity']:
            return apology("You may not sell more shares than you currently hold")

        # pull quote from yahoo finance
        quote = lookup(request.form.get("stock"))
        if quote == None:
            return apology("Stock symbol not valid, please try again")
        cost = int(request.form.get("shares")) * quote['price']
        u_id=session["user_id"]
        # update cash amount in users database
        db.execute("UPDATE users SET cash=cash+? WHERE id=?", cost,u_id);
        db.execute("INSERT INTO data (user_id, stock, qty, price, date) VALUES (:user_id, :stock, :qty, :price, :date)", user_id=session["user_id"], stock=quote["symbol"], qty=int(request.form.get("shares")), price=quote['price'], date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.execute("UPDATE portfolio SET quantity=quantity-:quantity WHERE stock=:stock",quantity=int(request.form.get("shares")), stock=quote["symbol"]);
        return redirect("/")
    else:
        # pull all transactions belonging to user
        portfolio = db.execute("SELECT stock FROM portfolio")
        return render_template("sell.html", stocks=portfolio)