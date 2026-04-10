#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import yfinance as yf

class QuantEngine:
    """A simple backtesting engine for quantitative research."""
    
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.data = yf.download(ticker, start=start_date, end=end_date)

    def moving_average_strategy(self, short_window=20, long_window=50):
        """Generates signals based on moving average crossovers."""
        signals = pd.DataFrame(index=self.data.index)
        signals['price'] = self.data['Close']
        signals['short_mavg'] = self.data['Close'].rolling(window=short_window).mean()
        signals['long_mavg'] = self.data['Close'].rolling(window=long_window).mean()
        
        # Create signals: 1 is Buy, 0 is Hold/Sell
        signals['signal'] = 0.0
        signals['signal'][short_window:] = np.where(
            signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0
        )
        signals['positions'] = signals['signal'].diff()
        return signals

    def calculate_metrics(self, signals):
        """Calculates basic performance metrics like Sharpe Ratio."""
        returns = signals['price'].pct_change()
        strategy_returns = returns * signals['signal'].shift(1)
        sharpe = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252)
        return {"Sharpe Ratio": round(sharpe, 2)}

# Example Usage
if __name__ == "__main__":
    engine = QuantEngine("NASDAQ:AAPL", "2023-01-01", "2024-01-01")
    strategy_signals = engine.moving_average_strategy()
    print(engine.calculate_metrics(strategy_signals))


# In[10]:





# In[ ]:





# In[ ]:




