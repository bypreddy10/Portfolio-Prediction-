from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import yfinance as yf
import time
import threading
import socket

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Portfolio: US + Indian Stocks ---
portfolio = {
    # Initialize with 1-hour price tracking
    symbol: {**data, "price_1h": 0} for symbol, data in {
    # US Tech Stocks
    "AAPL": {"shares": 10, "price": 0},    # Apple
    "MSFT": {"shares": 5, "price": 0},     # Microsoft
    "TSLA": {"shares": 4, "price": 0},     # Tesla
    "GOOGL": {"shares": 6, "price": 0},    # Alphabet (Google)
    "AMZN": {"shares": 8, "price": 0},     # Amazon
    "NVDA": {"shares": 2, "price": 0},     # Nvidia
    "META": {"shares": 3, "price": 0},     # Meta (Facebook)
    "NFLX": {"shares": 5, "price": 0},     # Netflix
    "AMD": {"shares": 7, "price": 0},      # AMD
    "INTC": {"shares": 6, "price": 0},     # Intel
    "CRM": {"shares": 4, "price": 0},      # Salesforce
    "ORCL": {"shares": 3, "price": 0},     # Oracle
    "ADBE": {"shares": 2, "price": 0},     # Adobe
    "PYPL": {"shares": 5, "price": 0},     # PayPal
    "UBER": {"shares": 8, "price": 0},     # Uber
    "SNAP": {"shares": 10, "price": 0},    # Snap
    "SPOT": {"shares": 3, "price": 0},     # Spotify
    "ZM": {"shares": 4, "price": 0},       # Zoom
    "SHOP": {"shares": 2, "price": 0},     # Shopify
    "ROKU": {"shares": 6, "price": 0},     # Roku

    # US Blue Chip Stocks
    "JPM": {"shares": 5, "price": 0},      # JPMorgan Chase
    "BAC": {"shares": 8, "price": 0},      # Bank of America
    "WFC": {"shares": 6, "price": 0},      # Wells Fargo
    "JNJ": {"shares": 4, "price": 0},      # Johnson & Johnson
    "PFE": {"shares": 7, "price": 0},      # Pfizer
    "XOM": {"shares": 3, "price": 0},      # ExxonMobil
    "CVX": {"shares": 2, "price": 0},      # Chevron
    "DIS": {"shares": 5, "price": 0},      # Disney
    "NKE": {"shares": 4, "price": 0},      # Nike
    "MCD": {"shares": 3, "price": 0},      # McDonald's
    "KO": {"shares": 6, "price": 0},       # Coca-Cola
    "PEP": {"shares": 5, "price": 0},      # PepsiCo
    "WMT": {"shares": 4, "price": 0},      # Walmart
    "HD": {"shares": 3, "price": 0},       # Home Depot
    "V": {"shares": 2, "price": 0},        # Visa
    "MA": {"shares": 3, "price": 0},       # Mastercard

    # Additional US Tech Stocks
    "CRM": {"shares": 4, "price": 0},       # Salesforce
    "ORCL": {"shares": 3, "price": 0},      # Oracle
    "ADBE": {"shares": 2, "price": 0},      # Adobe
    "PYPL": {"shares": 5, "price": 0},      # PayPal
    "UBER": {"shares": 8, "price": 0},      # Uber
    "SNAP": {"shares": 10, "price": 0},   # Snap
    "SPOT": {"shares": 3, "price": 0},    # Spotify
    "ZM": {"shares": 4, "price": 0},      # Zoom
    "SHOP": {"shares": 2, "price": 0},    # Shopify
    "ROKU": {"shares": 6, "price": 0},    # Roku
    "COIN": {"shares": 4, "price": 0},    # Coinbase
    "TWLO": {"shares": 3, "price": 0},    # Twilio
    "DDOG": {"shares": 2, "price": 0},    # Datadog
    "NET": {"shares": 5, "price": 0},     # Cloudflare
    "PLTR": {"shares": 8, "price": 0},    # Palantir
    "SNOW": {"shares": 3, "price": 0},    # Snowflake
    "CRWD": {"shares": 4, "price": 0},    # CrowdStrike
    "OKTA": {"shares": 2, "price": 0},    # Okta
    "ROKU": {"shares": 6, "price": 0},    # Roku

    # US Blue Chip Stocks
    "JPM": {"shares": 5, "price": 0},     # JPMorgan Chase
    "BAC": {"shares": 8, "price": 0},     # Bank of America
    "WFC": {"shares": 6, "price": 0},     # Wells Fargo
    "JNJ": {"shares": 4, "price": 0},     # Johnson & Johnson
    "PFE": {"shares": 7, "price": 0},     # Pfizer
    "XOM": {"shares": 3, "price": 0},     # ExxonMobil
    "CVX": {"shares": 2, "price": 0},     # Chevron
    "DIS": {"shares": 5, "price": 0},     # Disney
    "NKE": {"shares": 4, "price": 0},     # Nike
    "MCD": {"shares": 3, "price": 0},     # McDonald's
    "KO": {"shares": 6, "price": 0},      # Coca-Cola
    "PEP": {"shares": 5, "price": 0},     # PepsiCo
    "WMT": {"shares": 4, "price": 0},     # Walmart
    "HD": {"shares": 3, "price": 0},      # Home Depot
    "V": {"shares": 2, "price": 0},       # Visa
    "MA": {"shares": 3, "price": 0},      # Mastercard
    "PG": {"shares": 4, "price": 0},      # Procter & Gamble
    "UNH": {"shares": 2, "price": 0},     # UnitedHealth
    "ABT": {"shares": 5, "price": 0},     # Abbott Laboratories
    "T": {"shares": 8, "price": 0},       # AT&T
    "VZ": {"shares": 6, "price": 0},      # Verizon
    "IBM": {"shares": 4, "price": 0},     # IBM
    "GE": {"shares": 7, "price": 0},      # General Electric
    "CAT": {"shares": 3, "price": 0},     # Caterpillar
    "MMM": {"shares": 2, "price": 0},     # 3M
    "BA": {"shares": 4, "price": 0},      # Boeing
    "LMT": {"shares": 2, "price": 0},     # Lockheed Martin

    # Indian Stocks (NSE) - More reliable symbols
    "RELIANCE.NS": {"shares": 10, "price": 0},   # Reliance Industries
    "TCS.NS": {"shares": 5, "price": 0},         # Tata Consultancy Services
    "INFY.NS": {"shares": 8, "price": 0},        # Infosys
    "HDFCBANK.NS": {"shares": 6, "price": 0},    # HDFC Bank
    "ICICIBANK.NS": {"shares": 10, "price": 0},  # ICICI Bank
    "SBIN.NS": {"shares": 15, "price": 0},       # State Bank of India
    "ITC.NS": {"shares": 12, "price": 0},        # ITC Limited
    "AXISBANK.NS": {"shares": 8, "price": 0},    # Axis Bank
    "KOTAKBANK.NS": {"shares": 6, "price": 0},   # Kotak Mahindra Bank
    "BHARTIARTL.NS": {"shares": 8, "price": 0},  # Bharti Airtel
    "LT.NS": {"shares": 4, "price": 0},          # Larsen & Toubro
    "HINDUNILVR.NS": {"shares": 5, "price": 0},  # Hindustan Unilever
    "ASIANPAINT.NS": {"shares": 6, "price": 0},  # Asian Paints
    "MARUTI.NS": {"shares": 3, "price": 0},       # Maruti Suzuki
    "TITAN.NS": {"shares": 7, "price": 0},        # Titan Company
    "ULTRACEMCO.NS": {"shares": 2, "price": 0},   # UltraTech Cement
    "NESTLEIND.NS": {"shares": 1, "price": 0},   # Nestle India
    "BAJFINANCE.NS": {"shares": 4, "price": 0},   # Bajaj Finance
    "M&M.NS": {"shares": 5, "price": 0},          # Mahindra & Mahindra
    "POWERGRID.NS": {"shares": 9, "price": 0},   # Power Grid Corporation
    "NTPC.NS": {"shares": 11, "price": 0},        # NTPC Limited
    "SUNPHARMA.NS": {"shares": 6, "price": 0},   # Sun Pharmaceutical
    "DRREDDY.NS": {"shares": 4, "price": 0},     # Dr. Reddy's Labs
    "CIPLA.NS": {"shares": 8, "price": 0},       # Cipla
    "TATACONSUM.NS": {"shares": 12, "price": 0}, # Tata Consumer Products
    "HCLTECH.NS": {"shares": 7, "price": 0},     # HCL Technologies
    "TECHM.NS": {"shares": 9, "price": 0},      # Tech Mahindra
    "WIPRO.NS": {"shares": 20, "price": 0},     # Wipro
}.items()}

