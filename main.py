import config, sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
       SELECT id, symbol, name FROM stock ORDER BY symbol
    """)

    rows = cursor.fetchall()

    cursor.execute("""
            SELECT balance FROM virtual_balance
        """)

    # round shown balance to 2 digits
    balance = round(cursor.fetchone()["balance"], 2)

    return render_template("index.html", stocks=rows, is_portfolio_page=False, balance=balance)

@app.route("/search")
def search():
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = request.args.get("q", "")
    cursor.execute("""
            SELECT id, symbol, name
            FROM stock
            WHERE symbol LIKE ? OR name LIKE ?
            ORDER BY symbol
        """, (f"%{query}%", f"%{query}%"))

    rows = cursor.fetchall()

    return render_template("index.html", stocks=rows)

@app.route("/stock/<symbol>")
def stock_detail(symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
            SELECT id, symbol, name FROM stock WHERE symbol = ?
        """, (symbol,))

    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ?
    """, (row["id"],))

    prices = cursor.fetchall()

    cursor.execute("""
            SELECT balance FROM virtual_balance
        """)

    # round shown balance to 2 digits
    balance = round(cursor.fetchone()["balance"], 2)

    return render_template("stock_detail.html", stock=row, bars=prices, last_bar=prices[-1], balance=balance)

@app.route("/buy_stock/<symbol>", methods=['POST'])
def buy_stock(symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, name FROM stock WHERE symbol = ?
    """, (symbol,))

    row = cursor.fetchone()
    stock_id = row["id"]

    cursor.execute("""
        SELECT * FROM stock_price
        WHERE stock_id = ?
        ORDER BY date DESC
    """, (stock_id,))

    row = cursor.fetchone()
    stock_price = row["close"]
    quantity = int(request.form['quantity'])
    # cost of buying the chosen stocks
    cost = stock_price * quantity

    cursor.execute("""
        SELECT balance FROM virtual_balance
    """)

    balance = cursor.fetchone()["balance"]
    # flash user if they cannot afford the transaction selected
    if (cost > balance):
        flash("You do not have enough money for this transaction!")
        return redirect(url_for("stock_detail", symbol=symbol))

    # update balance after purchase
    cursor.execute("""
            UPDATE virtual_balance SET balance = balance - ?
        """, (cost,))

    cursor.execute("""
        INSERT INTO portfolio (stock_id, quantity, bought_price) VALUES (?, ?, ?)
    """, (stock_id, quantity, stock_price))

    connection.commit()

    return redirect(url_for("portfolio"))

@app.route("/portfolio")
def portfolio():
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT stock.symbol, stock.name, portfolio.quantity, portfolio.bought_price
        FROM stock JOIN portfolio on stock.id = portfolio.stock_id
    """)

    rows = cursor.fetchall()

    cursor.execute("""
        SELECT balance FROM virtual_balance
    """)

    # round shown balance to 2 digits
    balance = round(cursor.fetchone()["balance"], 2)

    cursor.execute("""
        SELECT COUNT (*) FROM portfolio
    """)

    # get count of number of rows (used for truncating the recent prices table)
    count = cursor.fetchone()[0]

    # use left join to keep duplicates of stocks in the order that they appear in the table!!!!!
    cursor.execute("""
        SELECT stock_price.close, stock_price.date
        FROM portfolio LEFT JOIN stock_price on stock_price.stock_id = portfolio.stock_id
        ORDER BY date DESC
    """)

    recent_prices = cursor.fetchall()

    return render_template("portfolio.html", stocks_prices=list(zip(rows, recent_prices[:count])), balance=balance, is_portfolio_page=True)

if __name__ == "__main__":
    app.run(debug=True)