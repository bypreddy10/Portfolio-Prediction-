from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import yfinance as yf
import eventlet
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Portfolio with 10 stocks ---
portfolio = {
    "AAPL": {"shares": 10, "price": 0},   # Apple
    "MSFT": {"shares": 5, "price": 0},    # Microsoft
    "TSLA": {"shares": 4, "price": 0},    # Tesla
    "GOOGL": {"shares": 6, "price": 0},   # Alphabet (Google)
    "AMZN": {"shares": 8, "price": 0},    # Amazon
    "META": {"shares": 3, "price": 0},    # Meta (Facebook)
    "NFLX": {"shares": 2, "price": 0},    # Netflix
    "NVDA": {"shares": 1, "price": 0},    # Nvidia
    "JPM": {"shares": 10, "price": 0},    # JP Morgan
    "INTC": {"shares": 20, "price": 0}    # Intel
}

@app.route("/")
def home():
    return render_template("index.html", portfolio=portfolio)

def fetch_prices():
    """Background thread to update prices"""
    while True:
        for symbol in portfolio:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="1d")
                new_price = round(data["Close"].iloc[-1], 2)
                old_price = portfolio[symbol]["price"]

                # Send price update if it changed
                if old_price != 0 and new_price != old_price:
                    change = new_price - old_price
                    socketio.emit('price_update', {
                        "symbol": symbol,
                        "new_price": new_price,
                        "change": round(change, 2)
                    })

                portfolio[symbol]["price"] = new_price
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")

        time.sleep(10)  # Update every 10 seconds

@socketio.on('connect')
def handle_connect():
    print("Client connected!")

if __name__ == "__main__":
    thread = threading.Thread(target=fetch_prices)
    thread.daemon = True
    thread.start()

    socketio.run(app, debug=True)
