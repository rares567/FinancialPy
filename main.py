import config, sqlite3
from flask import Flask, render_template, request, redirect, url_for

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

    return render_template("index.html", stocks=rows)

@app.route("/search")
def search(query:str):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
            SELECT id, symbol, name
            FROM stock
            WHERE symbol LIKE ? OR name LIKE ?
            ORDER BY symbol
        """, (f"%{query}%", f"%{query}%"))

    rows = cursor.fetchall()

    return render_template("index.html", stocks=rows, query=query)

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

    return render_template("stock_detail.html", stock=row, bars=prices, last_bar=prices[-1])

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
        SELECT quantity, bought_price FROM portfolio
    """)

    portfolio = cursor.fetchall()

    cursor.execute("""
        SELECT symbol, name
        FROM stock JOIN portfolio on portfolio.stock_id = stock.id
    """)

    stock_names = cursor.fetchall()

    return render_template("portfolio.html", stock_names=stock_names, portfolio=portfolio)

if __name__ == "__main__":
    app.run(debug=True)