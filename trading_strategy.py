import os
import time
import web3
import json
from web3 import Web3
from dotenv import load_dotenv
from pypfopt import expected_returns, risk_models, EfficientFrontier
import pandas as pd

load_dotenv()

# Connect to Web3 provider and get account
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))
w3.eth.default_account = w3.eth.accounts[0]

# Connect to SpookySwap router and contracts
router_address = Web3.toChecksumAddress(os.getenv("ROUTER_ADDRESS"))
router_abi = json.loads(os.getenv("ROUTER_ABI"))
router = w3.eth.contract(address=router_address, abi=router_abi)

usdc_address = Web3.toChecksumAddress(os.getenv("USDC_ADDRESS"))
ftm_address = Web3.toChecksumAddress(os.getenv("FTM_ADDRESS"))
weth_address = Web3.toChecksumAddress(os.getenv("WETH_ADDRESS"))

usdc_abi = json.loads(os.getenv("USDC_ABI"))
ftm_abi = json.loads(os.getenv("FTM_ABI"))
weth_abi = json.loads(os.getenv("WETH_ABI"))

usdc = w3.eth.contract(address=usdc_address, abi=usdc_abi)
ftm = w3.eth.contract(address=ftm_address, abi=ftm_abi)
weth = w3.eth.contract(address=weth_address, abi=weth_abi)

# Define function to read data from CSV file
def read_data_from_csv():
    data = pd.read_csv("historical_data.csv", header=None)
    data.columns = ["Date", "USDC", "FTM", "WETH"]
    data = data.set_index("Date")
    return data

# Define function to optimize portfolio weights
def optimize_portfolio(data):
    mu = expected_returns.mean_historical_return(data)
    Sigma = risk_models.sample_cov(data)
    ef = EfficientFrontier(mu, Sigma)
    return ef.max_sharpe()

# Define function to buy or sell tokens on Uniswap
def execute_trade(token_in, token_out, amount_in, amount_out_min, path):
    deadline = int(time.time()) + 3600
    tx_hash = router.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_min,
        path,
        w3.eth.default_account,
        deadline
    ).transact({'from': w3.eth.default_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Executed trade: {amount_in} {token_in.symbol()} for {amount_out_min} {token_out.symbol()}")

# Define function to handle trading errors
def handle_trade_error(error):
    print(f"An error occurred while executing trade: {error}")

# Main function to execute trades based on optimal portfolio weights
def main():
    # Read data from CSV file
    data = read_data_from_csv()
    
    # Optimize portfolio weights
    weights = optimize_portfolio(data)
    
    # Get token balances
    usdc_balance = usdc.functions.balanceOf(w3.eth.default_account).call() / 10**6
    ftm_balance = ftm.functions.balanceOf(w3.eth.default_account).call() / 10**18
    weth_balance = weth.functions.balanceOf(w3.eth.default_account).call() / 10**18
    
    # Calculate amounts to buy and sell based on portfolio weights and current prices
    usdc_amount = weights["USDC"] * (usdc_balance + ftm_balance * router.functions.getAmountsOut(ftm_balance, [ftm_address, usdc_address]).call()[1] / 10**6 + weth_balance * router.functions.getAmountsOut(weth_balance, [weth_address, usdc_address]).call()[1] / 10**18)
    weth_amount = weights["WETH"] * (weth_balance + ftm_balance * router.functions.getAmountsOut(ftm_balance, [ftm_address, weth_address]).call()[1] / 10**18 + usdc_balance * router.functions.getAmountsOut(usdc_balance * 10**6, [usdc_address, weth_address]).call()[1] / 10**18)

    # Define token symbols
    USDC = usdc.functions.symbol().call()
    FTM = ftm.functions.symbol().call()
    WETH = weth.functions.symbol().call()

    # Calculate amounts to buy and sell
    usdc_amount = round(usdc_amount, 2)
    weth_amount = round(weth_amount, 2)

    # Execute trades
    try:
        execute_trade(USDC, FTM, usdc_amount, 0, [usdc_address, weth_address, ftm_address])
        execute_trade(WETH, FTM, weth_amount, 0, [weth_address, ftm_address])
    except Exception as e:
        handle_trade_error(e)

    if __name__ == '__main__':
        main()
