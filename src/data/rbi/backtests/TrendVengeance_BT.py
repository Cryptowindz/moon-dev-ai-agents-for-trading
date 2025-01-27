Here is the implementation of the TrendVengeance strategy in Python using the `backtesting.py` framework. This implementation includes all the necessary components, such as trend identification, pullback entries, trailing stops, and risk management. It also includes Moon Dev-themed debug prints for better visualization and debugging.

```python
import os
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Define the TrendVengeance strategy
class TrendVengeance(Strategy):
    # Strategy parameters
    risk_per_trade = 0.02  # Risk 2% of the account per trade
    trailing_stop_pct = 0.02  # 2% trailing stop
    swing_period = 20  # Period for identifying swing highs/lows

    def init(self):
        # Clean and prepare data
        self.data.columns = self.data.columns.str.strip().str.lower()
        self.data = self.data.drop(columns=[col for col in self.data.columns if 'unnamed' in col.lower()])
        self.data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        # Calculate swing highs and lows using talib.MAX/MIN
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=self.swing_period)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period)

        # Print Moon Dev-themed initialization message
        print("🌙✨ Moon Dev's TrendVengeance Strategy Initialized! 🚀✨")

    def next(self):
        # Calculate position size based on risk percentage
        account_size = self.equity
        position_size = (account_size * self.risk_per_trade) / (self.data.Close[-1] - self.swing_low[-1])

        # Long entry logic: Price pulls back to swing low in an uptrend
        if self.data.Close[-1] > self.swing_high[-1] and self.data.Close[-2] <= self.swing_high[-2]:
            print("🌙✨ Moon Dev Signal: Long Entry Detected! 🚀")
            self.buy(size=position_size, sl=self.swing_low[-1])

        # Short entry logic: Price pulls back to swing high in a downtrend
        elif self.data.Close[-1] < self.swing_low[-1] and self.data.Close[-2] >= self.swing_low[-2]:
            print("🌙✨ Moon Dev Signal: Short Entry Detected! 🚀")
            self.sell(size=position_size, sl=self.swing_high[-1])

        # Trailing stop logic
        for trade in self.trades:
            if trade.is_long:
                new_sl = self.data.Close[-1] * (1 - self.trailing_stop_pct)
                if new_sl > trade.sl:
                    trade.sl = new_sl
                    print(f"🌙✨ Moon Dev Update: Trailing Stop for Long Trade Updated to {new_sl:.2f} 🚀")
            elif trade.is_short:
                new_sl = self.data.Close[-1] * (1 + self.trailing_stop_pct)
                if new_sl < trade.sl:
                    trade.sl = new_sl
                    print(f"🌙✨ Moon Dev Update: Trailing Stop for Short Trade Updated to {new_sl:.2f} 🚀")

# Load data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=['datetime'])
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if 'unnamed' in col.lower()])
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# Initialize and run backtest
bt = Backtest(data, TrendVengeance, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print initial results
print("🌙✨ Moon Dev's TrendVengeance Initial Backtest Results: 🚀")
print(stats)
print(stats._strategy)

# Save initial plot
chart_file = os.path.join("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/charts", "TrendVengeance_initial_chart.html")
bt.plot(filename=chart_file, open_browser=False)
print(f"🌙✨ Moon Dev: Initial Backtest Plot Saved to {chart_file} 🚀")

# Optimize parameters
print("🌙✨ Moon Dev: Optimizing Strategy Parameters... 🚀")
opt_stats = bt.optimize(
    risk_per_trade=[0.01, 0.02, 0.03],
    trailing_stop_pct=[0.01, 0.02, 0.03],
    swing_period=range(15, 25, 5),
    maximize='Return [%]'
)

# Print optimized results
print("🌙✨ Moon Dev's TrendVengeance Optimized Results: 🚀")
print(opt_stats)
print(opt_stats._strategy)

# Save optimized plot
opt_chart_file = os.path.join("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/charts", "TrendVengeance_optimized_chart.html")
bt.plot(filename=opt_chart_file, open_browser=False)
print(f"🌙✨ Moon Dev: Optimized Backtest Plot Saved to {opt_chart_file} 🚀")
```

### Key Features:
1. **Trend Identification**: Uses swing highs and lows to identify trends.
2. **Pullback Entries**: Enters trades during pullbacks to swing highs/lows.
3. **Trailing Stops**: Dynamically adjusts stop-loss levels to lock in profits.
4. **Risk Management**: Calculates position sizes based on a fixed risk percentage.
5. **Parameter Optimization**: Optimizes risk percentage, trailing stop percentage, and swing period.
6. **Moon Dev-Themed Debug Prints**: Adds fun and informative debug messages.

### Execution Order:
1. Runs an initial backtest with default parameters.
2. Prints detailed statistics and strategy information.
3. Saves the initial performance plot.
4. Optimizes key parameters.
5. Prints optimized results and saves the final plot.

Let me know if you need further adjustments or additional features! 🌙✨🚀