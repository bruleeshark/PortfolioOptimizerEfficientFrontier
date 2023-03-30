# Use the file we wrote, efficient_frontier.py , to find the optimal portfolio weights.
# Use optimization algorithms provided by PyPortfolioOpt library to find optimal portfolio weights.
# Find portfolio weights that maximize the Sharpe ratio.
# Specify constraints on portfolio weights such that the portfolio is never 0% of any asset.

# Import necessary libraries
import numpy as np
import pandas as pd
from pypfopt import expected_returns, risk_models, EfficientFrontier
from pypfopt.constraints import MinWeightConstraint

# Define function to read data from CSV file
def read_data_from_csv():
    data = pd.read_csv("historical_data.csv", header=None)
    data.columns = ["Date", "USDC", "FTM", "WETH"]
    data = data.set_index("Date")
    return data

# Define function to optimize portfolio weights
def optimize_portfolio(data):
    # Calculate expected returns and covariance matrix of assets
    mu = expected_returns.mean_historical_return(data)
    Sigma = risk_models.sample_cov(data)
    
    # Define constraints on portfolio weights
    constraints = [MinWeightConstraint(0.01) for _ in range(len(data.columns))]
    
    # Find portfolio weights that maximize the Sharpe ratio
    ef = EfficientFrontier(mu, Sigma, constraints=constraints)
    weights = ef.max_sharpe()
    
    # Return optimal portfolio weights
    return weights

# Main function to run the portfolio optimization
def main():
    data = read_data_from_csv()
    weights = optimize_portfolio(data)
    print("Optimal Portfolio Weights:")
    for asset, weight in weights.items():
        print(f"{asset}: {weight:.2%}")

if __name__ == '__main__':
    main()
   
# This implementation uses the expected_returns.mean_historical_return() function and 
# the risk_models.sample_cov() function from the PyPortfolioOpt library to calculate 
# the expected returns and covariance matrix of the assets. 
# It then defines constraints on the portfolio weights using the MinWeightConstraint() class, 
# which ensures that the portfolio is never 0% of any asset. 
# Finally, it uses the EfficientFrontier() class to find the portfolio weights 
# that maximize the Sharpe ratio, and returns these weights.

# In the main function, it reads the data from the CSV file, calls the optimize_portfolio() function 
# to find the optimal portfolio weights, and prints the results.
