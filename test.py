import yfinance as yf

# Replace 'INFY.BO' with the appropriate symbol for Infosys on the NSE
symbol = 'INFY.BO'

# Fetch historical data for Infosys in INR
infosys_data = yf.download(symbol, start='2022-01-01', end='2022-01-10')

# Display the stock data
print(infosys_data)
