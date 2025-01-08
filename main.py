import config, sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

from trading_bot import buy_or_sell, predict_price_trend

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

    cursor.execute("""
            SELECT quantity FROM portfolio WHERE stock_id = ?
        """, (row["id"],))

    # get stock quantity for selling stock (cannot sell more than is owned)
    stocks = cursor.fetchall()
    stock_quantity = 0
    for stock in stocks:
        stock_quantity += stock["quantity"]

    price_trend = predict_price_trend(symbol);

    return render_template("stock_detail.html", stock=row, bars=prices,
                           last_bar=prices[-1], balance=balance, stock_quantity=stock_quantity,
                           action=buy_or_sell(symbol), trend=price_trend['trend'], patterns=price_trend['patterns'])

@app.route("/buy_stock/<symbol>", methods=['POST'])
def buy_stock(symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM stock WHERE symbol = ?
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
    quantity = int(request.form['buy-quantity'])
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

@app.route("/sell_stock/<symbol>", methods=['POST'])
def sell_stock(symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM stock WHERE symbol = ?
    """, (symbol,))

    row = cursor.fetchone()
    stock_id = row["id"]

    cursor.execute("""
        SELECT id, quantity FROM portfolio WHERE stock_id = ?
    """, (stock_id,))

    # remove the sold stocks from portfolio
    stocks = cursor.fetchall()
    sold_quantity = int(request.form['sell-quantity'])
    for stock in stocks:
        if stock["quantity"] <= sold_quantity:
            # stock["id"] in this context is the row id of portfolio!!!
            cursor.execute("""
                DELETE FROM portfolio WHERE id = ?
            """, (stock["id"],))
            sold_quantity -= stock["quantity"]
        elif sold_quantity > 0:
            cursor.execute("""
                UPDATE portfolio SET quantity = quantity - ? WHERE id = ?
            """, (sold_quantity, stock["id"]))
            sold_quantity = 0
        else:
            break

    cursor.execute("""
        SELECT * FROM stock_price
        WHERE stock_id = ?
        ORDER BY date DESC
    """, (stock_id,))

    row = cursor.fetchone()
    stock_price = row["close"]
    quantity = int(request.form['sell-quantity'])
    # calculate money gained and add it to virtual balance
    value = stock_price * quantity

    cursor.execute("""
        UPDATE virtual_balance SET balance = balance + ?
    """, (value,))

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
        SELECT stock_price.close
        FROM portfolio LEFT JOIN stock_price on stock_price.stock_id = portfolio.stock_id
        ORDER BY date DESC
    """)

    recent_prices = cursor.fetchall()
    # create a list of the 2 lists in parallel for easier iteration (take only required number of prices)
    stocks_prices = list(zip(rows, recent_prices[:count]))

    return render_template("portfolio.html", stocks_prices=stocks_prices, balance=balance, is_portfolio_page=True)

if __name__ == "__main__":
    app.run(debug=True)