import yfinance as yf
from random import randint
from utils import calculate_future_date
from broker import Broker
from strategies import StockFunctions

symbol = 'INFY.BO'
symbol = 'INFY.BO'
start_date = '2012-07-01'
end_date = calculate_future_date(start_date, 365*5)
infosys_data = yf.download(symbol, start=start_date, end=end_date)

broker = Broker()
functions = StockFunctions(infosys_data)

EMA_12 = functions.EMA(window = 12)
EMA_26 = functions.EMA(window = 26)
MACD = EMA_12 - EMA_26
MACD_EMA = functions.custom_EMA(MACD, window=9)
SIGNAL = MACD - MACD_EMA
time = 0
for i in range(len(infosys_data)):
    if broker.shares == 0 and broker.buy_share > 12:
        break
    OpenPrice = infosys_data['Open'].iloc[i]
    ClosePrice = infosys_data['Close'].iloc[i]
    HighPrice = infosys_data['High'].iloc[i]
    LowPrice = infosys_data['Low'].iloc[i]
    Volume = infosys_data['Volume'].iloc[i]


    if SIGNAL[i] < -6.5:
        broker.buy(20, ClosePrice)
    elif SIGNAL[i] > 4.5:
        broker.sell(20, ClosePrice)
    
    time+=1

# functions.data_to_show['MACD'] = MACD
# functions.show_graph()

print(f"Time spend trading: {time}")
rem_share_value = infosys_data['Close'].mean()
broker.show_money()
broker.show_remaining_shares()
broker.show_buy_and_sell_shares()
broker.show_returns(rem_share_value)