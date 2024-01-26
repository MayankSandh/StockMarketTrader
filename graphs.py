import yfinance as yf
import matplotlib.pyplot as plt

# Fetching data
data = yf.download('AAPL', start='2023-01-01', end='2024-01-01')

# Calculating Simple Moving Average (SMA)
window_size = 20  # Adjust as needed
data['SMA'] = data['Close'].rolling(window=window_size).mean()

# Plotting
plt.plot(data['Close'], label='Closing Price')
plt.plot(data['SMA'], label=f'SMA ({window_size} days)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('AAPL Closing Prices with SMA')
plt.legend()
plt.grid()
plt.show()
