import yfinance as yf
from random import randint
from utils import calculate_future_date
from broker import Broker
from strategies import StockFunctions
# import talib

def random_action(shares):
    action = randint(-1, 1)
    if action == 0: # HOLD
        return 0, 0
    elif action == 1: # BUY
        return 1, randint(0, 1000)
    elif action == -1: # SELL
        return -1, randint(0, shares)
    
def moving_average(stock_data, index, window):
    acc = 0
    for i in range(window):
        acc += stock_data['Close'].iloc[index - i]
    return acc / window

def EMA(stock_data, index, EMA_data, alpha):
    return alpha * stock_data['Close'].iloc[index] + (1 - alpha) * EMA_data[index - 1]

def calculate_RSI(stock_data, index, RS_window):
    gains = []
    losses = []

    for i in range(1, RS_window + 1):
        price_diff = stock_data['Close'].iloc[index - i + 1] - stock_data['Close'].iloc[index - i]
        if price_diff > 0:
            gains.append(price_diff)
        else:
            losses.append(abs(price_diff))

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    return 100-100/(1+(avg_gain / avg_loss)) if avg_loss != 0 else 100

def std_dev_signal(stock_data, index, window):
    return stock_data['Close'][index-window: index].std()
    
symbol = 'INFY.BO'
symbol = 'INFY.BO'
start_date = '2018-07-01'
end_date = calculate_future_date(start_date, 365*5)
infosys_data = yf.download(symbol, start=start_date, end=end_date)

broker = Broker()
functions = StockFunctions(infosys_data)

# DATA
moving_average_data = []
EMA_data = []
day12_EMA_data = []
day26_EMA_data = []
RSI_data = []
std_data = []

RS_window = 14  # Set the RS time period


lastBuy = False
for i in range(len(infosys_data)):
    if broker.shares == 0 and broker.buy_share > 12:
        break
    OpenPrice = infosys_data['Open'].iloc[i]
    ClosePrice = infosys_data['Close'].iloc[i]
    HighPrice = infosys_data['High'].iloc[i]
    LowPrice = infosys_data['Low'].iloc[i]
    Volume = infosys_data['Volume'].iloc[i]

    # Calculate Moving Average
    moving_average_window = 20
    if i<moving_average_window:
        value_ma = ClosePrice
    else:
        value_ma = moving_average(infosys_data, i, moving_average_window)
    moving_average_data.append(value_ma)

    # Calculate EMA
    EMA_TimePeriod = 12
    EMA_TimePeriod2 = 26
    alpha = 2 / (EMA_TimePeriod + 1)
    alpha2 = 2 / (EMA_TimePeriod2 + 1)
    if i<EMA_TimePeriod:
        value_ema = ClosePrice
    else:
        value_ema = EMA(infosys_data, i, EMA_data, alpha)
    if i<EMA_TimePeriod:
        value_ema = ClosePrice
    else:
        value_ema = EMA(infosys_data, i, EMA_data, alpha)
    EMA_data.append(value_ema)
    EMA_data.append(value_ema)

    # Calculate RS
    if i >= RS_window:
        value_rs = calculate_RSI(infosys_data, i, RS_window)
        RSI_data.append(value_rs)
    else:
        RSI_data.append(50)
    # print(infosys_data.index[i], RSI_data[i], infosys_data['Close'][i])
    if RSI_data[i] > 70: # SELL
        amt_shares = 20
        if broker.shares - amt_shares >= 0:
            broker.sell(amt_shares, ClosePrice)

    elif RSI_data[i] < 30: # BUY
        amt_shares = 20
        broker.buy(amt_shares, ClosePrice)
    
    # Calculate Std
    std_window = 20
    if i<=std_window:
        std_data.append(ClosePrice)
    else:
        std_data.append(std_dev_signal(infosys_data, i, std_window))
    
    if std_data[i]*2 + moving_average_data[i] <= ClosePrice: # sell
        amt_shares = 20
        if broker.shares - amt_shares >= 0:
            broker.sell(amt_shares, ClosePrice)
    elif -1*std_data[i]*2 + moving_average_data[i] >= ClosePrice: # buy
        amt_shares = 20
        broker.buy(amt_shares, ClosePrice)


# print(RSI_data)
rem_share_value = infosys_data['Close'].mean()
broker.show_money()
broker.show_remaining_shares()
broker.show_buy_and_sell_shares()
broker.show_returns(rem_share_value)

# Display the calculated data
# print("Moving Average Data:", moving_average_data)
# print("EMA Data:", EMA_data)
# print("RSI Data:", RSI_data)
#bogdanoff
