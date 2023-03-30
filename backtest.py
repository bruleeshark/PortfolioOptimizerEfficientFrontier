# Use backtesting framework like Backtrader or Zipline to test trading strategy on historical data
# Simulate trades based on trading strategy
# Evaluate performance of portfolio
# Specify time range of historical data, initial balance of portfolio, and any fees or slippage that may affect trading process

import os
import pandas as pd
import backtrader as bt
from dotenv import load_dotenv
from efficient_frontier import get_optimal_portfolio_weights
from trading_strategy import TradingStrategy

load_dotenv()

# Load historical data from CSV file
data = pd.read_csv("historical_data.csv")
data = data.set_index(pd.DatetimeIndex(data['Date']))
data = data.drop(columns=['Date'])

# Define initial portfolio balance and fees
initial_balance = 1000
fees = 0.1

class TradingStrategyBacktrader(bt.Strategy):
    def __init__(self):
        # Set initial portfolio balance
        self.broker.set_cash(initial_balance)
        
        # Define trading strategy
        self.trading_strategy = TradingStrategy()

    def next(self):
        # Get current portfolio value
        portfolio_value = self.broker.get_value()
        
        # Calculate current portfolio weights
        current_weights = {}
        for data_name in self.datas:
            current_weights[data_name._name] = self.getposition(data_name).size * data_name.close[0] / portfolio_value
        
        # Optimize portfolio weights using historical data
        optimal_weights = get_optimal_portfolio_weights(data, fees)
        
        # Calculate trade amounts based on optimal weights and current prices
        trades = self.trading_strategy.calculate_trades(current_weights, optimal_weights, self.datas)
        
        # Execute trades
        for trade in trades:
            self.order_target_percent(data=self.datas[trade['symbol']], target=trade['target'])
        
# Create Backtrader Cerebro engine and add data feed
cerebro = bt.Cerebro()
for symbol in ['USDC', 'FTM', 'WETH']:
    data = bt.feeds.PandasData(dataname=data[symbol])
    data._name = symbol
    cerebro.adddata(data)

# Add trading strategy
cerebro.addstrategy(TradingStrategyBacktrader)

# Set initial portfolio balance
cerebro.broker.setcash(initial_balance)

# Run backtest
cerebro.run()

# Print final portfolio value
final_value = cerebro.broker.getvalue()
print(f"Final portfolio value: {final_value}")

# Note that this code assumes that efficient_frontier.py and trading_strategy.py 
# are in the same directory as the backtest.py file. 
# You may need to adjust the imports if these files are located elsewhere.
# Additionally, you will need to install the Backtrader framework (pip install backtrader) to run this code.