@app.route("/")
def home():
    return render_template("index.html", portfolio=portfolio)

def fetch_prices():
    """Background thread to update prices"""
    while True:
        for symbol in portfolio:
            try:
                ticker = yf.Ticker(symbol)
                # Get 1-day data for current price
                data = ticker.history(period="1d")
                # Get intraday data for 1-hour comparison (use 1d with 1h interval)
                data_intraday = ticker.history(period="1d", interval="1h")
                
                if not data.empty and len(data) > 0:
                    new_price = round(data["Close"].iloc[-1], 2)
                    old_price = portfolio[symbol]["price"]
                    
                    # Get 1-hour ago price from intraday data
                    if data_intraday is not None and not data_intraday.empty:
                        if len(data_intraday) >= 2:
                            # Get the price from 1 hour ago (second to last)
                            price_1h_ago = round(data_intraday["Close"].iloc[-2], 2)
                        elif len(data_intraday) == 1:
                            # If only one hour of data, use current price
                            price_1h_ago = new_price
                        else:
                            # No intraday data, use stored 1h price or current
                            price_1h_ago = portfolio[symbol]["price_1h"] if portfolio[symbol]["price_1h"] != 0 else new_price
                    else:
                        # No intraday data available
                        price_1h_ago = portfolio[symbol]["price_1h"] if portfolio[symbol]["price_1h"] != 0 else new_price
                    
                    # Calculate 1-hour change
                    change_1h = round(new_price - price_1h_ago, 2)
                    
                    # Emit update if price changes or it's the first update
                    if new_price != old_price or old_price == 0:
                        change = round(new_price - old_price, 2) if old_price != 0 else 0
                        socketio.emit('price_update', {
                            "symbol": symbol,
                            "new_price": new_price,
                            "change": change,
                            "price_1h_ago": price_1h_ago,
                            "change_1h": change_1h
                        })
                    
                    portfolio[symbol]["price"] = new_price
                    portfolio[symbol]["price_1h"] = price_1h_ago
                    
                else:
                    print(f"⚠️ No data available for {symbol}")
                    
            except Exception as e:
                print(f"❌ Error fetching {symbol}: {e}")
                # Continue with next stock instead of stopping

        time.sleep(10)  # Fetch every 10 seconds

@socketio.on('connect')
def handle_connect():
    print("✅ Client connected!")

if __name__ == "__main__":
    # Background price fetch thread
    thread = threading.Thread(target=fetch_prices)
    thread.daemon = True
    thread.start()

    # Automatically find a free port
    s = socket.socket()
    s.bind(('', 0))
    free_port = s.getsockname()[1]
    s.close()

    print(f"🚀 Starting Flask-SocketIO on available port {free_port}...")
    socketio.run(app, debug=False, use_reloader=False, port=free_port)
