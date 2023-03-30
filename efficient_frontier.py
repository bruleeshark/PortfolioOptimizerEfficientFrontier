# Create efficient_frontier.py file
# Use PyPortfolioOpt library to calculate expected returns and covariance matrix of assets
# Calculate the efficient frontier
# Specify any constraints on portfolio weights

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define function to read data from CSV file
def read_data_from_csv():
    data = pd.read_csv("historical_data.csv", header=None)
    data.columns = ["Date", "USDC", "FTM", "WETH"]
    data = data.set_index("Date")
    return data

# Define function to calculate beta for an asset
def calculate_beta(asset, market):
    asset_returns = asset.pct_change().dropna()
    market_returns = market.pct_change().dropna()
    cov_matrix = np.cov(asset_returns, market_returns, ddof=1)
    beta = cov_matrix[0][1] / cov_matrix[1][1]
    return beta

# Define function to calculate time-weighted average return for an asset
def calculate_twap(asset):
    return asset.pct_change(periods=90).dropna().mean()

# Define function to calculate risk/reward ratio for a portfolio allocation
def calculate_risk_reward_ratio(weights, data):
    portfolio_returns = np.dot(data.pct_change().dropna(), weights)
    portfolio_beta = calculate_beta(portfolio_returns, data["WETH"].pct_change().dropna())
    portfolio_twap = np.dot(weights, [calculate_twap(data[asset]) for asset in ["USDC", "FTM", "WETH"]])
    return portfolio_beta / portfolio_twap

# Define function to simulate portfolio allocations and calculate risk/reward ratios
def simulate_portfolio_allocations(data):
    portfolio_allocations = []
    for usdc_weight in np.linspace(0, 1, 21):
        for ftm_weight in np.linspace(0, 1-usdc_weight, 21):
            weth_weight = 1 - usdc_weight - ftm_weight
            weights = [usdc_weight, ftm_weight, weth_weight]
            portfolio_allocations.append((weights, calculate_risk_reward_ratio(weights, data)))
    return portfolio_allocations

# Define function to plot portfolio allocations on an XY grid
def plot_portfolio_allocations(portfolio_allocations):
    x = [allocation[1] for allocation in portfolio_allocations]
    y = [allocation[0][0] / allocation[0][1] for allocation in portfolio_allocations]
    plt.scatter(x, y)
    plt.xlabel("Risk/Reward Ratio")
    plt.ylabel("USDC/FTM Ratio")
    plt.title("Efficient Frontier")
    plt.show()

# Define function to identify most efficient portfolio allocations
def identify_efficient_portfolios(portfolio_allocations):
    sorted_allocations = sorted(portfolio_allocations, key=lambda x: x[1], reverse=True)
    efficient_allocations = []
    for allocation in sorted_allocations:
        if allocation[1] > 0:
            efficient_allocations.append(allocation)
        if len(efficient_allocations) >= 5:
            break
    return efficient_allocations

# Main function to run the efficient frontier analysis
def main():
    data = read_data_from_csv()
    portfolio_allocations = simulate_portfolio_allocations(data)
    plot_portfolio_allocations(portfolio_allocations)
    efficient_allocations = identify_efficient_portfolios(portfolio_allocations)
    print("Most Efficient Portfolio Allocations:")
    for allocation in efficient_allocations:
        print(f"{allocation[0]} (Risk/Reward Ratio: {allocation[1]:.2f})")

if __name__ == '__main__':
    main()
