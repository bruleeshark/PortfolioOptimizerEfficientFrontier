# Create main.py file that imports functions from other files and orchestrates entire process of 
# calculating efficient frontier, optimizing portfolio weights, executing trades, and backtesting strategy
# Use command-line arguments or environment variables to specify inputs and outputs of program

import argparse
from datetime import datetime
from trading_strategy import MyTradingStrategy
from efficient_frontier import EfficientFrontier
from bot import MyBot

parser = argparse.ArgumentParser(description='Run backtest or activate trading bot')
parser.add_argument('--backtest', action='store_true', help='run backtest process')
parser.add_argument('--activate', action='store_true', help='activate trading bot')
parser.add_argument('--initial_balance', type=float, default=10000.0, help='initial balance of portfolio')
parser.add_argument('--fees', type=float, default=0.0, help='transaction fees in percentage')
parser.add_argument('--slippage', type=float, default=0.0, help='slippage in percentage')
parser.add_argument('--start_date', type=str, default='2017-01-01', help='start date of historical data in yyyy-mm-dd format')
parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='end date of historical data in yyyy-mm-dd format')

args = parser.parse_args()

if args.backtest:
    # Run backtest process
    trading_strategy = MyTradingStrategy()
    ef = EfficientFrontier(args.initial_balance, args.fees, args.slippage)
    ef.run_backtest(trading_strategy, args.start_date, args.end_date)

elif args.activate:
    # Activate trading bot
    bot = MyBot()
    bot.run()
    
else:
    print('Please specify either --backtest or --activate flag')

# This version of main.py accepts two new command-line arguments: 
# --initial_balance, --fees, --slippage, --start_date, and --end_date, 
# which allows the user to specify 
# initial balance of their portfolio, transaction fees, slippage, and the start and end dates for the historical data.

# When --backtest is specified, the script runs the backtest process with the specified parameters.
# When --activate is specified, the script activates the trading bot. 
# If neither flag is specified, the script outputs an error message.
