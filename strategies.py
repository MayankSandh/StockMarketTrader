import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
class StockFunctions:
    RSI = []
    
    def __init__(self, data):
        self.stock_data = data
        self.stock_len = len(self.stock_data)
    
    def MACD(self):
        pass

    data_to_show = {} # label of the data : the actual data

    def generate_RSI(self, window = 14):
        gains = []
        losses = []
        for index in range((self.stock_len)):
            if index < window:
                self.RSI.append(self.stock_data['Close'].iloc[index])
                continue
            for i in range(1, window + 1):
                price_diff = self.stock_data['Close'].iloc[index - i + 1] - self.stock_data['Close'].iloc[index - i]
                if price_diff > 0:
                    gains.append(price_diff)
                else:
                    losses.append(abs(price_diff))

            avg_gain = sum(gains) / len(gains) if gains else 0
            avg_loss = sum(losses) / len(losses) if losses else 0

            self.RSI.append(100-100/(1+(avg_gain / avg_loss)) if avg_loss != 0 else 100)
        return np.array(self.RSI)
    
    def SMA(self, window = 26):
        SMA = []
        for index in range((self.stock_len)):
                if index < window:
                    SMA.append(self.stock_data['Close'].iloc[index])
                    continue
                acc = 0
                for i in range(window):
                    acc += self.stock_data['Close'].iloc[index - i]
                SMA.append(acc / window)
        return np.array(SMA)

    def STD_DEV_DATA(self, window = 20):
        STD_DEV_DATA = []
        for index in range((self.stock_len)):
            if index < window:
                STD_DEV_DATA.append(100000000)
                continue
            STD_DEV_DATA.append(self.stock_data['Close'][index-window: index].std())
        return np.array(STD_DEV_DATA)

    def EMA(self, window = 26):
        EMA = []
        alpha = 2/(1+window)
        for index in range(self.stock_len):
            if index < window:
                EMA.append(self.stock_data['Close'].iloc[index])
                continue
            EMA.append(alpha * self.stock_data['Close'].iloc[index] + (1 - alpha) * EMA[index - 1])
        return np.array(EMA)
    
    def custom_EMA(self, data, window = 26):
        EMA = []
        alpha = 2/(1+window)
        for index in range(len(data)):
            if index < window:
                EMA.append(data[index])
                continue
            EMA.append(alpha * data[index] + (1 - alpha) * EMA[index - 1])
        return np.array(EMA)
    
    def show_graph(self):
        data = deepcopy(self.stock_data)
        plt.plot(data['Close'], label='Closing Price')
        for key, value in self.data_to_show.items():
            # plt.plot(value, label=f'{key}')
            data[key] = value
            plt.plot(data[key], label=f'{key}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Stock Data')
        plt.legend()
        plt.grid()
        plt.show()











