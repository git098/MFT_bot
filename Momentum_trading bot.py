# Importing libraries
from kiteconnect import KiteConnect
import pandas as pd
import datetime
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

# Connecting to Zerodha Kite API
api_key = "api_key"
api_secret = "api_secret"
kite = KiteConnect(api_key=api_key)

request_token = "request_token"

data = kite.generate_session(request_token, api_secret)
access_token = data["access_token"]

kite.set_access_token(access_token)

#Stocks and capital
def main():
    stock_list = ['AARTIIND', 'AAVAS', 'AFFLE', 'ALOKINDS', 'ARE&M', 'AMBER', 'ANGELONE', 'APARINDS', 'BLS', 'BSOFT', 'BLUESTARCO', 'CESC', 'CIEINDIA', 'CANFINHOME', 'CASTROLIND', 'CEATLTD', 'CENTRALBK', 'CDSL', 'CENTURYTEX', 'CHAMBLFERT', 'CUB', 'COCHINSHIP', 'CAMS', 'CREDITACC', 'CROMPTON', 'CYIENT', 'DATAPATTNS', 'DUMMYRAYMD', 'EQUITASBNK', 'EXIDEIND', 'FINCABLES', 'FSL', 'FIVESTAR', 'GLENMARK', 'MEDANTA', 'GRAPHITE', 'GESHIP', 'GMDCLTD', 'GNFC', 'GSPL', 'HFCL', 'HAPPSTMNDS', 'HSCL', 'HINDCOPPER', 'HONASA', 'HUDCO', 'IDFC', 'IIFL', 'IRB', 'IRCON', 'ITI', 'INDIAMART', 'IEX', 'IOB', 'INTELLECT', 'JBCHEPHARM', 'JBMA', 'J&KBANK', 'JYOTHYLAB', 'KARURVYSYA', 'KEC', 'MGL', 'MANAPPURAM', 'MRPL', 'MCX', 'NATCOPHARM', 'NBCC', 'NCC', 'NLCINDIA', 'NSLNISP', 'NH', 'NATIONALUM', 'NAVINFLUOR', 'NAM-INDIA', 'OLECTRA', 'PNBHOUSING', 'PVRINOX', 'PPLPHARMA', 'PRAJIND', 'RRKABEL', 'RBLBANK', 'RITES', 'RADICO', 'RKFORGE', 'RAYMOND', 'REDINGTON', 'RENUKA', 'SHYAMMETL', 'SONATSOFTW', 'SWANENERGY', 'TANLA', 'TATAINVEST', 'TTML', 'TEJASNET', 'TITAGARH', 'TRIDENT', 'TRITURBINE', 'UCOBANK', 'UJJIVANSFB', 'WELSPUNLIV', 'ZENSARTECH']  
    allocated_capital = 20000  
    for stock in stock_list:
        apply_strategy(stock, allocated_capital)

if __name__ == "__main__":
    main()

# Technical indicators
def rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(series, slow=26, fast=12, signal=9):
    fast_ema = series.ewm(span=fast, adjust=False).mean()
    slow_ema = series.ewm(span=slow, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

def bollinger_bands(series, window=20, n_std=2):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    upper_band = rolling_mean + (rolling_std * n_std)
    lower_band = rolling_mean - (rolling_std * n_std)
    return upper_band, lower_band

#  Historical data
def get_historical_data(stock, interval="5minute"):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)
    instrument_token = kite.ltp(stock)[stock]['instrument_token']
    data = kite.historical_data(
        instrument_token=instrument_token,
        from_date=start_date.strftime('%Y-%m-%d %H:%M:%S'),
        to_date=end_date.strftime('%Y-%m-%d %H:%M:%S'),
        interval=interval
    )
    df = pd.DataFrame(data)
    return df

#  Position size
def calculate_position_size(current_capital, percentage=0.10):
    return current_capital * percentage

#  Prices
def get_latest_price(stock):
    quote = kite.ltp(stock)
    return quote[stock]['last_price']

#  Strategy and trading
def apply_strategy(stock, allocated_capital):
    df = get_historical_data(stock)
    df['rsi'] = rsi(df['close'])
    macd_line, macd_signal = macd(df['close'])
    df['macd'] = macd_line
    df['macd_signal'] = macd_signal
    df['bollinger_high'], df['bollinger_low'] = bollinger_bands(df['close'])

    if (df['rsi'].iloc[-1] < 30) and (df['close'].iloc[-1] < df['bollinger_low'].iloc[-1]):
        place_order(stock, 'BUY', allocated_capital)
    elif (df['rsi'].iloc[-1] > 70) and (df['macd'].iloc[-1] > df['macd_signal'].iloc[-1]):
        place_order(stock, 'SELL', allocated_capital)

# Placing order with position sizing
def place_order(stock, transaction_type, allocated_capital):
    position_size = calculate_position_size(allocated_capital)
    latest_price = get_latest_price(stock)
    quantity = int(position_size / latest_price)

    try:
        order = kite.place_order(
            tradingsymbol=stock,
            exchange="NSE",
            transaction_type=transaction_type,
            quantity=quantity,
            order_type="MARKET",
            product="MIS"
        )
        return order
    except Exception as e:
        print(f"Error placing order for {stock}: {str(e)}")
        return None

# Calculating net profit or loss
def calculate_net_profit_or_loss(entry_price, exit_price, quantity, transaction_type):
    gross_profit = (exit_price - entry_price) * quantity if transaction_type == 'BUY' else (entry_price - exit_price) * quantity
    charges = calculate_charges(entry_price, exit_price, quantity)
    net_profit = gross_profit - charges
    return net_profit

#  Charges
def calculate_charges(entry_price, exit_price, quantity):
    brokerage = min(0.0003 * quantity * entry_price, 20)
    sell_side_charges = 0.00025 * quantity * exit_price
    transaction_charge = 0.0000322 * (quantity * (entry_price + exit_price) / 2)
    gst = 0.18 * (brokerage + transaction_charge)

    total_charges = brokerage + sell_side_charges + transaction_charge + gst
    return total_charges