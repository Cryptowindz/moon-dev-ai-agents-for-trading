import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import numpy as np

class VWAPVolumeStrategy(Strategy):
    # Define the parameters for the strategy
    vwap_window = 20  # VWAP calculation window
    volume_ma_window = 20  # Volume moving average window
    volume_threshold = 2.0  # Volume threshold multiplier (e.g., 2.0x average volume)
    stop_loss = 0.02  # 2% stop loss
    take_profit = 0.04  # 4% take profit
    trend_window = 50  # Window for trend calculation

    def init(self):
        # Calculate VWAP using numpy operations
        typical_price = (self.data.High + self.data.Low + self.data.Close) / 3
        volume = self.data.Volume
        
        # Create rolling sum arrays for VWAP
        rolling_sum_price_volume = np.convolve(typical_price * volume, np.ones(self.vwap_window), 'valid')
        rolling_sum_volume = np.convolve(volume, np.ones(self.vwap_window), 'valid')
        
        # Pad the arrays to match original length
        pad_length = len(typical_price) - len(rolling_sum_price_volume)
        self.vwap = np.pad(rolling_sum_price_volume / rolling_sum_volume, (pad_length, 0), 'constant', constant_values=np.nan)
        
        # Calculate volume indicators
        self.volume_ma = pd.Series(volume).rolling(window=self.volume_ma_window).mean().values
        self.volume_std = pd.Series(volume).rolling(window=self.volume_ma_window).std().values
        
        # Calculate trend using simple moving average
        self.trend_ma = pd.Series(self.data.Close).rolling(window=self.trend_window).mean().values
        
        print("🌙 MOON DEV: VWAP and Volume calculations initialized successfully! 🚀")

    def next(self):
        price = self.data.Close[-1]
        
        # Skip if we don't have enough data yet
        if np.isnan(self.vwap[-1]) or np.isnan(self.volume_ma[-1]) or np.isnan(self.trend_ma[-1]):
            return

        # Only enter new positions if we don't have any open positions
        if not self.position:
            volume_z_score = (self.data.Volume[-1] - self.volume_ma[-1]) / self.volume_std[-1]
            price_to_vwap = price / self.vwap[-1] - 1  # Percentage difference from VWAP
            
            # Strong trend conditions
            uptrend = price > self.trend_ma[-1]
            strong_volume = volume_z_score > 2  # Volume is 2 standard deviations above mean
            
            # Go long if price is above VWAP with strong volume in uptrend
            if (uptrend and 
                price_to_vwap > 0.01 and  # Price is 1% above VWAP
                strong_volume and 
                self.data.Close[-1] > self.data.Open[-1]):  # Green candle
                
                sl = price * (1 - self.stop_loss)
                tp = price * (1 + self.take_profit)
                self.buy(sl=sl, tp=tp, size=0.5)  # Use only 50% of available capital
                print("🌕 MOON DEV: Long position entered! 🚀📈")

            # Go short if price is below VWAP with strong volume in downtrend
            elif (not uptrend and 
                  price_to_vwap < -0.01 and  # Price is 1% below VWAP
                  strong_volume and 
                  self.data.Close[-1] < self.data.Open[-1]):  # Red candle
                
                sl = price * (1 + self.stop_loss)
                tp = price * (1 - self.take_profit)
                self.sell(sl=sl, tp=tp, size=0.5)  # Use only 50% of available capital
                print("🌑 MOON DEV: Short position entered! 🚀📉")

# Download Apple (AAPL) data from Yahoo Finance
ticker = "GOOG"
df = yf.download(ticker, start="2020-01-01", end="2023-01-01")

# Create a new DataFrame with the exact structure needed
data = pd.DataFrame(index=df.index)
data['Open'] = df['Open']
data['High'] = df['High']
data['Low'] = df['Low']
data['Close'] = df['Close']
data['Volume'] = df['Volume']

# Drop rows with missing data
data = data.dropna()

# Run the backtest
bt = Backtest(data, VWAPVolumeStrategy, cash=10000, commission=.002)
stats = bt.run()

# Print the results
print(stats)

# Plot the backtest results with custom settings
bt.plot(resample='1D')  # Use daily resampling