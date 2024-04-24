import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

exchange = ccxt.binance({
    'apiKey': '',
    'secret': '',
})

symbols = ['BTC/USDT',
           'ETH/USDT',
           'ADA/USDT',
           'SOL/USDT',
           'BNB/USDT',
           'DOT/USDT',
           'ATOM/USDT']

now = datetime.now()
today = now.strftime("%Y-%m-%d %H:%M:%S")
lastmonth = now - timedelta(days=30)
yesterday = now - timedelta(hours=24)

lastmonth = lastmonth.strftime("%Y-%m-%d %H:%M:%S")
yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")

print('DATE: ', today)
# print(lastmonth)
# print(yesterday)

start_date = int(pd.to_datetime(lastmonth).timestamp() * 1000)
end_date = int(pd.to_datetime(today).timestamp() * 1000)

for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe='1d', since=exchange.parse_date(start_date), limit=end_date - start_date)
    data = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Date'] = pd.to_datetime(data['Date'], unit='ms')

    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['MA_200'] = data['Close'].rolling(window=200).mean()
    delta = data['Close'].diff(1)
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=14).mean()
    roll_down = down.rolling(window=14).mean().abs()
    RS = roll_up / roll_down
    data['RSI'] = 100.0 - (100.0 / (1.0 + RS))
    data['Trend'] = ''
    data.loc[data['Close'] > data['MA_50'], 'Trend'] = 'Up   /'
    data.loc[data['Close'] < data['MA_50'], 'Trend'] = 'Down \\'
    
    exchange.load_markets()
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], label='Close')  # Use 'Date' as the x-axis
    plt.plot(data['Date'], data['MA_50'], label='MA 50')
    plt.plot(data['Date'], data['MA_200'], label='MA 200')
    plt.legend(loc='upper left')
    plt.title(symbol + ' Historical Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['RSI'], label='RSI')
    plt.axhline(y=70, color='r', linestyle='--', label='Overbought')
    plt.axhline(y=30, color='g', linestyle='--', label='Oversold')
    plt.legend(loc='upper left')
    plt.title(symbol + ' Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.show()

    print(f'\nMonthly Trend : {symbol}')
    print('Current Trend :', data.iloc[-1]['Trend'])
    print('Next Few Hours:', 'Up   /' if data.iloc[-1]['Close'] > data.iloc[-1]['MA_50'] else 'Down \\')
    print('Next Few Days :', 'Up   /' if data.iloc[-1]['Close'] > data.iloc[-1]['MA_200'] else 'Down \\')
    print('Today\'s price :', current_price)

start_date = int(pd.to_datetime(yesterday).timestamp() * 1000)
end_date = int(pd.to_datetime(today).timestamp() * 1000)
    
for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', since=exchange.parse_date(start_date), limit=end_date - start_date)
    data = pd.DataFrame(bars, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Date'] = pd.to_datetime(data['Date'], unit='ms')

    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['MA_200'] = data['Close'].rolling(window=200).mean()
    delta = data['Close'].diff(1)
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=14).mean()
    roll_down = down.rolling(window=14).mean().abs()
    RS = roll_up / roll_down
    data['RSI'] = 100.0 - (100.0 / (1.0 + RS))
    data['Trend'] = ''
    data.loc[data['Close'] > data['MA_50'], 'Trend'] = 'Up   /'
    data.loc[data['Close'] < data['MA_50'], 'Trend'] = 'Down \\'
    
    exchange.load_markets()
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], label='Close')  # Use 'Date' as the x-axis
    plt.plot(data['Date'], data['MA_50'], label='MA 50')
    plt.plot(data['Date'], data['MA_200'], label='MA 200')
    plt.legend(loc='upper left')
    plt.title(symbol + ' Historical Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['RSI'], label='RSI')
    plt.axhline(y=70, color='r', linestyle='--', label='Overbought')
    plt.axhline(y=30, color='g', linestyle='--', label='Oversold')
    plt.legend(loc='upper left')
    plt.title(symbol + ' Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.show()

    print(f'\nDaily Trend   : {symbol}')
    print('Current Trend :', data.iloc[-1]['Trend'])
    print('Next Few Hours:', 'Up   /' if data.iloc[-1]['Close'] > data.iloc[-1]['MA_50'] else 'Down \\')
    print('Next Few Days :', 'Up   /' if data.iloc[-1]['Close'] > data.iloc[-1]['MA_200'] else 'Down \\')
    print('Today\'s price :', current_price)
