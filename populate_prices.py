from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import config
import alpaca_trade_api as tradeapi
import sqlite3
import datetime

def adapt_date(date_obj):
    return date_obj.isoformat()

def convert_date(date_text):
    return datetime.date.fromisoformat(date_text)

sqlite3.register_adapter(datetime.date, adapt_date)
sqlite3.register_converter("DATE", convert_date)

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""SELECT id,symbol,name FROM stock""")

rows = cursor.fetchall()

symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = {"id": row['id'], "name": row['name']}

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i + chunk_size]

barsets = api.get_bars(["AAPL", "MSFT"], TimeFrame.Hour, "2024-12-31", "2024-12-31", adjustment='raw')


for bar in barsets:
    symbol = bar.S
    print(f"Processing symbol {symbol}")

    if symbol not in stock_dict:
        print(f"Symbol {symbol} not found...")
        continue

    stock_id = stock_dict[symbol]["id"]
    stock_name = stock_dict[symbol]["name"]

    cursor.execute("""INSERT INTO stock_price (id, stock_id, name, date, open, high, low, close, volume)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (None, stock_id, stock_name, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

connection.commit()
connection.close()